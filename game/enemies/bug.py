"""
Bug 알고리즘 기반 적들
"""

from game.enemies import EnemyBase
from algos.bug import Bug1Planner, Bug2Planner, TangentBugPlanner
from game.grid import world_to_grid
from config import (
    ENEMY_BUG1_SPEED, ENEMY_BUG2_SPEED, ENEMY_TANGENT_SPEED,
    COLOR_BUG1, COLOR_BUG2, COLOR_TANGENT
)


class Bug1Enemy(EnemyBase):
    """Bug1 알고리즘 적"""
    
    def __init__(self, x, y):
        super().__init__(x, y, ENEMY_BUG1_SPEED, COLOR_BUG1, "Bug1")
        self.planner = Bug1Planner()
        self.current_grid = world_to_grid(x, y)
        self.last_grid = None
    
    def update(self, dt, player, level):
        """업데이트"""
        # 현재 그리드 위치
        current_grid = world_to_grid(self.x, self.y)
        
        # 그리드 위치가 바뀌었을 때만 다음 스텝 계획
        if current_grid != self.last_grid:
            self.last_grid = current_grid
            
            goal_grid = world_to_grid(player.x, player.y)
            
            # Bug1 한 스텝 - 상태를 유지하며 다음 그리드 계산
            next_grid = self.planner.plan_step(current_grid, goal_grid, level.grid_map)
            
            # 다음 목표 설정
            if next_grid != current_grid:
                self.path = [next_grid]
                self.path_index = 0
        
        # 경로 따라 이동
        if self.path:
            self.move_along_path(dt, level)
        else:
            # 경로가 없으면 플레이어를 향해 직접 이동
            self.move_towards(player.x, player.y, dt, level)
    
    def draw(self, surface, camera_offset=(0, 0)):
        """Bug1 적 그리기 (상태 시각화)"""
        super().draw(surface, camera_offset)
        
        import pygame
        from config import TILE_SIZE
        ox, oy = camera_offset
        
        # Hit point 표시 (빨간색)
        if self.planner.hit_point:
            gx, gy = self.planner.hit_point
            x = int(gx * TILE_SIZE + TILE_SIZE / 2 - ox)
            y = int(gy * TILE_SIZE + TILE_SIZE / 2 - oy)
            pygame.draw.circle(surface, (255, 0, 0), (x, y), 5)
        
        # Leave point 표시 (녹색)
        if self.planner.leave_point:
            gx, gy = self.planner.leave_point
            x = int(gx * TILE_SIZE + TILE_SIZE / 2 - ox)
            y = int(gy * TILE_SIZE + TILE_SIZE / 2 - oy)
            pygame.draw.circle(surface, (0, 255, 0), (x, y), 5)
        
        # Wall points 표시 (노란색 선)
        if len(self.planner.wall_points) > 1:
            points = []
            for gx, gy in self.planner.wall_points:
                x = int(gx * TILE_SIZE + TILE_SIZE / 2 - ox)
                y = int(gy * TILE_SIZE + TILE_SIZE / 2 - oy)
                points.append((x, y))
            if len(points) > 1:
                pygame.draw.lines(surface, (255, 255, 0), False, points, 1)


class Bug2Enemy(EnemyBase):
    """Bug2 알고리즘 적"""
    
    def __init__(self, x, y):
        super().__init__(x, y, ENEMY_BUG2_SPEED, COLOR_BUG2, "Bug2")
        self.planner = Bug2Planner()
        self.start_grid = world_to_grid(x, y)
        self.last_grid = None
    
    def update(self, dt, player, level):
        """업데이트"""
        # 현재 그리드 위치
        current_grid = world_to_grid(self.x, self.y)
        
        # 그리드 위치가 바뀌었을 때만 다음 스텝 계획
        if current_grid != self.last_grid:
            self.last_grid = current_grid
            
            goal_grid = world_to_grid(player.x, player.y)
            
            # Bug2 한 스텝 - M-line 상태 유지
            next_grid = self.planner.plan_step(
                current_grid, goal_grid, level.grid_map, self.start_grid
            )
            
            if next_grid != current_grid:
                self.path = [next_grid]
                self.path_index = 0
        
        if self.path:
            self.move_along_path(dt, level)
        else:
            self.move_towards(player.x, player.y, dt, level)
    
    def draw(self, surface, camera_offset=(0, 0)):
        """Bug2 적 그리기 (M-line 시각화)"""
        super().draw(surface, camera_offset)
        
        import pygame
        from config import TILE_SIZE
        ox, oy = camera_offset
        
        # M-line 표시 (시작점과 목표 사이의 선)
        if self.planner.start_pos and self.planner.goal_pos:
            sx, sy = self.planner.start_pos
            gx, gy = self.planner.goal_pos
            x1 = int(sx * TILE_SIZE + TILE_SIZE / 2 - ox)
            y1 = int(sy * TILE_SIZE + TILE_SIZE / 2 - oy)
            x2 = int(gx * TILE_SIZE + TILE_SIZE / 2 - ox)
            y2 = int(gy * TILE_SIZE + TILE_SIZE / 2 - oy)
            pygame.draw.line(surface, (0, 255, 255), (x1, y1), (x2, y2), 1)
        
        # Hit point 표시
        if self.planner.hit_point:
            gx, gy = self.planner.hit_point
            x = int(gx * TILE_SIZE + TILE_SIZE / 2 - ox)
            y = int(gy * TILE_SIZE + TILE_SIZE / 2 - oy)
            pygame.draw.circle(surface, (255, 0, 0), (x, y), 5)


class TangentBugEnemy(EnemyBase):
    """Tangent Bug 알고리즘 적"""
    
    def __init__(self, x, y):
        super().__init__(x, y, ENEMY_TANGENT_SPEED, COLOR_TANGENT, "Tangent")
        self.planner = TangentBugPlanner()
        self.last_grid = None
    
    def update(self, dt, player, level):
        """업데이트"""
        # 현재 그리드 위치
        current_grid = world_to_grid(self.x, self.y)
        
        # 그리드 위치가 바뀌었을 때만 다음 스텝 계획
        if current_grid != self.last_grid:
            self.last_grid = current_grid
            
            goal_grid = world_to_grid(player.x, player.y)
            
            # Tangent Bug 한 스텝 - 센서 기반 접선 탐색
            next_grid = self.planner.plan_step(current_grid, goal_grid, level.grid_map)
            
            if next_grid != current_grid:
                self.path = [next_grid]
                self.path_index = 0
        
        if self.path:
            self.move_along_path(dt, level)
        else:
            self.move_towards(player.x, player.y, dt, level)
    
    def draw(self, surface, camera_offset=(0, 0)):
        """Tangent Bug 적 그리기 (센서 범위 시각화)"""
        super().draw(surface, camera_offset)
        
        import pygame
        from config import TILE_SIZE
        ox, oy = camera_offset
        
        # 센서 범위 표시 (원)
        screen_x = int(self.x - ox)
        screen_y = int(self.y - oy)
        sensor_range = self.planner.sensor_range * TILE_SIZE
        pygame.draw.circle(surface, (100, 100, 255), (screen_x, screen_y), int(sensor_range), 1)
        
        # Tangent point 표시
        if self.planner.tangent_point:
            gx, gy = self.planner.tangent_point
            x = int(gx * TILE_SIZE + TILE_SIZE / 2 - ox)
            y = int(gy * TILE_SIZE + TILE_SIZE / 2 - oy)
            pygame.draw.circle(surface, (255, 0, 255), (x, y), 5)
