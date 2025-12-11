"""
파티클 이펙트 시스템
"""

import pygame
import random
import math
from config import COLOR_WHITE


class Particle:
    """단일 파티클"""
    
    def __init__(self, x, y, vx, vy, lifetime, color, size=3):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.color = color
        self.size = size
        self.gravity = 100  # pixels/s^2
    
    def update(self, dt):
        """파티클 업데이트"""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += self.gravity * dt  # 중력
        self.lifetime -= dt
    
    def is_alive(self):
        """생존 여부"""
        return self.lifetime > 0
    
    def draw(self, surface, camera_offset=(0, 0)):
        """파티클 그리기"""
        ox, oy = camera_offset
        screen_x = int(self.x - ox)
        screen_y = int(self.y - oy)
        
        # 알파 계산 (수명에 따라 투명해짐)
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        
        # 크기 감소
        current_size = int(self.size * (self.lifetime / self.max_lifetime))
        if current_size < 1:
            current_size = 1
        
        # 반투명 원 그리기
        temp_surface = pygame.Surface((current_size * 2, current_size * 2), pygame.SRCALPHA)
        pygame.draw.circle(temp_surface, (*self.color, alpha), 
                         (current_size, current_size), current_size)
        surface.blit(temp_surface, (screen_x - current_size, screen_y - current_size))


class ParticleSystem:
    """파티클 시스템 관리"""
    
    def __init__(self):
        self.particles = []
    
    def emit_burst(self, x, y, count, color, speed_range=(50, 150)):
        """폭발 파티클"""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(*speed_range)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            lifetime = random.uniform(0.3, 0.8)
            size = random.randint(2, 5)
            
            particle = Particle(x, y, vx, vy, lifetime, color, size)
            self.particles.append(particle)
    
    def emit_dash_trail(self, x, y, color):
        """대시 트레일 파티클"""
        for _ in range(3):
            vx = random.uniform(-20, 20)
            vy = random.uniform(-20, 20)
            lifetime = random.uniform(0.2, 0.4)
            
            particle = Particle(x, y, vx, vy, lifetime, color, 4)
            self.particles.append(particle)
    
    def emit_hit_effect(self, x, y):
        """충돌 이펙트"""
        self.emit_burst(x, y, 15, (255, 50, 50), speed_range=(100, 250))
    
    def emit_key_collect(self, x, y):
        """열쇠 수집 이펙트"""
        self.emit_burst(x, y, 20, (255, 255, 0), speed_range=(80, 200))
    
    def emit_wall_place(self, x, y):
        """장벽 설치 이펙트"""
        self.emit_burst(x, y, 10, (100, 100, 255), speed_range=(50, 120))
    
    def update(self, dt):
        """모든 파티클 업데이트"""
        # 파티클 업데이트
        for particle in self.particles:
            particle.update(dt)
        
        # 죽은 파티클 제거
        self.particles = [p for p in self.particles if p.is_alive()]
    
    def draw(self, surface, camera_offset=(0, 0)):
        """모든 파티클 그리기"""
        for particle in self.particles:
            particle.draw(surface, camera_offset)
    
    def clear(self):
        """모든 파티클 제거"""
        self.particles.clear()
