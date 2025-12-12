"""
적 기반 클래스 및 공통 인터페이스
"""

import pygame
import math
from config import TILE_SIZE
from game.grid import world_to_grid, distance_world


class EnemyBase:
    """모든 적의 기반 클래스"""
    
    def __init__(self, x, y, speed, color, name="Enemy"):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.name = name
        self.radius = 10
        
        # 경로 관리
        self.path = []  # 그리드 좌표 리스트
        self.path_index = 0
        self.path_update_timer = 0
        self.path_update_interval = 0.5  # 경로 재계산 간격
        
        # 상태
        self.is_active = True
        self.stuck_timer = 0
        self.stuck_threshold = 2.0
        self.last_pos = (x, y)
        
        # 통계
        self.distance_traveled = 0
    
    def update(self, dt, player, level):
        """적 업데이트 (자식 클래스에서 구현)"""
        raise NotImplementedError
    
    def move_along_path(self, dt, level):
        """경로를 따라 이동"""
        if not self.path or self.path_index >= len(self.path):
            return False
        
        # 현재 목표 지점
        target_gx, target_gy = self.path[self.path_index]
        target_x = target_gx * TILE_SIZE + TILE_SIZE / 2
        target_y = target_gy * TILE_SIZE + TILE_SIZE / 2
        
        # 목표까지의 방향과 거리
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.sqrt(dx * dx + dy * dy)
        
        if dist < 5:  # 목표 도달
            self.path_index += 1
            return True
        
        # 이동
        move_dist = self.speed * dt
        if move_dist > dist:
            move_dist = dist
        
        # 새 위치 계산
        new_x = self.x + (dx / dist) * move_dist
        new_y = self.y + (dy / dist) * move_dist
        
        # 벽 충돌 검사
        new_gx = int(new_x / TILE_SIZE)
        new_gy = int(new_y / TILE_SIZE)
        
        from game.grid import is_walkable
        if is_walkable(level.grid_map, new_gx, new_gy):
            self.x = new_x
            self.y = new_y
            self.distance_traveled += move_dist
        else:
            # 벽에 막히면 경로 재계획
            self.path = []
            self.path_index = 0
        
        return True
    
    def move_towards(self, target_x, target_y, dt, level=None):
        """목표 지점을 향해 직접 이동"""
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.sqrt(dx * dx + dy * dy)
        
        if dist < 1:
            return
        
        move_dist = self.speed * dt
        if move_dist > dist:
            move_dist = dist
        
        # 새 위치 계산
        new_x = self.x + (dx / dist) * move_dist
        new_y = self.y + (dy / dist) * move_dist
        
        # 벽 충돌 검사 (만약 level이 제공되면)
        if level is not None:
            new_gx = int(new_x / TILE_SIZE)
            new_gy = int(new_y / TILE_SIZE)
            
            from game.grid import is_walkable
            if is_walkable(level.grid_map, new_gx, new_gy):
                self.x = new_x
                self.y = new_y
                self.distance_traveled += move_dist
        else:
            # level이 없으면 기존 방식대로
            self.x = new_x
            self.y = new_y
            self.distance_traveled += move_dist
    
    def check_stuck(self, dt):
        """제자리에 갇혔는지 확인"""
        current_pos = (self.x, self.y)
        dist_moved = distance_world(current_pos, self.last_pos)
        
        if dist_moved < 1:  # 거의 움직이지 않음
            self.stuck_timer += dt
        else:
            self.stuck_timer = 0
        
        self.last_pos = current_pos
        return self.stuck_timer > self.stuck_threshold
    
    def collides_with(self, player):
        """플레이어와 충돌 체크"""
        dist = distance_world((self.x, self.y), (player.x, player.y))
        return dist < self.radius + player.radius
    
    def draw(self, surface, camera_offset=(0, 0)):
        """적 그리기"""
        ox, oy = camera_offset
        screen_x = int(self.x - ox)
        screen_y = int(self.y - oy)
        
        # 적 원
        pygame.draw.circle(surface, self.color, (screen_x, screen_y), self.radius)
        
        # 테두리
        pygame.draw.circle(surface, (255, 255, 255), (screen_x, screen_y), self.radius, 1)
        
        # 이름과 상태 표시 (디버그용)
        font = pygame.font.Font(None, 16)
        
        # 이름 표시
        text = font.render(self.name, True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen_x, screen_y - self.radius - 20))
        surface.blit(text, text_rect)
        
        # Bug 알고리즘 상태 표시
        if hasattr(self, 'planner') and hasattr(self.planner, 'state'):
            state_text = font.render(self.planner.state, True, (255, 255, 0))
            state_rect = state_text.get_rect(center=(screen_x, screen_y - self.radius - 5))
            surface.blit(state_text, state_rect)
    
    def draw_path(self, surface, camera_offset=(0, 0)):
        """경로 그리기 (디버그용)"""
        if not self.path or len(self.path) < 2:
            return
        
        ox, oy = camera_offset
        
        for i in range(len(self.path) - 1):
            gx1, gy1 = self.path[i]
            gx2, gy2 = self.path[i + 1]
            
            x1 = gx1 * TILE_SIZE + TILE_SIZE / 2 - ox
            y1 = gy1 * TILE_SIZE + TILE_SIZE / 2 - oy
            x2 = gx2 * TILE_SIZE + TILE_SIZE / 2 - ox
            y2 = gy2 * TILE_SIZE + TILE_SIZE / 2 - oy
            
            pygame.draw.line(surface, self.color, (x1, y1), (x2, y2), 1)
