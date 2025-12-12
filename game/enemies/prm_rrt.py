"""
PRM, RRT 알고리즘 기반 적들
"""

from game.enemies import EnemyBase
from algos.prm import PRMPlanner
from algos.rrt import RRTPlanner
from game.grid import world_to_grid
from config import (
    ENEMY_PRM_SPEED, ENEMY_RRT_SPEED,
    COLOR_PRM, COLOR_RRT
)


class PRMEnemy(EnemyBase):
    """PRM (Probabilistic Roadmap) 적"""
    
    def __init__(self, x, y, grid_map):
        super().__init__(x, y, ENEMY_PRM_SPEED, COLOR_PRM, "PRM")
        self.planner = PRMPlanner(num_samples=120, connection_radius=10.0, max_neighbors=6)
        
        # 로드맵 사전 구축
        self.planner.build_roadmap(grid_map)
        
        # 경로 재계산 간격 (PRM은 덜 자주)
        self.path_update_interval = 1.5
        
        # 시각화 데이터
        self.show_graph = True
        self.state = 'planning'  # 상태 표시용
        
        # 맵 변경 감지용
        self.last_temp_wall_count = 0
    
    def update(self, dt, player, level):
        """업데이트"""
        self.path_update_timer += dt
        
        # 맵이 변경되면 (임시 벽 추가 등) 로드맵 재구축
        if not self.planner.is_built or self.check_map_changed(level):
            self.planner.build_roadmap(level.grid_map)
            self.path = []
        
        # 주기적으로 경로 재계산
        if self.path_update_timer >= self.path_update_interval or not self.path:
            self.path_update_timer = 0
            
            current_grid = world_to_grid(self.x, self.y)
            goal_grid = world_to_grid(player.x, player.y)
            
            # PRM 경로 계획
            full_path = self.planner.plan_path(current_grid, goal_grid, level.grid_map)
            
            if full_path and len(full_path) > 1:
                self.path = full_path[1:]  # 현재 위치 제외
                self.path_index = 0
        
        # 경로 따라 이동
        if self.path:
            self.move_along_path(dt, level)
        else:
            # 경로 없으면 직접 이동
            self.move_towards(player.x, player.y, dt, level)
    
    def check_map_changed(self, level):
        """맵 변경 감지"""
        # 임시 벽 개수가 변경되면 재구축
        current_count = len(level.temp_walls)
        if current_count != self.last_temp_wall_count:
            self.last_temp_wall_count = current_count
            return True
        return False
    
    def draw(self, surface, camera_offset=(0, 0)):
        """PRM 그래프 포함 그리기"""
        # 그래프 먼저 그리기
        if self.show_graph and hasattr(self.planner, 'is_built') and self.planner.is_built:
            self.draw_prm_graph(surface, camera_offset)
        
        # 적 그리기
        super().draw(surface, camera_offset)
    
    def draw_prm_graph(self, surface, camera_offset=(0, 0)):
        """PRM 그래프 시각화 (부드럽게)"""
        import pygame
        from config import TILE_SIZE
        
        ox, oy = camera_offset
        nodes, edges = self.planner.get_graph_for_visualization()
        
        # 엣지 그리기 (어두운 회색, 낮은 투명도)
        for node1, node2 in edges:
            x1 = node1[0] * TILE_SIZE + TILE_SIZE / 2 - ox
            y1 = node1[1] * TILE_SIZE + TILE_SIZE / 2 - oy
            x2 = node2[0] * TILE_SIZE + TILE_SIZE / 2 - ox
            y2 = node2[1] * TILE_SIZE + TILE_SIZE / 2 - oy
            
            pygame.draw.line(surface, (80, 80, 80, 40), (x1, y1), (x2, y2), 1)
        
        # 노드 그리기 (작고 어둡게)
        for node in nodes:
            x = node[0] * TILE_SIZE + TILE_SIZE / 2 - ox
            y = node[1] * TILE_SIZE + TILE_SIZE / 2 - oy
            pygame.draw.circle(surface, (100, 100, 100, 60), (int(x), int(y)), 1)


class RRTEnemy(EnemyBase):
    """RRT (Rapidly-exploring Random Tree) 적"""
    
    def __init__(self, x, y):
        super().__init__(x, y, ENEMY_RRT_SPEED, COLOR_RRT, "RRT")
        self.planner = RRTPlanner(max_iterations=300, step_size=2.5, goal_sample_rate=0.2)
        
        # 경로 재계산 간격 (RRT는 자주 재계산)
        self.path_update_interval = 0.8
        
        # 시각화 데이터
        self.show_tree = True
        
        # 맵 변경 감지용
        self.last_temp_wall_count = 0
    
    def update(self, dt, player, level):
        """업데이트"""
        self.path_update_timer += dt
        
        # 맵이 변경되면 즉시 재계획
        current_count = len(level.temp_walls)
        if current_count != self.last_temp_wall_count:
            self.last_temp_wall_count = current_count
            self.path_update_timer = self.path_update_interval  # 즉시 재계획
        
        # 자주 경로 재계산 (RRT는 매번 새로운 트리)
        if self.path_update_timer >= self.path_update_interval:
            self.path_update_timer = 0
            
            current_grid = world_to_grid(self.x, self.y)
            goal_grid = world_to_grid(player.x, player.y)
            
            # RRT 경로 계획
            full_path = self.planner.plan_path(current_grid, goal_grid, level.grid_map)
            
            if full_path and len(full_path) > 1:
                self.path = full_path[1:]  # 현재 위치 제외
                self.path_index = 0
        
        # 경로 따라 이동
        if self.path:
            self.move_along_path(dt, level)
        else:
            # 경로 없으면 직접 이동
            self.move_towards(player.x, player.y, dt, level)
    
    def draw(self, surface, camera_offset=(0, 0)):
        """RRT 트리 포함 그리기"""
        # 트리 먼저 그리기
        if self.show_tree and hasattr(self.planner, 'nodes') and len(self.planner.nodes) > 0:
            self.draw_rrt_tree(surface, camera_offset)
        
        # 적 그리기
        super().draw(surface, camera_offset)
    
    def draw_rrt_tree(self, surface, camera_offset=(0, 0)):
        """RRT 트리 시각화 (부드럽게)"""
        import pygame
        from config import TILE_SIZE
        
        ox, oy = camera_offset
        nodes, edges = self.planner.get_tree_for_visualization()
        
        # 엣지 그리기 (어두운 회색, 낮은 투명도)
        for node1, node2 in edges:
            x1 = node1[0] * TILE_SIZE + TILE_SIZE / 2 - ox
            y1 = node1[1] * TILE_SIZE + TILE_SIZE / 2 - oy
            x2 = node2[0] * TILE_SIZE + TILE_SIZE / 2 - ox
            y2 = node2[1] * TILE_SIZE + TILE_SIZE / 2 - oy
            
            pygame.draw.line(surface, (70, 70, 70, 35), (x1, y1), (x2, y2), 1)
        
        # 노드 그리기 (작고 어둡게)
        for node in nodes:
            x = node[0] * TILE_SIZE + TILE_SIZE / 2 - ox
            y = node[1] * TILE_SIZE + TILE_SIZE / 2 - oy
            pygame.draw.circle(surface, (90, 90, 90, 50), (int(x), int(y)), 1)
