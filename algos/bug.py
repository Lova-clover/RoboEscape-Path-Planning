"""
Bug 알고리즘 (Bug1, Bug2, Tangent Bug)
"""

import math
import numpy as np
from game.grid import is_walkable, line_of_sight, get_neighbors


class Bug1Planner:
    """Bug1 알고리즘"""
    
    def __init__(self):
        self.state = 'go_to_goal'  # 'go_to_goal', 'follow_wall', 'leave_wall'
        self.hit_point = None
        self.leave_point = None
        self.wall_points = []
        self.circumnavigate_complete = False
        self.min_distance = float('inf')
    
    def plan_step(self, current_pos, goal_pos, grid_map):
        """한 스텝 계획"""
        gx, gy = current_pos
        goal_gx, goal_gy = goal_pos
        
        # 목표 도달
        if (gx, gy) == (goal_gx, goal_gy):
            return current_pos
        
        # Go to goal 상태
        if self.state == 'go_to_goal':
            # 목표로 직진 시도
            next_pos = self._move_towards(current_pos, goal_pos)
            
            # 장애물 만남
            if not is_walkable(grid_map, next_pos[0], next_pos[1]):
                self.state = 'follow_wall'
                self.hit_point = current_pos
                self.wall_points = []
                self.min_distance = self._distance(current_pos, goal_pos)
                self.circumnavigate_complete = False
                return self._follow_wall(current_pos, goal_pos, grid_map)
            
            return next_pos
        
        # Follow wall 상태
        elif self.state == 'follow_wall':
            current_dist = self._distance(current_pos, goal_pos)
            
            # 최소 거리 업데이트
            if current_dist < self.min_distance:
                self.min_distance = current_dist
                self.leave_point = current_pos
            
            # 한 바퀴 돌았는지 확인
            if len(self.wall_points) > 5 and self._distance(current_pos, self.hit_point) < 2:
                self.circumnavigate_complete = True
                if self.leave_point:
                    self.state = 'leave_wall'
                    return self.leave_point
            
            self.wall_points.append(current_pos)
            return self._follow_wall(current_pos, goal_pos, grid_map)
        
        # Leave wall 상태
        elif self.state == 'leave_wall':
            # 벽에서 벗어남
            if line_of_sight(grid_map, current_pos, goal_pos):
                self.state = 'go_to_goal'
                self.hit_point = None
                self.leave_point = None
                self.wall_points = []
            
            return self._move_towards(current_pos, goal_pos)
        
        return current_pos
    
    def _move_towards(self, current, goal):
        """목표를 향해 한 칸 이동"""
        dx = goal[0] - current[0]
        dy = goal[1] - current[1]
        
        # 정규화 및 한 칸 이동
        if abs(dx) > abs(dy):
            return (current[0] + (1 if dx > 0 else -1), current[1])
        elif dy != 0:
            return (current[0], current[1] + (1 if dy > 0 else -1))
        else:
            return current
    
    def _follow_wall(self, current_pos, goal_pos, grid_map):
        """벽을 따라 이동 (왼손 법칙)"""
        # 현재 위치에서 목표 방향
        goal_dir = math.atan2(goal_pos[1] - current_pos[1], goal_pos[0] - current_pos[0])
        
        # 8방향 탐색
        neighbors = get_neighbors(current_pos[0], current_pos[1], grid_map, diagonal=True)
        
        if not neighbors:
            return current_pos
        
        # 목표 방향과 가장 유사한 방향 선택
        best_neighbor = min(neighbors, key=lambda n: abs(
            math.atan2(n[1] - current_pos[1], n[0] - current_pos[0]) - goal_dir
        ))
        
        return best_neighbor
    
    def _distance(self, p1, p2):
        """유클리드 거리"""
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


