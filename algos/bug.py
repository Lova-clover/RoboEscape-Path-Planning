"""
Bug 알고리즘 (Bug1, Bug2, Tangent Bug)
"""

import math
import numpy as np
from game.grid import is_walkable, line_of_sight, get_neighbors


class Bug1Planner:
    """Bug1 알고리즘"""
    
    def __init__(self):
        self.state = 'motion_to_goal'  # 'motion_to_goal', 'boundary_following', 'leave_wall'
        self.hit_point = None
        self.obstacle_tiles = set()  # 처음 부딪힌 장애물의 타일들 (BFS로 탐색)
        self.leave_point = None
        self.wall_points = []
        self.circumnavigate_complete = False
        self.min_distance = float('inf')
    
    def plan_step(self, current_pos, goal_pos, grid_map):
        """한 스텝 계획"""
        gx, gy = current_pos
        goal_gx, goal_gy = goal_pos
        
        # 목표 도달
        if (gx, gy) == (goal_gx, goal_gy):
            return current_pos
        
        # Motion to goal 상태
        if self.state == 'motion_to_goal':
            # 목표로 직진 시도
            next_pos = self._move_towards(current_pos, goal_pos)
            
            # 장애물 만남
            if not is_walkable(grid_map, next_pos[0], next_pos[1]):
                # BFS로 부딪힌 장애물의 모든 타일 찾기
                found_tiles = self._find_obstacle_tiles(next_pos, grid_map)
                
                # 실제 장애물을 찾았으면 boundary following 시작
                if found_tiles:
                    self.state = 'boundary_following'
                    self.hit_point = current_pos
                    self.obstacle_tiles = found_tiles
                    self.wall_points = []
                    self.min_distance = self._distance(current_pos, goal_pos)
                    self.circumnavigate_complete = False
                    return self._follow_wall(current_pos, goal_pos, grid_map)
                else:
                    # 장애물을 찾지 못함 (플레이어 등) - 다른 방향으로 우회
                    neighbors = get_neighbors(gx, gy, grid_map, diagonal=True)
                    if neighbors:
                        # 목표에 가까운 방향으로 이동
                        return min(neighbors, key=lambda n: self._distance(n, goal_pos))
                    return current_pos
            
            return next_pos
        
        # Boundary following 상태
        elif self.state == 'boundary_following':
            current_dist = self._distance(current_pos, goal_pos)
            
            # 최소 거리 업데이트 (한 바퀴 도는 동안 가장 가까운 지점 기록)
            if current_dist < self.min_distance:
                self.min_distance = current_dist
                self.leave_point = current_pos
            
            # Bug1 규칙: 반드시 한 바퀴를 완전히 돌아야 함
            # 충분히 돌았고(최소 10스텝) 시작점으로 돌아왔는지 확인
            if len(self.wall_points) > 10 and self._distance(current_pos, self.hit_point) < 1.5:
                self.circumnavigate_complete = True
                if self.leave_point:
                    self.state = 'leave_wall'
                    return self.leave_point
            
            # Bug1 핵심: boundary following 중에는 목표를 완전히 무시하고 무조건 벽만 따라감
            # 플레이어가 어디 있든 상관없이 오직 벽을 따라 한 바퀴 도는 것만 수행
            self.wall_points.append(current_pos)
            return self._follow_wall(current_pos, goal_pos, grid_map)
        
        # Leave wall 상태
        elif self.state == 'leave_wall':
            # 벽에서 벗어남
            if line_of_sight(grid_map, current_pos, goal_pos):
                self.state = 'motion_to_goal'
                self.hit_point = None
                self.leave_point = None
                self.wall_points = []
            
            return self._move_towards(current_pos, goal_pos)
        
        return current_pos
    
    def _move_towards(self, current, goal):
        """목표를 향해 한 칸 이동"""
        dx = goal[0] - current[0]
        dy = goal[1] - current[1]
        
        # 정규화 및 한 칸 이동
        if abs(dx) > abs(dy):
            return (current[0] + (1 if dx > 0 else -1), current[1])
        elif dy != 0:
            return (current[0], current[1] + (1 if dy > 0 else -1))
        else:
            return current
    
    def _follow_wall(self, current_pos, goal_pos, grid_map):
        """벽을 따라 이동 (boundary following with right-hand rule)
        Bug1 규칙: boundary following 중에는 목표를 완전히 무시하고 오직 벽만 따라감
        벽에서 1-2칸 떨어져서 크게 돌도록 수정"""
        gx, gy = current_pos
        
        # 갈 수 있는 이웃들
        neighbors = get_neighbors(gx, gy, grid_map, diagonal=True)
        
        if not neighbors:
            return current_pos
        
        # 처음 부딪힌 장애물에만 인접한 이웃만 선택
        if self.obstacle_tiles:
            valid_neighbors = []
            for nx, ny in neighbors:
                # 이 위치가 처음 부딪힌 장애물에 인접한지 확인
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if (nx + dx, ny + dy) in self.obstacle_tiles:
                            valid_neighbors.append((nx, ny))
                            break
                    else:
                        continue
                    break
            
            # 처음 부딪힌 장애물에 인접한 이웃만 사용
            if valid_neighbors:
                neighbors = valid_neighbors
        
        # 이전 위치 기반으로 벽을 따라 계속 이동
        if len(self.wall_points) >= 2:
            # 일관된 방향으로 벽을 따라감 (목표 완전 무시)
            prev_pos = self.wall_points[-1]
            prev_prev_pos = self.wall_points[-2]
            
            # 이전 이동 방향 벡터
            prev_dir_x = prev_pos[0] - prev_prev_pos[0]
            prev_dir_y = prev_pos[1] - prev_prev_pos[1]
            
            # Bug1: 방향 연속성만 고려
            best = min(neighbors, key=lambda n: (
                # 이전 방향과의 일관성
                -(prev_dir_x * (n[0] - gx) + prev_dir_y * (n[1] - gy))
            ))
            return best
        
        # 첫 벽 따라가기 시작 - 벽과 가장 가까운 곳으로
        best = min(neighbors, key=lambda n: (
            # 장애물과의 인접도
            -sum(1 for dy in [-1, 0, 1] for dx in [-1, 0, 1] 
                 if not is_walkable(grid_map, n[0] + dx, n[1] + dy))
        ))
        
        return best
    
    def _find_obstacle_tiles(self, start_tile, grid_map):
        """BFS로 부딪힌 장애물의 모든 타일 찾기"""
        from collections import deque
        
        map_width = len(grid_map[0])
        map_height = len(grid_map)
        
        # 맵 경계인지 확인
        def is_boundary(x, y):
            return x == 0 or x == map_width - 1 or y == 0 or y == map_height - 1
        
        # 시작 타일이 맵 경계면 빈 set 반환 (경계는 무시)
        if is_boundary(start_tile[0], start_tile[1]):
            return set()
        
        # BFS로 연결된 장애물 타일들 찾기
        visited = set()
        queue = deque([start_tile])
        visited.add(start_tile)
        obstacle_tiles = {start_tile}
        
        while queue:
            x, y = queue.popleft()
            
            # 4방향 탐색
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                nx, ny = x + dx, y + dy
                
                if (nx, ny) in visited:
                    continue
                if nx < 0 or nx >= map_width or ny < 0 or ny >= map_height:
                    continue
                
                visited.add((nx, ny))
                
                # 벽이면서 맵 경계가 아닌 경우만 포함
                if not is_walkable(grid_map, nx, ny) and not is_boundary(nx, ny):
                    obstacle_tiles.add((nx, ny))
                    queue.append((nx, ny))
        
        return obstacle_tiles
    
    def _find_nearby_obstacle_center(self, pos, grid_map):
        """현재 위치 주변의 내부 장애물들을 찾아서 중심점 반환 (맵 경계 제외)"""
        gx, gy = pos
        nearby_walls = []
        
        # 맵 크기 확인
        map_width = len(grid_map[0])
        map_height = len(grid_map)
        
        # 3x3 범위 내의 벽 찾기 (범위 축소)
        search_range = 3
        for dy in range(-search_range, search_range + 1):
            for dx in range(-search_range, search_range + 1):
                check_x, check_y = gx + dx, gy + dy
                
                # 범위 체크
                if 0 <= check_x < map_width and 0 <= check_y < map_height:
                    # 맵 경계는 제외 (내부 장애물만 포함)
                    is_boundary = (check_x == 0 or check_x == map_width - 1 or 
                                 check_y == 0 or check_y == map_height - 1)
                    
                    if not is_boundary and not is_walkable(grid_map, check_x, check_y):
                        nearby_walls.append((check_x, check_y))
        
        # 벽들의 중심점 계산
        if nearby_walls:
            avg_x = sum(w[0] for w in nearby_walls) / len(nearby_walls)
            avg_y = sum(w[1] for w in nearby_walls) / len(nearby_walls)
            return (avg_x, avg_y)
        
        # 내부 장애물을 못 찾으면 현재 위치 반환
        return pos
    
    def _distance(self, p1, p2):
        """유클리드 거리"""
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


