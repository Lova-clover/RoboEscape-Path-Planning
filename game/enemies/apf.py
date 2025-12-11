"""
APF 알고리즘 기반 적
"""

import math
from game.enemies import EnemyBase
from algos.apf import APFPlanner
from game.grid import world_to_grid
from config import ENEMY_APF_SPEED, COLOR_APF


class APFEnemy(EnemyBase):
    """Artificial Potential Field 적"""
    
    def __init__(self, x, y):
        super().__init__(x, y, ENEMY_APF_SPEED, COLOR_APF, "APF")
        self.planner = APFPlanner(
            k_att=1.5,
            k_rep=150.0,
            d_inf=60.0
        )
        
        # 로컬 미니멈 감지
        self.force_history = []
        self.stuck_in_minimum = False
        self.minimum_escape_timer = 0
        self.escape_direction = None
    
    def update(self, dt, player, level):
        """업데이트"""
        self.path_update_timer += dt
        
        # 로컬 미니멈 탈출 모드
        if self.stuck_in_minimum:
            self.minimum_escape_timer -= dt
            if self.minimum_escape_timer <= 0:
                self.stuck_in_minimum = False
                self.escape_direction = None
            else:
                # 랜덤 방향으로 이동
                if self.escape_direction:
                    self.move_towards(
                        self.x + self.escape_direction[0] * 100,
                        self.y + self.escape_direction[1] * 100,
                        dt
                    )
                return
        
        # 주기적으로 힘 계산
        if self.path_update_timer >= self.path_update_interval * 0.3:  # APF는 더 자주 업데이트
            self.path_update_timer = 0
            
            current_grid = world_to_grid(self.x, self.y)
            goal_grid = world_to_grid(player.x, player.y)
            
            # APF 힘 계산
            next_grid = self.planner.plan_step_grid(current_grid, goal_grid, level.grid_map)
            
            # 힘의 크기 기록 (로컬 미니멈 감지용)
            fx, fy = self.planner.compute_force(
                (self.x, self.y),
                (player.x, player.y),
                self.planner._get_nearby_obstacles(current_grid, level.grid_map)
            )
            force_mag = math.sqrt(fx * fx + fy * fy)
            self.force_history.append(force_mag)
            
            # 히스토리 크기 제한
            if len(self.force_history) > 20:
                self.force_history.pop(0)
            
            # 로컬 미니멈 체크
            if self.planner.detect_local_minimum(self.force_history, threshold=0.3, window=10):
                if not self.stuck_in_minimum:
                    self.stuck_in_minimum = True
                    self.minimum_escape_timer = 1.5  # 1.5초 동안 탈출 시도
                    
                    # 랜덤 탈출 방향
                    import random
                    angle = random.uniform(0, 2 * math.pi)
                    self.escape_direction = (math.cos(angle), math.sin(angle))
            
            # 경로 설정
            if next_grid != current_grid:
                self.path = [next_grid]
                self.path_index = 0
        
        # 경로 따라 이동
        if self.path:
            self.move_along_path(dt, level)
        else:
            # 직접 이동
            self.move_towards(player.x, player.y, dt)
