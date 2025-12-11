"""
RRT (Rapidly-exploring Random Tree) 알고리즘
트리 기반 경로 탐색
"""

import numpy as np
import random
import math
from game.grid import is_valid_grid, is_walkable, line_of_sight, distance_grid


class RRTPlanner:
    """RRT 플래너"""
    
    def __init__(self, max_iterations=500, step_size=2.0, goal_sample_rate=0.15):
        self.max_iterations = max_iterations
        self.step_size = step_size
        self.goal_sample_rate = goal_sample_rate
        
        # 트리 구조
        self.nodes = []  # [(x, y), ...]
        self.parents = []  # [parent_idx, ...]
        self.start_idx = None
        self.goal_idx = None
    
    def plan_path(self, start_pos, goal_pos, grid_map):
        """RRT 경로 계획"""
        # 트리 초기화
        self.nodes = [start_pos]
        self.parents = [-1]  # 루트는 부모 없음
        self.start_idx = 0
        self.goal_idx = None
        
        height, width = grid_map.shape
        
        # RRT 메인 루프
        for i in range(self.max_iterations):
            # 1. 랜덤 샘플링 (goal-biased)
            if random.random() < self.goal_sample_rate:
                random_point = goal_pos
            else:
                random_point = (
                    random.randint(1, width - 2),
                    random.randint(1, height - 2)
                )
            
            # 2. 가장 가까운 노드 찾기
            nearest_idx = self._find_nearest(random_point)
            nearest_node = self.nodes[nearest_idx]
            
            # 3. 새 노드 생성 (step_size만큼 이동)
            new_node = self._steer(nearest_node, random_point)
            
            # 4. 충돌 검사
            if not is_walkable(grid_map, new_node[0], new_node[1]):
                continue
            
            if not line_of_sight(grid_map, nearest_node, new_node):
                continue
            
            # 5. 트리에 추가
            new_idx = len(self.nodes)
            self.nodes.append(new_node)
            self.parents.append(nearest_idx)
            
            # 6. 목표 도달 체크
            if distance_grid(new_node, goal_pos) < self.step_size * 2:
                # 목표까지 직접 연결 시도
                if line_of_sight(grid_map, new_node, goal_pos):
                    goal_idx = len(self.nodes)
                    self.nodes.append(goal_pos)
                    self.parents.append(new_idx)
                    self.goal_idx = goal_idx
                    break
        
        # 경로 추출
        if self.goal_idx is not None:
            return self._extract_path()
        
        # 목표에 도달하지 못했다면, 가장 가까운 노드까지의 경로
        closest_idx = self._find_nearest(goal_pos)
        return self._extract_path_to(closest_idx)
    
    def _find_nearest(self, point):
        """가장 가까운 노드 찾기"""
        min_dist = float('inf')
        nearest_idx = 0
        
        for i, node in enumerate(self.nodes):
            dist = distance_grid(node, point)
            if dist < min_dist:
                min_dist = dist
                nearest_idx = i
        
        return nearest_idx
    
    def _steer(self, from_node, to_node):
        """from_node에서 to_node 방향으로 step_size만큼 이동"""
        dx = to_node[0] - from_node[0]
        dy = to_node[1] - from_node[1]
        dist = math.sqrt(dx * dx + dy * dy)
        
        if dist < self.step_size:
            return to_node
        
        # 정규화 후 step_size만큼 이동
        ratio = self.step_size / dist
        new_x = int(from_node[0] + dx * ratio)
        new_y = int(from_node[1] + dy * ratio)
        
        return (new_x, new_y)
    
    def _extract_path(self):
        """목표까지의 경로 추출"""
        if self.goal_idx is None:
            return []
        
        return self._extract_path_to(self.goal_idx)
    
    def _extract_path_to(self, target_idx):
        """특정 노드까지의 경로 추출"""
        path = []
        current = target_idx
        
        while current != -1:
            path.append(self.nodes[current])
            current = self.parents[current]
        
        return list(reversed(path))
    
    def get_tree_for_visualization(self):
        """시각화용 트리 데이터"""
        edges = []
        for i, parent_idx in enumerate(self.parents):
            if parent_idx != -1:
                edges.append((self.nodes[parent_idx], self.nodes[i]))
        return self.nodes, edges
