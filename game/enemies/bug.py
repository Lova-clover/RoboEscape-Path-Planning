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
    
    def update(self, dt, player, level):
        """업데이트"""
        self.path_update_timer += dt
        
        # 주기적으로 경로 재계산
        if self.path_update_timer >= self.path_update_interval:
            self.path_update_timer = 0
            
            # 현재 위치와 목표 위치 (그리드)
            current_grid = world_to_grid(self.x, self.y)
            goal_grid = world_to_grid(player.x, player.y)
            
            # Bug1 한 스텝
            next_grid = self.planner.plan_step(current_grid, goal_grid, level.grid_map)
            
            # 경로 설정
            if next_grid != current_grid:
                self.path = [next_grid]
                self.path_index = 0
        
        # 경로 따라 이동
        if self.path:
            self.move_along_path(dt, level)
        else:
            # 경로가 없으면 플레이어를 향해 직접 이동
            self.move_towards(player.x, player.y, dt)


class Bug2Enemy(EnemyBase):
    """Bug2 알고리즘 적"""
    
    def __init__(self, x, y):
        super().__init__(x, y, ENEMY_BUG2_SPEED, COLOR_BUG2, "Bug2")
        self.planner = Bug2Planner()
        self.start_grid = world_to_grid(x, y)
    
    def update(self, dt, player, level):
        """업데이트"""
        self.path_update_timer += dt
        
        if self.path_update_timer >= self.path_update_interval:
            self.path_update_timer = 0
            
            current_grid = world_to_grid(self.x, self.y)
            goal_grid = world_to_grid(player.x, player.y)
            
            # Bug2 한 스텝
            next_grid = self.planner.plan_step(
                current_grid, goal_grid, level.grid_map, self.start_grid
            )
            
            if next_grid != current_grid:
                self.path = [next_grid]
                self.path_index = 0
        
        if self.path:
            self.move_along_path(dt, level)
        else:
            self.move_towards(player.x, player.y, dt)


class TangentBugEnemy(EnemyBase):
    """Tangent Bug 알고리즘 적"""
    
    def __init__(self, x, y):
        super().__init__(x, y, ENEMY_TANGENT_SPEED, COLOR_TANGENT, "TangentBug")
        self.planner = TangentBugPlanner(sensor_range=12)
    
    def update(self, dt, player, level):
        """업데이트"""
        self.path_update_timer += dt
        
        if self.path_update_timer >= self.path_update_interval * 0.7:  # 더 빠른 재계산
            self.path_update_timer = 0
            
            current_grid = world_to_grid(self.x, self.y)
            goal_grid = world_to_grid(player.x, player.y)
            
            # Tangent Bug 한 스텝
            next_grid = self.planner.plan_step(current_grid, goal_grid, level.grid_map)
            
            if next_grid != current_grid:
                self.path = [next_grid]
                self.path_index = 0
        
        if self.path:
            self.move_along_path(dt, level)
        else:
            self.move_towards(player.x, player.y, dt)
