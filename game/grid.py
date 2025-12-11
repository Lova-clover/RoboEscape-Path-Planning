"""
그리드 시스템 및 좌표 변환
"""

import numpy as np
from config import TILE_SIZE, GRID_WIDTH, GRID_HEIGHT, TILE_WALL, TILE_TEMP_WALL


def grid_to_world(gx, gy):
    """그리드 좌표를 월드 좌표로 변환 (중심점)"""
    return gx * TILE_SIZE + TILE_SIZE / 2, gy * TILE_SIZE + TILE_SIZE / 2


def world_to_grid(x, y):
    """월드 좌표를 그리드 좌표로 변환"""
    return int(x // TILE_SIZE), int(y // TILE_SIZE)


def is_valid_grid(gx, gy):
    """그리드 좌표가 유효한지 확인"""
    return 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT


def is_walkable(grid_map, gx, gy):
    """해당 그리드 타일을 걸어갈 수 있는지 확인"""
    if not is_valid_grid(gx, gy):
        return False
    tile = grid_map[gy][gx]
    return tile != TILE_WALL and tile != TILE_TEMP_WALL


def get_neighbors(gx, gy, grid_map, diagonal=True):
    """인접한 이동 가능한 그리드 좌표들을 반환"""
    neighbors = []
    
    # 4방향
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # 8방향 (대각선 포함)
    if diagonal:
        directions.extend([(-1, -1), (-1, 1), (1, -1), (1, 1)])
    
    for dx, dy in directions:
        nx, ny = gx + dx, gy + dy
        if is_walkable(grid_map, nx, ny):
            neighbors.append((nx, ny))
    
    return neighbors


def line_of_sight(grid_map, start, end):
    """두 점 사이에 장애물이 없는지 확인 (Bresenham 알고리즘)"""
    x0, y0 = start
    x1, y1 = end
    
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    
    x, y = x0, y0
    
    while True:
        # 현재 위치가 벽이면 시야 차단
        if not is_walkable(grid_map, x, y):
            return False
        
        # 목표 도달
        if x == x1 and y == y1:
            return True
        
        # 다음 위치 계산
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy


def distance_grid(p1, p2):
    """두 그리드 좌표 사이의 유클리드 거리"""
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def distance_world(p1, p2):
    """두 월드 좌표 사이의 유클리드 거리"""
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def get_rectangle_tiles(center_x, center_y, width, height):
    """중심점 기준 사각형 영역의 그리드 타일들을 반환"""
    tiles = []
    half_w = width // 2
    half_h = height // 2
    
    for dy in range(-half_h, half_h + 1):
        for dx in range(-half_w, half_w + 1):
            gx, gy = center_x + dx, center_y + dy
            if is_valid_grid(gx, gy):
                tiles.append((gx, gy))
    
    return tiles


def check_collision_circle(x, y, radius, grid_map):
    """원형 충돌 체크 (플레이어/적 이동용)"""
    # 원의 경계 상자를 그리드로 변환
    gx_min = int((x - radius) // TILE_SIZE)
    gx_max = int((x + radius) // TILE_SIZE)
    gy_min = int((y - radius) // TILE_SIZE)
    gy_max = int((y + radius) // TILE_SIZE)
    
    # 경계 상자 내의 모든 타일 체크
    for gy in range(gy_min, gy_max + 1):
        for gx in range(gx_min, gx_max + 1):
            if not is_valid_grid(gx, gy):
                return True
            
            if not is_walkable(grid_map, gx, gy):
                # 타일과 원의 충돌 체크
                tile_x, tile_y = grid_to_world(gx, gy)
                dist = distance_world((x, y), (tile_x, tile_y))
                
                # 타일의 반경 (타일 중심에서 모서리까지)
                tile_radius = TILE_SIZE * 0.707  # sqrt(2)/2 * TILE_SIZE
                
                if dist < radius + tile_radius:
                    return True
    
    return False
