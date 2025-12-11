"""
Probabilistic Localization (Bayesian Filter)
확률 기반 위치 추정
"""

import numpy as np
import math
from game.grid import is_valid_grid, is_walkable, line_of_sight, distance_world
from config import TILE_SIZE, GRID_WIDTH, GRID_HEIGHT


class BeliefPlanner:
    """Belief 기반 추적 플래너"""
    
    def __init__(self, grid_resolution=4, sensor_range=300, sensor_noise=40, motion_noise=20):
        """
        Args:
            grid_resolution: Belief 그리드 해상도 (값이 클수록 저해상도)
            sensor_range: 센서 감지 범위
            sensor_noise: 센서 노이즈 (표준편차)
            motion_noise: 모션 노이즈 (표준편차)
        """
        self.resolution = grid_resolution
        self.sensor_range = sensor_range
        self.sensor_noise = sensor_noise
        self.motion_noise = motion_noise
        
        # Belief 그리드 크기
        self.belief_width = GRID_WIDTH // grid_resolution
        self.belief_height = GRID_HEIGHT // grid_resolution
        
        # Belief 분포 (확률)
        self.belief = np.ones((self.belief_height, self.belief_width))
        self.belief /= self.belief.sum()  # 정규화
        
        # 이전 측정값
        self.last_measurement = None
    
    def reset(self):
        """Belief 초기화 (균등 분포)"""
        self.belief = np.ones((self.belief_height, self.belief_width))
        self.belief /= self.belief.sum()
        self.last_measurement = None
    
    def predict(self, motion_model):
        """
        Prediction step (Motion Model)
        
        Args:
            motion_model: (dx, dy) 예상 이동량 (그리드 단위)
        """
        dx, dy = motion_model
        
        # 새 belief
        new_belief = np.zeros_like(self.belief)
        
        for y in range(self.belief_height):
            for x in range(self.belief_width):
                if self.belief[y, x] < 0.001:
                    continue
                
                # 이동 후 위치 (노이즈 고려)
                for noise_dx in range(-1, 2):
                    for noise_dy in range(-1, 2):
                        nx = x + dx + noise_dx
                        ny = y + dy + noise_dy
                        
                        if 0 <= nx < self.belief_width and 0 <= ny < self.belief_height:
                            # 노이즈 확률 (가우시안)
                            noise_prob = self._gaussian_2d(noise_dx, noise_dy, 0, 0, 1.0)
                            new_belief[ny, nx] += self.belief[y, x] * noise_prob
        
        self.belief = new_belief
        self.belief /= (self.belief.sum() + 1e-10)  # 정규화
    
    def update(self, measurement, grid_map, enemy_pos):
        """
        Update step (Sensor Model)
        
        Args:
            measurement: (x, y) 플레이어 측정 위치 (월드 좌표)
            grid_map: 맵 (시야 체크용)
            enemy_pos: (x, y) 적 위치 (월드 좌표)
        """
        # 측정값을 belief 그리드 좌표로 변환
        meas_gx = int(measurement[0] / TILE_SIZE / self.resolution)
        meas_gy = int(measurement[1] / TILE_SIZE / self.resolution)
        
        # 거리 체크
        dist = distance_world(enemy_pos, measurement)
        if dist > self.sensor_range:
            # 범위 밖이면 업데이트 안 함
            return
        
        # 시야 체크
        enemy_grid = (int(enemy_pos[0] / TILE_SIZE), int(enemy_pos[1] / TILE_SIZE))
        meas_grid = (int(measurement[0] / TILE_SIZE), int(measurement[1] / TILE_SIZE))
        
        has_line_of_sight = line_of_sight(grid_map, enemy_grid, meas_grid)
        
        # Likelihood 계산
        for y in range(self.belief_height):
            for x in range(self.belief_width):
                # 이 위치에서 측정값까지의 거리
                dx = x - meas_gx
                dy = y - meas_gy
                
                # 가우시안 likelihood
                if has_line_of_sight:
                    # 시야 확보 시: 정확한 측정
                    likelihood = self._gaussian_2d(dx, dy, 0, 0, 
                                                   self.sensor_noise / (TILE_SIZE * self.resolution))
                else:
                    # 시야 차단 시: 불확실한 측정
                    likelihood = self._gaussian_2d(dx, dy, 0, 0, 
                                                   self.sensor_noise * 2 / (TILE_SIZE * self.resolution))
                
                self.belief[y, x] *= likelihood
        
        # 정규화
        belief_sum = self.belief.sum()
        if belief_sum > 1e-10:
            self.belief /= belief_sum
        else:
            # 모든 확률이 0이면 리셋
            self.reset()
        
        self.last_measurement = measurement
    
    def get_estimated_position(self):
        """가장 확률이 높은 위치 반환 (월드 좌표)"""
        # 최대값 위치
        max_idx = np.unravel_index(np.argmax(self.belief), self.belief.shape)
        by, bx = max_idx
        
        # Belief 그리드 → 월드 좌표
        world_x = (bx * self.resolution + self.resolution / 2) * TILE_SIZE
        world_y = (by * self.resolution + self.resolution / 2) * TILE_SIZE
        
        return (world_x, world_y)
    
    def get_mean_position(self):
        """평균 위치 반환 (가중평균)"""
        total_x = 0
        total_y = 0
        total_prob = 0
        
        for y in range(self.belief_height):
            for x in range(self.belief_width):
                prob = self.belief[y, x]
                total_x += x * prob
                total_y += y * prob
                total_prob += prob
        
        if total_prob > 0:
            mean_x = total_x / total_prob
            mean_y = total_y / total_prob
            
            # Belief 그리드 → 월드 좌표
            world_x = (mean_x * self.resolution + self.resolution / 2) * TILE_SIZE
            world_y = (mean_y * self.resolution + self.resolution / 2) * TILE_SIZE
            
            return (world_x, world_y)
        
        return self.get_estimated_position()
    
    def _gaussian_2d(self, x, y, mu_x, mu_y, sigma):
        """2D 가우시안"""
        dx = x - mu_x
        dy = y - mu_y
        return math.exp(-(dx*dx + dy*dy) / (2 * sigma * sigma)) / (2 * math.pi * sigma * sigma)
    
    def get_belief_heatmap(self):
        """시각화용 히트맵 데이터"""
        return self.belief.copy()
