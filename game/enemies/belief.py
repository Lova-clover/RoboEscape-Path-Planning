"""
Belief 기반 추적 적
"""

import random
import numpy as np
from game.enemies import EnemyBase
from algos.belief import BeliefPlanner
from game.grid import world_to_grid
from config import (
    ENEMY_BELIEF_SPEED, COLOR_BELIEF,
    BELIEF_GRID_RESOLUTION, BELIEF_SENSOR_RANGE,
    BELIEF_SENSOR_NOISE, BELIEF_MOTION_NOISE
)


class BeliefEnemy(EnemyBase):
    """Probabilistic Localization 기반 적"""
    
    def __init__(self, x, y):
        super().__init__(x, y, ENEMY_BELIEF_SPEED, COLOR_BELIEF, "Belief")
        self.planner = BeliefPlanner(
            grid_resolution=BELIEF_GRID_RESOLUTION,
            sensor_range=BELIEF_SENSOR_RANGE,
            sensor_noise=BELIEF_SENSOR_NOISE,
            motion_noise=BELIEF_MOTION_NOISE
        )
        
        # 측정 주기
        self.measurement_timer = 0
        self.measurement_interval = 0.5  # 0.5초마다 센서 측정
        self.state = 'estimating'  # 상태 표시용
        
        # 노이즈 효과
        self.is_noised = False
        self.noise_duration = 0
        
        # 시각화
        self.show_belief = True
    
    def update(self, dt, player, level):
        """업데이트"""
        # 노이즈 효과 감소
        if self.is_noised:
            self.noise_duration -= dt
            if self.noise_duration <= 0:
                self.is_noised = False
        
        self.measurement_timer += dt
        
        # 주기적으로 센서 측정 및 belief 업데이트
        if self.measurement_timer >= self.measurement_interval:
            self.measurement_timer = 0
            
            # Motion model (이전 이동 방향 예측)
            prev_grid = world_to_grid(self.x, self.y)
            
            # Prediction step
            motion = (0, 0)  # 간단하게 제자리로 가정
            self.planner.predict(motion)
            
            # Measurement (노이즈 추가)
            true_pos = (player.x, player.y)
            
            if self.is_noised:
                # 노이즈 폭탄 영향: 큰 오차
                noise_x = random.gauss(0, BELIEF_SENSOR_NOISE * 3)
                noise_y = random.gauss(0, BELIEF_SENSOR_NOISE * 3)
            else:
                # 일반 센서 노이즈
                noise_x = random.gauss(0, BELIEF_SENSOR_NOISE)
                noise_y = random.gauss(0, BELIEF_SENSOR_NOISE)
            
            noisy_measurement = (true_pos[0] + noise_x, true_pos[1] + noise_y)
            
            # Update step
            self.planner.update(noisy_measurement, level.grid_map, (self.x, self.y))
        
        # Belief 기반 목표 위치
        estimated_pos = self.planner.get_mean_position()
        
        # 목표를 향해 이동
        self.move_towards(estimated_pos[0], estimated_pos[1], dt, level)
        
        # 간혹 랜덤 탐색 (belief 불확실성 높을 때)
        max_belief = np.max(self.planner.belief)
        if max_belief < 0.05:  # 매우 불확실
            # 랜덤 워크
            angle = random.uniform(0, 2 * 3.14159)
            import math
            rand_x = self.x + math.cos(angle) * 50
            rand_y = self.y + math.sin(angle) * 50
            self.move_towards(rand_x, rand_y, dt * 0.5, level)
    
    def apply_noise_effect(self, duration=3.0):
        """노이즈 폭탄 효과 적용"""
        self.is_noised = True
        self.noise_duration = duration
    
    def draw(self, surface, camera_offset=(0, 0)):
        """Belief 분포 포함 그리기"""
        # Belief 히트맵 먼저 그리기
        if self.show_belief:
            self.draw_belief_heatmap(surface, camera_offset)
        
        # 적 그리기
        super().draw(surface, camera_offset)
        
        # 노이즈 상태 표시
        if self.is_noised:
            import pygame
            ox, oy = camera_offset
            screen_x = int(self.x - ox)
            screen_y = int(self.y - oy)
            
            # 노이즈 이펙트 (깜빡이는 원)
            if int(self.noise_duration * 10) % 2 == 0:
                pygame.draw.circle(surface, (255, 255, 0), (screen_x, screen_y), 
                                 self.radius + 5, 2)
    
    def draw_belief_heatmap(self, surface, camera_offset=(0, 0)):
        """Belief 히트맵 시각화"""
        import pygame
        from config import TILE_SIZE
        
        ox, oy = camera_offset
        belief = self.planner.get_belief_heatmap()
        
        # 최대값 정규화
        max_belief = np.max(belief)
        if max_belief < 1e-6:
            return
        
        belief_normalized = belief / max_belief
        
        # 히트맵 그리기
        for y in range(belief.shape[0]):
            for x in range(belief.shape[1]):
                prob = belief_normalized[y, x]
                
                if prob < 0.1:  # 낮은 확률은 스킵
                    continue
                
                # Belief 그리드 → 월드 좌표
                world_x = (x * self.planner.resolution + self.planner.resolution / 2) * TILE_SIZE
                world_y = (y * self.planner.resolution + self.planner.resolution / 2) * TILE_SIZE
                
                screen_x = world_x - ox
                screen_y = world_y - oy
                
                # 색상 (부드러운 보라 계열, 낮은 투명도)
                alpha = int(prob * 50)  # 투명도 대폭 감소
                color = (*self.color, alpha)
                
                # 반투명 사각형
                size = self.planner.resolution * TILE_SIZE
                temp_surface = pygame.Surface((size, size), pygame.SRCALPHA)
                temp_surface.fill(color)
                surface.blit(temp_surface, (screen_x - size/2, screen_y - size/2))
