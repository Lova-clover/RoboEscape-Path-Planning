"""
플레이어 클래스
"""

import pygame
import math
from config import (
    PLAYER_SPEED, PLAYER_DASH_SPEED, PLAYER_DASH_DURATION, PLAYER_DASH_COOLDOWN,
    PLAYER_MAX_HEALTH, PLAYER_INVINCIBLE_TIME, COLOR_GREEN, COLOR_CYAN,
    SKILL_WALL_COOLDOWN, SKILL_NOISE_COOLDOWN, SKILL_SLOWMO_COOLDOWN,
    SKILL_WALL_DURATION, SKILL_NOISE_DURATION, SKILL_SLOWMO_DURATION
)
from game.grid import world_to_grid, check_collision_circle, get_rectangle_tiles


class Player:
    """플레이어 캐릭터"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 12
        self.health = PLAYER_MAX_HEALTH
        
        # 이동 상태
        self.vx = 0
        self.vy = 0
        self.is_dashing = False
        self.dash_time = 0
        self.dash_cooldown = 0
        self.dash_dir = (0, 0)
        
        # 무적 상태 (피격 후)
        self.invincible = False
        self.invincible_time = 0
        
        # 스킬 쿨타임
        self.wall_skill_cooldown = 0
        self.noise_skill_cooldown = 0
        self.slowmo_skill_cooldown = 0
        
        # 통계
        self.stats = {
            'distance_traveled': 0,
            'dodges': 0,
            'walls_placed': 0,
            'noise_used': 0
        }
    
    def handle_input(self, keys):
        """키보드 입력 처리"""
        if self.is_dashing:
            return  # 대시 중에는 입력 무시
        
        # 이동 방향 계산
        dx, dy = 0, 0
        if keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_s]:
            dy += 1
        if keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_d]:
            dx += 1
        
        # 정규화 (대각선 이동 속도 보정)
        if dx != 0 or dy != 0:
            length = math.sqrt(dx * dx + dy * dy)
            self.vx = dx / length
            self.vy = dy / length
        else:
            self.vx = 0
            self.vy = 0
    
    def try_dash(self):
        """대시 시도"""
        if self.dash_cooldown <= 0 and not self.is_dashing:
            if self.vx != 0 or self.vy != 0:
                self.is_dashing = True
                self.dash_time = PLAYER_DASH_DURATION
                self.dash_cooldown = PLAYER_DASH_COOLDOWN
                self.dash_dir = (self.vx, self.vy)
                self.stats['dodges'] += 1
                return True
        return False
    
    def try_wall_skill(self, level):
        """장벽 설치 스킬"""
        if self.wall_skill_cooldown <= 0:
            # 플레이어 앞쪽에 장벽 설치
            gx, gy = world_to_grid(self.x, self.y)
            
            # 이동 방향 기준으로 앞쪽 타일들
            if abs(self.vx) > abs(self.vy):
                # 좌우 이동
                offset_x = 2 if self.vx > 0 else -2
                tiles = [(gx + offset_x, gy), (gx + offset_x, gy - 1), (gx + offset_x, gy + 1)]
            else:
                # 상하 이동
                offset_y = 2 if self.vy > 0 else -2
                tiles = [(gx, gy + offset_y), (gx - 1, gy + offset_y), (gx + 1, gy + offset_y)]
            
            # 타일들에 장벽 설치
            placed = False
            for tx, ty in tiles:
                if level.add_temp_wall(tx, ty, SKILL_WALL_DURATION):
                    placed = True
            
            if placed:
                self.wall_skill_cooldown = SKILL_WALL_COOLDOWN
                self.stats['walls_placed'] += 1
                return True
        
        return False
    
    def try_noise_skill(self):
        """노이즈 폭탄 스킬"""
        if self.noise_skill_cooldown <= 0:
            self.noise_skill_cooldown = SKILL_NOISE_COOLDOWN
            self.stats['noise_used'] += 1
            return True
        return False
    
    def try_slowmo_skill(self):
        """슬로우 모션 스킬"""
        if self.slowmo_skill_cooldown <= 0:
            self.slowmo_skill_cooldown = SKILL_SLOWMO_COOLDOWN
            return True
        return False
    
    def update(self, dt, level):
        """플레이어 업데이트"""
        # 쿨타임 감소
        if self.dash_cooldown > 0:
            self.dash_cooldown -= dt
        if self.wall_skill_cooldown > 0:
            self.wall_skill_cooldown -= dt
        if self.noise_skill_cooldown > 0:
            self.noise_skill_cooldown -= dt
        if self.slowmo_skill_cooldown > 0:
            self.slowmo_skill_cooldown -= dt
        
        # 무적 시간 감소
        if self.invincible:
            self.invincible_time -= dt
            if self.invincible_time <= 0:
                self.invincible = False
        
        # 대시 처리
        if self.is_dashing:
            self.dash_time -= dt
            if self.dash_time <= 0:
                self.is_dashing = False
            
            # 대시 이동
            speed = PLAYER_DASH_SPEED
            vx, vy = self.dash_dir
        else:
            # 일반 이동
            speed = PLAYER_SPEED
            vx, vy = self.vx, self.vy
        
        # 이동 시도
        if vx != 0 or vy != 0:
            new_x = self.x + vx * speed * dt
            new_y = self.y + vy * speed * dt
            
            # 충돌 체크
            if not check_collision_circle(new_x, self.y, self.radius, level.grid_map):
                self.x = new_x
                self.stats['distance_traveled'] += abs(vx * speed * dt)
            
            if not check_collision_circle(self.x, new_y, self.radius, level.grid_map):
                self.y = new_y
                self.stats['distance_traveled'] += abs(vy * speed * dt)
    
    def take_damage(self):
        """피해 입기"""
        if not self.invincible:
            self.health -= 1
            self.invincible = True
            self.invincible_time = PLAYER_INVINCIBLE_TIME
            return True
        return False
    
    def is_alive(self):
        """생존 여부"""
        return self.health > 0
    
    def draw(self, surface, camera_offset=(0, 0)):
        """플레이어 그리기"""
        ox, oy = camera_offset
        screen_x = int(self.x - ox)
        screen_y = int(self.y - oy)
        
        # 무적 상태면 깜빡임
        if self.invincible and int(self.invincible_time * 10) % 2 == 0:
            alpha = 128
        else:
            alpha = 255
        
        # 플레이어 원 그리기
        color = COLOR_CYAN if self.is_dashing else COLOR_GREEN
        
        # 반투명 처리를 위한 서페이스
        if alpha < 255:
            temp_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(temp_surface, (*color, alpha), (self.radius, self.radius), self.radius)
            surface.blit(temp_surface, (screen_x - self.radius, screen_y - self.radius))
        else:
            pygame.draw.circle(surface, color, (screen_x, screen_y), self.radius)
        
        # 방향 표시
        if self.vx != 0 or self.vy != 0:
            end_x = screen_x + self.vx * self.radius * 1.5
            end_y = screen_y + self.vy * self.radius * 1.5
            pygame.draw.line(surface, (255, 255, 255), (screen_x, screen_y), (end_x, end_y), 2)