class Bug2Planner:
    """Bug2 알고리즘 - M-line 기반"""
    
    def __init__(self):
        self.state = 'go_to_goal'  # 'go_to_goal', 'follow_wall'
        self.m_line = None  # (start, goal)
        self.hit_point = None
    
    def plan_step(self, current_pos, goal_pos, grid_map, start_pos=None):
        """한 스텝 계획"""
        if start_pos is None:
            start_pos = current_pos
        
        gx, gy = current_pos
        goal_gx, goal_gy = goal_pos
        
        # M-line 설정
        if self.m_line is None:
            self.m_line = (start_pos, goal_pos)
        
        # 목표 도달
        if (gx, gy) == (goal_gx, goal_gy):
            return current_pos
        
        # Go to goal 상태
        if self.state == 'go_to_goal':
            next_pos = self._move_towards(current_pos, goal_pos)
            
            # 장애물 만남
            if not is_walkable(grid_map, next_pos[0], next_pos[1]):
                self.state = 'follow_wall'
                self.hit_point = current_pos
                return self._follow_wall(current_pos, goal_pos, grid_map)
            
            return next_pos
        
        # Follow wall 상태
        elif self.state == 'follow_wall':
            # M-line에 도달하고 hit point보다 목표에 가까운가?
            if self._on_m_line(current_pos) and \
               self._distance(current_pos, goal_pos) < self._distance(self.hit_point, goal_pos):
                self.state = 'go_to_goal'
                self.hit_point = None
                return self._move_towards(current_pos, goal_pos)
            
            return self._follow_wall(current_pos, goal_pos, grid_map)
        
        return current_pos
    
    def _move_towards(self, current, goal):
        """목표를 향해 한 칸 이동"""
        dx = goal[0] - current[0]
        dy = goal[1] - current[1]
        
        if abs(dx) > abs(dy):
            return (current[0] + (1 if dx > 0 else -1), current[1])
        elif dy != 0:
            return (current[0], current[1] + (1 if dy > 0 else -1))
        else:
            return current
    
    def _follow_wall(self, current_pos, goal_pos, grid_map):
        """벽을 따라 이동"""
        neighbors = get_neighbors(current_pos[0], current_pos[1], grid_map, diagonal=True)
        
        if not neighbors:
            return current_pos
        
        # M-line 방향 우선
        best_neighbor = min(neighbors, key=lambda n: 
            self._distance_to_m_line(n) + self._distance(n, goal_pos) * 0.1
        )
        
        return best_neighbor
    
    def _on_m_line(self, pos, threshold=1.5):
        """M-line 위에 있는지 확인"""
        if self.m_line is None:
            return False
        
        return self._distance_to_m_line(pos) < threshold
    
    def _distance_to_m_line(self, pos):
        """M-line까지의 거리"""
        if self.m_line is None:
            return float('inf')
        
        start, goal = self.m_line
        
        # 점에서 직선까지의 거리
        x0, y0 = pos
        x1, y1 = start
        x2, y2 = goal
        
        num = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
        den = math.sqrt((y2 - y1)**2 + (x2 - x1)**2)
        
        if den == 0:
            return self._distance(pos, start)
        
        return num / den
    
    def _distance(self, p1, p2):
        """유클리드 거리"""
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


class TangentBugPlanner:
    """Tangent Bug 알고리즘 (간소화 버전)"""
    
    def __init__(self, sensor_range=10):
        self.state = 'go_to_goal'
        self.sensor_range = sensor_range
    
    def plan_step(self, current_pos, goal_pos, grid_map):
        """한 스텝 계획"""
        gx, gy = current_pos
        goal_gx, goal_gy = goal_pos
        
        # 목표 도달
        if (gx, gy) == (goal_gx, goal_gy):
            return current_pos
        
        # 목표까지 시야 확보되면 직진
        if line_of_sight(grid_map, current_pos, goal_pos):
            return self._move_towards(current_pos, goal_pos)
        
        # Tangent 포인트 찾기
        tangent_point = self._find_tangent_point(current_pos, goal_pos, grid_map)
        
        if tangent_point:
            return self._move_towards(current_pos, tangent_point)
        else:
            # Tangent 못 찾으면 일반 이동
            neighbors = get_neighbors(gx, gy, grid_map, diagonal=True)
            if neighbors:
                return min(neighbors, key=lambda n: self._distance(n, goal_pos))
            return current_pos
    
    def _find_tangent_point(self, current_pos, goal_pos, grid_map):
        """Tangent 포인트 찾기"""
        # 센서 범위 내의 장애물 모서리 탐색
        gx, gy = current_pos
        candidates = []
        
        for dy in range(-self.sensor_range, self.sensor_range + 1):
            for dx in range(-self.sensor_range, self.sensor_range + 1):
                nx, ny = gx + dx, gy + dy
                
                # 범위 체크
                if not is_walkable(grid_map, nx, ny):
                    # 장애물 주변의 빈 공간 찾기
                    for neighbor in get_neighbors(nx, ny, grid_map, diagonal=True):
                        if line_of_sight(grid_map, current_pos, neighbor):
                            candidates.append(neighbor)
        
        # 목표에 가장 가까운 후보 선택
        if candidates:
            return min(candidates, key=lambda p: self._distance(p, goal_pos))
        
        return None
    
    def _move_towards(self, current, goal):
        """목표를 향해 한 칸 이동"""
        dx = goal[0] - current[0]
        dy = goal[1] - current[1]
        
        if abs(dx) > abs(dy):
            return (current[0] + (1 if dx > 0 else -1), current[1])
        elif dy != 0:
            return (current[0], current[1] + (1 if dy > 0 else -1))
        else:
            return current
    
    def _distance(self, p1, p2):
        """유클리드 거리"""
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
