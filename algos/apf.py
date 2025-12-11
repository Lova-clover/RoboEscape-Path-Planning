"""
Artificial Potential Field (APF) 알고리즘
"""

import numpy as np
import math
from config import APF_ATTRACT_GAIN, APF_REPULSE_GAIN, APF_INFLUENCE_DISTANCE, TILE_SIZE
from game.grid import is_valid_grid, is_walkable


class APFPlanner:
    """Artificial Potential Field 경로 계획"""
    
    def __init__(self, k_att=APF_ATTRACT_GAIN, k_rep=APF_REPULSE_GAIN, 
                 d_inf=APF_INFLUENCE_DISTANCE):
        self.k_att = k_att  # 인력 게인
        self.k_rep = k_rep  # 척력 게인
        self.d_inf = d_inf  # 척력 영향 거리
    
    def compute_force(self, current_pos, goal_pos, obstacles):
        """
        현재 위치에서의 합력 계산
        
        Args:
            current_pos: (x, y) 현재 위치
            goal_pos: (x, y) 목표 위치
            obstacles: 장애물 리스트 [(x, y), ...]
        
        Returns:
            (fx, fy): 합력 벡터
        """
        # 인력 (목표로 끌어당김)
        f_att = self._attractive_force(current_pos, goal_pos)
        
        # 척력 (장애물이 밀어냄)
        f_rep = self._repulsive_force(current_pos, obstacles)
        
        # 합력
        fx = f_att[0] + f_rep[0]
        fy = f_att[1] + f_rep[1]
        
        return fx, fy
    
    def _attractive_force(self, current_pos, goal_pos):
        """인력 계산 (목표를 향함)"""
        dx = goal_pos[0] - current_pos[0]
        dy = goal_pos[1] - current_pos[1]
        dist = math.sqrt(dx * dx + dy * dy)
        
        if dist < 1:
            return (0, 0)
        
        # 정규화된 방향 * 게인
        fx = self.k_att * dx / dist
        fy = self.k_att * dy / dist
        
        return fx, fy
    
    def _repulsive_force(self, current_pos, obstacles):
        """척력 계산 (장애물로부터 멀어짐)"""
        fx_total = 0
        fy_total = 0
        
        for obs in obstacles:
            dx = current_pos[0] - obs[0]
            dy = current_pos[1] - obs[1]
            dist = math.sqrt(dx * dx + dy * dy)
            
            # 영향 범위 밖이면 무시
            if dist > self.d_inf or dist < 1:
                continue
            
            # 척력 (거리에 반비례)
            force_magnitude = self.k_rep * (1.0 / dist - 1.0 / self.d_inf) * (1.0 / (dist * dist))
            
            # 방향 (장애물 반대편)
            fx_total += force_magnitude * dx / dist
            fy_total += force_magnitude * dy / dist
        
        return fx_total, fy_total
    
    def plan_step_grid(self, current_grid, goal_grid, grid_map):
        """
        그리드 기반 한 스텝 계획
        
        Args:
            current_grid: (gx, gy) 현재 그리드 위치
            goal_grid: (gx, gy) 목표 그리드 위치
            grid_map: 2D numpy array
        
        Returns:
            (gx, gy): 다음 그리드 위치
        """
        # 그리드 → 월드 좌표
        current_pos = (current_grid[0] * TILE_SIZE + TILE_SIZE/2, 
                      current_grid[1] * TILE_SIZE + TILE_SIZE/2)
        goal_pos = (goal_grid[0] * TILE_SIZE + TILE_SIZE/2,
                   goal_grid[1] * TILE_SIZE + TILE_SIZE/2)
        
        # 주변 장애물 수집
        obstacles = self._get_nearby_obstacles(current_grid, grid_map)
        
        # 합력 계산
        fx, fy = self.compute_force(current_pos, goal_pos, obstacles)
        
        # 힘의 크기 확인
        force_mag = math.sqrt(fx * fx + fy * fy)
        
        if force_mag < 0.01:  # 로컬 미니멈 (힘이 거의 0)
            # 랜덤 워크로 탈출 시도
            import random
            neighbors = self._get_walkable_neighbors(current_grid, grid_map)
            if neighbors:
                return random.choice(neighbors)
            return current_grid
        
        # 힘 방향으로 이동할 그리드 결정
        next_x = current_pos[0] + fx * TILE_SIZE * 0.5
        next_y = current_pos[1] + fy * TILE_SIZE * 0.5
        
        next_gx = int(next_x // TILE_SIZE)
        next_gy = int(next_y // TILE_SIZE)
        
        # 유효성 검사
        if is_walkable(grid_map, next_gx, next_gy):
            return (next_gx, next_gy)
        
        # 벽에 막혔으면 현재 위치 유지 (또는 대체 경로)
        return current_grid
    
    def _get_nearby_obstacles(self, center_grid, grid_map, radius=5):
        """주변 장애물 수집"""
        obstacles = []
        gx, gy = center_grid
        
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                nx, ny = gx + dx, gy + dy
                
                if is_valid_grid(nx, ny) and not is_walkable(grid_map, nx, ny):
                    # 장애물의 월드 좌표
                    ox = nx * TILE_SIZE + TILE_SIZE / 2
                    oy = ny * TILE_SIZE + TILE_SIZE / 2
                    obstacles.append((ox, oy))
        
        return obstacles
    
    def _get_walkable_neighbors(self, grid_pos, grid_map):
        """이동 가능한 인접 타일"""
        gx, gy = grid_pos
        neighbors = []
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1),
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            nx, ny = gx + dx, gy + dy
            if is_walkable(grid_map, nx, ny):
                neighbors.append((nx, ny))
        
        return neighbors
    
    def detect_local_minimum(self, force_history, threshold=0.1, window=5):
        """
        로컬 미니멈 감지
        
        Args:
            force_history: 최근 힘의 크기 리스트
            threshold: 임계값
            window: 확인할 프레임 수
        
        Returns:
            bool: 로컬 미니멈 여부
        """
        if len(force_history) < window:
            return False
        
        recent_forces = force_history[-window:]
        avg_force = sum(recent_forces) / window
        
        return avg_force < threshold