class Bug2Planner:
    """Bug2 알고리즘 - M-line 기반"""
    
    def __init__(self):
        self.state = 'motion_to_goal'  # 'motion_to_goal', 'boundary_following'
        self.m_line = None  # (start, goal)
        self.hit_point = None
        self.obstacle_tiles = set()  # 처음 부딪힌 장애물의 타일들
        self.start_pos = None  # M-line 시각화용
        self.goal_pos = None   # M-line 시각화용
    
    def plan_step(self, current_pos, goal_pos, grid_map, start_pos=None):
        """한 스텝 계획"""
        if start_pos is None:
            start_pos = current_pos
        
        gx, gy = current_pos
        goal_gx, goal_gy = goal_pos
        
        # M-line 시작점 설정 (최초 1회만)
        if self.start_pos is None:
            self.start_pos = start_pos
        
        # M-line 업데이트 (시작점은 고정, 목표점은 현재 목표로)
        self.goal_pos = goal_pos
        self.m_line = (self.start_pos, goal_pos)
        
        # 목표 도달
        if (gx, gy) == (goal_gx, goal_gy):
            return current_pos
        
        # Motion to goal 상태 - M-line을 따라 이동
        if self.state == 'motion_to_goal':
            # M-line을 따라 목표로 이동
            next_pos = self._move_along_m_line(current_pos, goal_pos, grid_map)
            
            # 장애물 만남
            if not is_walkable(grid_map, next_pos[0], next_pos[1]):
                # BFS로 부딪힌 장애물의 모든 타일 찾기
                found_tiles = self._find_obstacle_tiles(next_pos, grid_map)
                
                # 실제 장애물을 찾았으면 boundary following 시작
                if found_tiles:
                    self.state = 'boundary_following'
                    self.hit_point = current_pos
                    self.obstacle_tiles = found_tiles
                    return self._follow_wall(current_pos, goal_pos, grid_map)
                else:
                    # 장애물을 찾지 못함 (플레이어 등) - 다른 방향으로 우회
                    neighbors = get_neighbors(gx, gy, grid_map, diagonal=True)
                    if neighbors:
                        # M-line에 가까운 방향으로 이동
                        return min(neighbors, key=lambda n: self._distance_to_m_line(n))
                    return current_pos
            
            return next_pos
        
        # Boundary following 상태
        elif self.state == 'boundary_following':
            # M-line에 도달하고 hit point보다 목표에 가까우면서, 목표로 가는 길이 clear한가?
            if self._on_m_line(current_pos) and \
               self._distance(current_pos, goal_pos) < self._distance(self.hit_point, goal_pos):
                # 목표를 향한 다음 이동이 안전한지 확인
                next_towards_goal = self._move_towards(current_pos, goal_pos)
                if is_walkable(grid_map, next_towards_goal[0], next_towards_goal[1]):
                    self.state = 'motion_to_goal'
                    self.hit_point = None
                    self.obstacle_tiles = set()  # 장애물 타일 초기화
                    return next_towards_goal
            
            # boundary following 중에는 무조건 벽을 따라감 (목표 방향 무시)
            return self._follow_wall(current_pos, goal_pos, grid_map)
        
        return current_pos
    
    def _move_towards(self, current, goal):
        """목표를 향해 한 칸 이동"""
        dx = goal[0] - current[0]
        dy = goal[1] - current[1]
        
        if abs(dx) > abs(dy):
            return (current[0] + (1 if dx > 0 else -1), current[1])
        elif dy != 0:
            return (current[0], current[1] + (1 if dy > 0 else -1))
        else:
            return current
    
    def _move_along_m_line(self, current_pos, goal_pos, grid_map):
        """M-line을 따라 목표로 이동"""
        gx, gy = current_pos
        
        # 목표를 향한 직진 방향 시도
        direct_next = self._move_towards(current_pos, goal_pos)
        
        # 직진이 가능하고 M-line에서 너무 멀지 않으면 직진
        if is_walkable(grid_map, direct_next[0], direct_next[1]):
            # M-line에서 너무 멀어지지 않으면 직진
            if self._distance_to_m_line(direct_next) < 3.0:  # threshold
                return direct_next
        
        # 직진이 불가능하거나 M-line에서 멀어지면 이웃 중 선택
        neighbors = get_neighbors(gx, gy, grid_map, diagonal=True)
        
        if not neighbors:
            return current_pos
        
        # 목표에 가까워지면서 M-line 근처를 유지하는 방향 선택
        best_neighbor = min(neighbors, key=lambda n: (
            self._distance(n, goal_pos),    # 목표에 가까울수록 우선 (1순위)
            self._distance_to_m_line(n)     # M-line에 가까울수록 좋음 (2순위)
        ))
        
        return best_neighbor
    
    def _follow_wall(self, current_pos, goal_pos, grid_map):
        """벽을 따라 이동하면서 M-line으로 복귀 시도 (특정 장애물만 따라감)"""
        gx, gy = current_pos
        neighbors = get_neighbors(gx, gy, grid_map, diagonal=True)
        
        if not neighbors:
            return current_pos
        
        # 처음 부딪힌 장애물과 인접한 이웃만 필터링
        if self.obstacle_tiles:
            offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            valid_neighbors = []
            for n in neighbors:
                # 이 이웃이 처음 부딪힌 장애물 타일에 인접한가?
                is_adjacent = any(
                    (n[0] + dx, n[1] + dy) in self.obstacle_tiles
                    for dx, dy in offsets
                )
                if is_adjacent:
                    valid_neighbors.append(n)
            
            # 유효한 이웃이 있으면 그 중에서만 선택
            if valid_neighbors:
                neighbors = valid_neighbors
        
        # Bug2: M-line에 가까워지는 방향으로 이동
        best_neighbor = min(neighbors, key=lambda n: (
            self._distance_to_m_line(n),  # M-line에 가까운 곳 우선
            # 벽과의 인접성도 고려 (벽을 따라가기 위해)
            -sum(1 for dy in [-1, 0, 1] for dx in [-1, 0, 1] 
                 if not is_walkable(grid_map, n[0] + dx, n[1] + dy)) * 0.1
        ))
        
        return best_neighbor
    
    def _on_m_line(self, pos, threshold=1.5):
        """M-line 위에 있는지 확인"""
        if self.m_line is None:
            return False
        
        return self._distance_to_m_line(pos) < threshold
    
    def _distance_to_m_line(self, pos):
        """M-line까지의 거리"""
        if self.m_line is None:
            return float('inf')
        
        start, goal = self.m_line
        
        # 점에서 직선까지의 거리
        x0, y0 = pos
        x1, y1 = start
        x2, y2 = goal
        
        num = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
        den = math.sqrt((y2 - y1)**2 + (x2 - x1)**2)
        
        if den == 0:
            return self._distance(pos, start)
        
        return num / den
    
    def _find_obstacle_tiles(self, start_pos, grid_map):
        """처음 부딪힌 장애물의 모든 타일을 BFS로 찾기 (맵 경계 제외)"""
        gx, gy = start_pos
        map_width = len(grid_map[0])
        map_height = len(grid_map)
        
        # 시작 위치가 벽이 아니면 인접한 벽 찾기
        if is_walkable(grid_map, gx, gy):
            # 4방향에서 벽 찾기
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = gx + dx, gy + dy
                if 0 <= nx < map_width and 0 <= ny < map_height:
                    if not is_walkable(grid_map, nx, ny):
                        # 맵 경계가 아닌 벽이면 이것을 시작점으로
                        if not (nx == 0 or nx == map_width - 1 or ny == 0 or ny == map_height - 1):
                            gx, gy = nx, ny
                            break
        
        # BFS로 연결된 모든 장애물 타일 찾기
        obstacle_tiles = set()
        queue = [(gx, gy)]
        visited = {(gx, gy)}
        
        while queue:
            x, y = queue.pop(0)
            
            # 맵 경계는 제외
            if x == 0 or x == map_width - 1 or y == 0 or y == map_height - 1:
                continue
            
            # 벽이면 추가
            if not is_walkable(grid_map, x, y):
                obstacle_tiles.add((x, y))
                
                # 4방향 탐색
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < map_width and 0 <= ny < map_height:
                        if (nx, ny) not in visited:
                            visited.add((nx, ny))
                            queue.append((nx, ny))
        
        return obstacle_tiles
    
    def _distance(self, p1, p2):
        """유클리드 거리"""
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


