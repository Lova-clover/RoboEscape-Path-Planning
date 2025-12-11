"""
PRM (Probabilistic Roadmap) 알고리즘
그래프 기반 경로 계획
"""

import numpy as np
import random
import math
from collections import defaultdict
from game.grid import is_valid_grid, is_walkable, line_of_sight, distance_grid


class PRMPlanner:
    """Probabilistic Roadmap 플래너"""
    
    def __init__(self, num_samples=150, connection_radius=8.0, max_neighbors=8):
        self.num_samples = num_samples
        self.connection_radius = connection_radius
        self.max_neighbors = max_neighbors
        
        # 그래프 구조
        self.nodes = []  # 샘플링된 노드들 (gx, gy)
        self.graph = defaultdict(list)  # 인접 리스트
        self.is_built = False
    
    def build_roadmap(self, grid_map):
        """로드맵 구축 (맵 로딩 시 한 번만)"""
        self.nodes = []
        self.graph = defaultdict(list)
        
        height, width = grid_map.shape
        
        # 1. 노드 샘플링
        attempts = 0
        max_attempts = self.num_samples * 10
        
        while len(self.nodes) < self.num_samples and attempts < max_attempts:
            x = random.randint(1, width - 2)
            y = random.randint(1, height - 2)
            
            if is_walkable(grid_map, x, y):
                self.nodes.append((x, y))
            
            attempts += 1
        
        # 2. 노드 연결 (k-nearest neighbors)
        for i, node in enumerate(self.nodes):
            # 거리 계산
            distances = []
            for j, other in enumerate(self.nodes):
                if i != j:
                    dist = distance_grid(node, other)
                    if dist <= self.connection_radius:
                        distances.append((dist, j))
            
            # 가까운 순으로 정렬
            distances.sort()
            
            # 최대 max_neighbors개까지 연결
            for dist, j in distances[:self.max_neighbors]:
                other = self.nodes[j]
                
                # 장애물 충돌 검사
                if line_of_sight(grid_map, node, other):
                    self.graph[i].append(j)
                    self.graph[j].append(i)  # 양방향
        
        self.is_built = True
    
    def find_nearest_node(self, pos):
        """주어진 위치에 가장 가까운 노드 찾기"""
        if not self.nodes:
            return None
        
        min_dist = float('inf')
        nearest = None
        nearest_idx = None
        
        for i, node in enumerate(self.nodes):
            dist = distance_grid(pos, node)
            if dist < min_dist:
                min_dist = dist
                nearest = node
                nearest_idx = i
        
        return nearest_idx, nearest
    
    def a_star(self, start_idx, goal_idx):
        """A* 알고리즘으로 그래프에서 경로 찾기"""
        if start_idx is None or goal_idx is None:
            return []
        
        from heapq import heappush, heappop
        
        # 오픈/클로즈드 리스트
        open_set = []
        heappush(open_set, (0, start_idx))
        
        came_from = {}
        g_score = {start_idx: 0}
        f_score = {start_idx: distance_grid(self.nodes[start_idx], self.nodes[goal_idx])}
        
        while open_set:
            _, current = heappop(open_set)
            
            if current == goal_idx:
                # 경로 재구성
                path = []
                while current in came_from:
                    path.append(self.nodes[current])
                    current = came_from[current]
                path.append(self.nodes[start_idx])
                return list(reversed(path))
            
            for neighbor in self.graph[current]:
                tentative_g = g_score[current] + distance_grid(
                    self.nodes[current], self.nodes[neighbor]
                )
                
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + distance_grid(
                        self.nodes[neighbor], self.nodes[goal_idx]
                    )
                    heappush(open_set, (f_score[neighbor], neighbor))
        
        return []  # 경로 없음
    
    def plan_path(self, start_pos, goal_pos, grid_map):
        """전체 경로 계획"""
        if not self.is_built:
            self.build_roadmap(grid_map)
        
        # 가장 가까운 노드 찾기
        start_idx, _ = self.find_nearest_node(start_pos)
        goal_idx, _ = self.find_nearest_node(goal_pos)
        
        if start_idx is None or goal_idx is None:
            return []
        
        # A* 실행
        path = self.a_star(start_idx, goal_idx)
        
        # 시작/끝 위치 추가
        if path:
            full_path = [start_pos] + path + [goal_pos]
            return full_path
        
        return []
    
    def get_graph_for_visualization(self):
        """시각화용 그래프 데이터"""
        edges = []
        for node_idx, neighbors in self.graph.items():
            for neighbor_idx in neighbors:
                if node_idx < neighbor_idx:  # 중복 방지
                    edges.append((self.nodes[node_idx], self.nodes[neighbor_idx]))
        return self.nodes, edges
