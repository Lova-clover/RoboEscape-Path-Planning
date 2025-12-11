"""
레벨/맵 관리 시스템
"""

import numpy as np
import random
from config import (
    GRID_WIDTH, GRID_HEIGHT, TILE_EMPTY, TILE_WALL, TILE_TEMP_WALL, 
    TILE_KEY, TILE_EXIT, KEYS_REQUIRED
)


class Level:
    """게임 레벨을 관리하는 클래스"""
    
    def __init__(self, stage_num=1):
        self.stage_num = stage_num
        self.grid_map = None
        self.spawn_pos = None
        self.exit_pos = None
        self.key_positions = []
        self.keys_collected = 0
        
        # 임시 장벽 관리 (위치, 남은 시간)
        self.temp_walls = []
        
        self.generate_level()
    
    def generate_level(self):
        """레벨 생성"""
        # 빈 맵 초기화
        self.grid_map = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
        
        # 외벽 생성
        self.grid_map[0, :] = TILE_WALL
        self.grid_map[-1, :] = TILE_WALL
        self.grid_map[:, 0] = TILE_WALL
        self.grid_map[:, -1] = TILE_WALL
        
        # 스테이지별 맵 생성
        if self.stage_num == 1:
            self._generate_stage1()
        elif self.stage_num == 2:
            self._generate_stage2()
        elif self.stage_num == 3:
            self._generate_stage3()
        elif self.stage_num == 4:
            self._generate_stage4()
        elif self.stage_num == 5:
            self._generate_stage5()
        elif self.stage_num == 6:
            self._generate_stage6()
        else:
            self._generate_random()
        
        # 플레이어 시작 위치 설정 (안전 확보)
        self.spawn_pos = (5, GRID_HEIGHT // 2)
        # 스폰 지역 주변 클리어 (3x3)
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                sx, sy = self.spawn_pos[0] + dx, self.spawn_pos[1] + dy
                if 0 < sx < GRID_WIDTH - 1 and 0 < sy < GRID_HEIGHT - 1:
                    self.grid_map[sy][sx] = TILE_EMPTY
        
        # 출구 위치 설정
        self.exit_pos = (GRID_WIDTH - 6, GRID_HEIGHT // 2)
        self.grid_map[self.exit_pos[1]][self.exit_pos[0]] = TILE_EXIT
        # 출구 주변도 클리어
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                ex, ey = self.exit_pos[0] + dx, self.exit_pos[1] + dy
                if 0 < ex < GRID_WIDTH - 1 and 0 < ey < GRID_HEIGHT - 1:
                    if self.grid_map[ey][ex] != TILE_EXIT:
                        self.grid_map[ey][ex] = TILE_EMPTY
        
        # 열쇠 배치
        self._place_keys()
    
    def _generate_stage1(self):
        """스테이지 1: 기본 맵 (Bug1 학습용)"""
        # 중앙에 간단한 장애물
        for i in range(5, 10):
            self.grid_map[10][i] = TILE_WALL
            self.grid_map[12][i] = TILE_WALL
        
        # L자 장애물 (Bug 알고리즘 테스트용)
        for i in range(8, 14):
            self.grid_map[i][15] = TILE_WALL
        for i in range(15, 20):
            self.grid_map[13][i] = TILE_WALL
    
    def _generate_stage2(self):
        """스테이지 2: U자 구조 (APF 로컬 미니멈 유도용)"""
        # 중앙에 U자 구조 만들기 (더 넓게)
        cx, cy = GRID_WIDTH // 2, GRID_HEIGHT // 2
        
        # 왼쪽 벽
        for i in range(cy - 5, cy + 5):
            self.grid_map[i][cx - 10] = TILE_WALL
        
        # 오른쪽 벽
        for i in range(cy - 5, cy + 5):
            self.grid_map[i][cx + 10] = TILE_WALL
        
        # 아래쪽 벽
        for i in range(cx - 10, cx + 11):
            self.grid_map[cy + 4][i] = TILE_WALL
        
        # 추가 작은 장애물들 (스폰 지역은 피함)
        for i in range(5):
            x = random.randint(15, GRID_WIDTH - 10)
            y = random.randint(8, GRID_HEIGHT - 8)
            if self.grid_map[y][x] == TILE_EMPTY:
                self.grid_map[y][x] = TILE_WALL
    
    def _generate_stage3(self):
        """스테이지 3: 복잡한 미로 (PRM/RRT 테스트용)"""
        # 여러 개의 방과 복도 (시작 영역 피함)
        rooms = [
            (12, 6, 10, 7),   # 시작점에서 멀리
            (25, 6, 10, 7),
            (12, 14, 10, 6),
            (28, 14, 8, 6)
        ]
        
        for x, y, w, h in rooms:
            # 방 테두리
            for i in range(w):
                self.grid_map[y][x + i] = TILE_WALL
                self.grid_map[y + h - 1][x + i] = TILE_WALL
            for i in range(h):
                self.grid_map[y + i][x] = TILE_WALL
                self.grid_map[y + i][x + w - 1] = TILE_WALL
            
            # 출입구 2개 (더 많은 경로)
            door1 = random.randint(1, w - 2)
            door2 = random.randint(1, h - 2)
            self.grid_map[y][x + door1] = TILE_EMPTY
            self.grid_map[y + door2][x] = TILE_EMPTY
    
    def _generate_stage4(self):
        """스테이지 4: 그래프/트리 경로용 - 복잡한 미로"""
        # 여러 작은 방들로 구성
        rooms = [
            (8, 5, 8, 6),
            (20, 5, 8, 6),
            (8, 13, 8, 6),
            (20, 13, 8, 6),
            (32, 9, 6, 8)
        ]
        
        for x, y, w, h in rooms:
            # 방 테두리
            for i in range(w):
                self.grid_map[y][x + i] = TILE_WALL
                self.grid_map[y + h - 1][x + i] = TILE_WALL
            for i in range(h):
                self.grid_map[y + i][x] = TILE_WALL
                self.grid_map[y + i][x + w - 1] = TILE_WALL
            
            # 출입구 2개
            door1 = random.randint(1, w - 2)
            door2 = random.randint(1, h - 2)
            self.grid_map[y][x + door1] = TILE_EMPTY
            self.grid_map[y + door2][x] = TILE_EMPTY
    
    def _generate_stage5(self):
        """스테이지 5: Belief용 - 시야 차단 많은 맵"""
        # 기둥들이 많은 맵
        for y in range(5, GRID_HEIGHT - 5, 4):
            for x in range(8, GRID_WIDTH - 8, 5):
                # 2x2 기둥
                self.grid_map[y][x] = TILE_WALL
                self.grid_map[y][x + 1] = TILE_WALL
                self.grid_map[y + 1][x] = TILE_WALL
                self.grid_map[y + 1][x + 1] = TILE_WALL
        
        # 큰 벽들 (시야 차단용)
        for i in range(6, 16):
            self.grid_map[10][i] = TILE_WALL
        for i in range(25, 35):
            self.grid_map[12][i] = TILE_WALL
    
    def _generate_stage6(self):
        """스테이지 6: 보스전 - 중앙 아레나"""
        cx, cy = GRID_WIDTH // 2, GRID_HEIGHT // 2
        
        # 중앙 원형 아레나
        radius = 8
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                dist_sq = (x - cx) ** 2 + (y - cy) ** 2
                if abs(dist_sq - radius * radius) < radius * 2:
                    self.grid_map[y][x] = TILE_WALL
        
        # 4개 입구
        self.grid_map[cy][cx - radius] = TILE_EMPTY
        self.grid_map[cy][cx + radius] = TILE_EMPTY
        self.grid_map[cy - radius][cx] = TILE_EMPTY
        self.grid_map[cy + radius][cx] = TILE_EMPTY
        
        # 외곽 벽들
        for i in range(8, 15):
            self.grid_map[5][i] = TILE_WALL
            self.grid_map[GRID_HEIGHT - 6][i] = TILE_WALL
        for i in range(GRID_WIDTH - 15, GRID_WIDTH - 8):
            self.grid_map[5][i] = TILE_WALL
            self.grid_map[GRID_HEIGHT - 6][i] = TILE_WALL
    
    def _generate_random(self):
        """랜덤 장애물 배치"""
        num_obstacles = 20 + self.stage_num * 5
        
        for _ in range(num_obstacles):
            # 랜덤 위치
            x = random.randint(3, GRID_WIDTH - 3)
            y = random.randint(3, GRID_HEIGHT - 3)
            
            # 랜덤 크기 (1x1 ~ 4x4)
            w = random.randint(1, 4)
            h = random.randint(1, 4)
            
            for dy in range(h):
                for dx in range(w):
                    nx, ny = x + dx, y + dy
                    if 0 < nx < GRID_WIDTH - 1 and 0 < ny < GRID_HEIGHT - 1:
                        if self.grid_map[ny][nx] == TILE_EMPTY:
                            self.grid_map[ny][nx] = TILE_WALL
    
    def _place_keys(self):
        """열쇠 배치"""
        self.key_positions = []
        placed = 0
        attempts = 0
        max_attempts = 100
        
        while placed < KEYS_REQUIRED and attempts < max_attempts:
            x = random.randint(5, GRID_WIDTH - 5)
            y = random.randint(5, GRID_HEIGHT - 5)
            
            if self.grid_map[y][x] == TILE_EMPTY:
                # 스폰 위치와 충분히 멀리 떨어진 곳에만 배치
                dist = abs(x - self.spawn_pos[0]) + abs(y - self.spawn_pos[1])
                if dist > 10:
                    self.grid_map[y][x] = TILE_KEY
                    self.key_positions.append((x, y))
                    # 주변 3x3 클리어 (접근 가능하도록)
                    for dy in range(-1, 2):
                        for dx in range(-1, 2):
                            kx, ky = x + dx, y + dy
                            if 0 < kx < GRID_WIDTH - 1 and 0 < ky < GRID_HEIGHT - 1:
                                if self.grid_map[ky][kx] == TILE_WALL:
                                    self.grid_map[ky][kx] = TILE_EMPTY
                    placed += 1
            
            attempts += 1
    
    def collect_key(self, grid_x, grid_y):
        """열쇠 수집"""
        if self.grid_map[grid_y][grid_x] == TILE_KEY:
            self.grid_map[grid_y][grid_x] = TILE_EMPTY
            self.keys_collected += 1
            if (grid_x, grid_y) in self.key_positions:
                self.key_positions.remove((grid_x, grid_y))
            return True
        return False
    
    def can_exit(self):
        """출구로 나갈 수 있는지 확인"""
        return self.keys_collected >= KEYS_REQUIRED
    
    def add_temp_wall(self, grid_x, grid_y, duration):
        """임시 장벽 추가"""
        if self.grid_map[grid_y][grid_x] == TILE_EMPTY:
            self.grid_map[grid_y][grid_x] = TILE_TEMP_WALL
            self.temp_walls.append(((grid_x, grid_y), duration))
            return True
        return False
    
    def update(self, dt):
        """레벨 업데이트 (임시 장벽 타이머 등)"""
        # 임시 장벽 시간 감소
        walls_to_remove = []
        
        for i, (pos, time_left) in enumerate(self.temp_walls):
            time_left -= dt
            self.temp_walls[i] = (pos, time_left)
            
            if time_left <= 0:
                walls_to_remove.append(i)
                # 맵에서 제거
                gx, gy = pos
                if self.grid_map[gy][gx] == TILE_TEMP_WALL:
                    self.grid_map[gy][gx] = TILE_EMPTY
        
        # 제거할 장벽들 삭제 (역순으로)
        for i in reversed(walls_to_remove):
            del self.temp_walls[i]