class TangentBugPlanner:
    """Tangent Bug 알고리즘 (간소화 버전)"""
    
    def __init__(self, sensor_range=10):
        self.state = 'go_to_goal'
        self.sensor_range = sensor_range
        self.tangent_point = None  # 시각화용
    
    def plan_step(self, current_pos, goal_pos, grid_map):
        """한 스텝 계획"""
        gx, gy = current_pos
        goal_gx, goal_gy = goal_pos
        
        # 목표 도달
        if (gx, gy) == (goal_gx, goal_gy):
            return current_pos
        
        # 목표까지 시야 확보되면 직진
        if line_of_sight(grid_map, current_pos, goal_pos):
            next_pos = self._move_towards(current_pos, goal_pos)
            # 다음 위치가 갈 수 있는지 확인
            if is_walkable(grid_map, next_pos[0], next_pos[1]):
                self.tangent_point = None
                return next_pos
            else:
                # 막혔으면 다른 방향으로 우회
                neighbors = get_neighbors(gx, gy, grid_map, diagonal=True)
                if neighbors:
                    return min(neighbors, key=lambda n: self._distance(n, goal_pos))
                return current_pos
        
        # Tangent 포인트 찾기
        tangent_point = self._find_tangent_point(current_pos, goal_pos, grid_map)
        self.tangent_point = tangent_point  # 시각화용 저장
        
        if tangent_point and tangent_point != current_pos:
            next_pos = self._move_towards(current_pos, tangent_point)
            # 다음 위치가 갈 수 있는지 확인
            if is_walkable(grid_map, next_pos[0], next_pos[1]):
                return next_pos
            else:
                # Tangent point로 가는 길이 막혔으면 우회
                neighbors = get_neighbors(gx, gy, grid_map, diagonal=True)
                if neighbors:
                    return min(neighbors, key=lambda n: self._distance(n, tangent_point))
                return current_pos
        else:
            # Tangent 못 찾으면 벽을 따라 이동
            neighbors = get_neighbors(gx, gy, grid_map, diagonal=True)
            if neighbors:
                # 벽과 인접하면서 목표에 가까운 방향
                best = min(neighbors, key=lambda n: (
                    self._distance(n, goal_pos),
                    -sum(1 for dy in [-1, 0, 1] for dx in [-1, 0, 1]
                         if not is_walkable(grid_map, n[0] + dx, n[1] + dy))
                ))
                return best
            return current_pos
    
    def _find_tangent_point(self, current_pos, goal_pos, grid_map):
        """Tangent 포인트 찾기 (센서 범위 내 장애물 모서리)"""
        gx, gy = current_pos
        candidates = set()  # 중복 제거를 위해 set 사용
        
        for dy in range(-self.sensor_range, self.sensor_range + 1):
            for dx in range(-self.sensor_range, self.sensor_range + 1):
                nx, ny = gx + dx, gy + dy
                
                # 범위 체크 및 장애물인지 확인
                if not is_walkable(grid_map, nx, ny):
                    # 장애물 주변의 빈 공간 찾기
                    for neighbor in get_neighbors(nx, ny, grid_map, diagonal=True):
                        # 현재 위치에서 시야가 확보되는 지점
                        if line_of_sight(grid_map, current_pos, neighbor):
                            candidates.add(neighbor)
        
        # 목표로 가는 방향에 있는 tangent point 선택
        if candidates:
            # 목표 방향으로 가장 많이 진전되는 점 선택
            goal_dir_x = goal_pos[0] - gx
            goal_dir_y = goal_pos[1] - gy
            goal_dist = math.sqrt(goal_dir_x**2 + goal_dir_y**2)
            
            if goal_dist > 0:
                goal_dir_x /= goal_dist
                goal_dir_y /= goal_dist
                
                best = max(candidates, key=lambda p: 
                    # 목표 방향으로의 투영 (progress toward goal)
                    (p[0] - gx) * goal_dir_x + (p[1] - gy) * goal_dir_y
                )
                return best
            else:
                return min(candidates, key=lambda p: self._distance(p, goal_pos))
        
        return None
    
    def _move_towards(self, current, goal):
        """목표를 향해 한 칸 이동"""
        dx = goal[0] - current[0]
        dy = goal[1] - current[1]
        
        if abs(dx) > abs(dy):
            return (current[0] + (1 if dx > 0 else -1), current[1])
        elif dy != 0:
            return (current[0], current[1] + (1 if dy > 0 else -1))
        else:
            return current
    
    def _distance(self, p1, p2):
        """유클리드 거리"""
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
