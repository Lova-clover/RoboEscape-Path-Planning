"""
메인 게임 엔진
"""

import pygame
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, COLOR_BLACK, COLOR_WHITE,
    COLOR_DARK_GRAY, TILE_WALL, TILE_TEMP_WALL, TILE_KEY, TILE_EXIT,
    STAGE_TIME_LIMIT, DEBUG_SHOW_GRID, DEBUG_SHOW_PATHS
)
from game.level import Level
from game.player import Player
from game.ui import UI
from game.particles import ParticleSystem
from game.sound import SoundSystem
from game.grid import grid_to_world, world_to_grid
from game.enemies.bug import Bug1Enemy, Bug2Enemy, TangentBugEnemy
from game.enemies.apf import APFEnemy
from game.enemies.prm_rrt import PRMEnemy, RRTEnemy
from game.enemies.belief import BeliefEnemy
from game.menu import MainMenu, HelpScreen


class GameState:
    """게임 상태"""
    MENU = 0
    HELP = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4
    STAGE_CLEAR = 5


class Game:
    """메인 게임 클래스"""
    
    def __init__(self, screen):
        self.screen = screen
        self.state = GameState.MENU
        self.stage_num = 1
        
        # 메뉴
        self.main_menu = MainMenu()
        self.help_screen = HelpScreen()
        
        # 게임 오브젝트
        self.level = None
        self.player = None
        self.enemies = []
        self.ui = UI()
        self.particles = ParticleSystem()
        self.sound = SoundSystem()
        
        # 사운드 로드
        self.sound.load_sounds()
        
        # 타이머
        self.time_left = STAGE_TIME_LIMIT
        
        # 카메라
        self.camera_x = 0
        self.camera_y = 0
    
    def init_stage(self):
        """스테이지 초기화"""
        # 레벨 생성
        self.level = Level(self.stage_num)
        
        # 플레이어 생성
        spawn_x, spawn_y = grid_to_world(
            self.level.spawn_pos[0],
            self.level.spawn_pos[1]
        )
        self.player = Player(spawn_x, spawn_y)
        
        # 적 생성 (스테이지별 구성)
        self.enemies = []
        self._spawn_enemies()
        
        # 파티클 클리어
        self.particles.clear()
        
        # 타이머 리셋
        self.time_left = STAGE_TIME_LIMIT
        
        # 게임 상태
        self.state = GameState.PLAYING
    
    def _spawn_enemies(self):
        """적 스폰 (스테이지별)"""
        if self.stage_num == 1:
            # Stage 1: Bug1 튜토리얼 - 기본 추격 학습
            self._safe_spawn(Bug1Enemy, 15, 10)
            self._safe_spawn(Bug1Enemy, 25, 12)
            self._safe_spawn(Bug1Enemy, 20, 8)
        elif self.stage_num == 2:
            # Stage 2: Bug 변형들 - 다양한 추격 패턴
            self._safe_spawn(Bug1Enemy, 12, 8)
            self._safe_spawn(Bug2Enemy, 20, 15)
            self._safe_spawn(TangentBugEnemy, 28, 10)
        
        elif self.stage_num == 3:
            # Stage 3: APF 등장 - 로컬 미니멈 활용
            self._safe_spawn(Bug2Enemy, 15, 8)
            self._safe_spawn(Bug2Enemy, 32, 18)
            self._safe_spawn(APFEnemy, 20, 15)
            self._safe_spawn(APFEnemy, 30, 10)
            self._safe_spawn(TangentBugEnemy, 25, 8)
        
        elif self.stage_num == 4:
            # Stage 4: Sampling-based - 그래프/트리 경로
            self._safe_spawn(Bug2Enemy, 10, 6)
            self._safe_spawn(TangentBugEnemy, 12, 8)
            self._safe_spawn_prm(20, 15)
            self._safe_spawn(RRTEnemy, 28, 12)
            self._safe_spawn(APFEnemy, 35, 10)
            self._safe_spawn(APFEnemy, 38, 18)
        
        elif self.stage_num == 5:
            # Stage 5: Belief 등장 - 확률적 추적
            self._safe_spawn(Bug2Enemy, 12, 8)
            self._safe_spawn(TangentBugEnemy, 10, 18)
            self._safe_spawn(APFEnemy, 18, 15)
            self._safe_spawn(BeliefEnemy, 25, 10)
            self._safe_spawn(RRTEnemy, 32, 12)
            self._safe_spawn(BeliefEnemy, 38, 16)
            self._safe_spawn_prm(35, 8)
        
        elif self.stage_num == 6:
            # Stage 6: 보스전 - 모든 알고리즘 총동원!
            # 외곽에 배치
            self._safe_spawn(Bug1Enemy, 10, 6)
            self._safe_spawn(Bug2Enemy, 35, 6)
            self._safe_spawn(TangentBugEnemy, 10, 18)
            self._safe_spawn(APFEnemy, 35, 18)
            self._safe_spawn_prm(15, 11)
            self._safe_spawn(RRTEnemy, 30, 11)
            self._safe_spawn(BeliefEnemy, 22, 8)
            self._safe_spawn(BeliefEnemy, 22, 16)
        
        else:
            # Stage 7+: 무한 난이도 상승
            num_enemies = min(3 + self.stage_num, 12)
            for i in range(num_enemies):
                enemy_type = i % 7
                spawn_x = 10 + (i * 4) % 28
                spawn_y = 6 + (i * 2) % 14
                
                if enemy_type == 0:
                    self.enemies.append(Bug1Enemy(*grid_to_world(spawn_x, spawn_y)))
                elif enemy_type == 1:
                    self.enemies.append(Bug2Enemy(*grid_to_world(spawn_x, spawn_y)))
                elif enemy_type == 2:
                    self.enemies.append(TangentBugEnemy(*grid_to_world(spawn_x, spawn_y)))
                elif enemy_type == 3:
                    self.enemies.append(APFEnemy(*grid_to_world(spawn_x, spawn_y)))
                elif enemy_type == 4:
                    self.enemies.append(PRMEnemy(*grid_to_world(spawn_x, spawn_y), self.level.grid_map))
                elif enemy_type == 5:
                    self.enemies.append(RRTEnemy(*grid_to_world(spawn_x, spawn_y)))
                else:
                    self.enemies.append(BeliefEnemy(*grid_to_world(spawn_x, spawn_y)))
    
    def _safe_spawn(self, enemy_class, grid_x, grid_y):
        """벽을 피해서 적을 안전하게 스폰"""
        # 먼저 지정된 위치가 안전한지 확인
        if self.level.grid_map[grid_y][grid_x] == 0:
            self.enemies.append(enemy_class(*grid_to_world(grid_x, grid_y)))
            return
        
        # 안전하지 않으면 가까운 안전한 위치 찾기 (BFS)
        from collections import deque
        visited = set()
        queue = deque([(grid_x, grid_y, 0)])
        visited.add((grid_x, grid_y))
        
        while queue:
            cx, cy, dist = queue.popleft()
            
            # 8방향 확인 (대각선 포함)
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]:
                nx, ny = cx + dx, cy + dy
                
                if (nx, ny) in visited:
                    continue
                if nx < 0 or nx >= 40 or ny < 0 or ny >= 22:
                    continue
                    
                visited.add((nx, ny))
                
                # 안전한 위치 발견
                if self.level.grid_map[ny][nx] == 0:
                    self.enemies.append(enemy_class(*grid_to_world(nx, ny)))
                    return
                
                # 계속 탐색 (최대 5칸까지만)
                if dist < 5:
                    queue.append((nx, ny, dist + 1))
        
        # 안전한 위치를 찾지 못하면 원래 위치에 스폰 (플레이어 시작 위치로)
        px, py = world_to_grid(*self.player.pos)
        self.enemies.append(enemy_class(*grid_to_world(px + 2, py)))
    
    def _safe_spawn_prm(self, grid_x, grid_y):
        """PRM은 grid_map이 필요하므로 별도 메서드"""
        if self.level.grid_map[grid_y][grid_x] == 0:
            self.enemies.append(PRMEnemy(*grid_to_world(grid_x, grid_y), self.level.grid_map))
            return
        
        # BFS로 안전한 위치 찾기
        from collections import deque
        visited = set()
        queue = deque([(grid_x, grid_y, 0)])
        visited.add((grid_x, grid_y))
        
        while queue:
            cx, cy, dist = queue.popleft()
            
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]:
                nx, ny = cx + dx, cy + dy
                
                if (nx, ny) in visited:
                    continue
                if nx < 0 or nx >= 40 or ny < 0 or ny >= 22:
                    continue
                    
                visited.add((nx, ny))
                
                if self.level.grid_map[ny][nx] == 0:
                    self.enemies.append(PRMEnemy(*grid_to_world(nx, ny), self.level.grid_map))
                    return
                
                if dist < 5:
                    queue.append((nx, ny, dist + 1))
        
        px, py = world_to_grid(*self.player.pos)
        self.enemies.append(PRMEnemy(*grid_to_world(px + 2, py), self.level.grid_map))
    
    def handle_event(self, event):
        """이벤트 처리"""
        # 메뉴 상태
        if self.state == GameState.MENU:
            mouse_pos = pygame.mouse.get_pos()
            action = self.main_menu.handle_event(event, mouse_pos)
            if action == "start":
                self.stage_num = 1
                self.init_stage()
            elif action == "help":
                self.state = GameState.HELP
            elif action == "exit":
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            return
        
        # 도움말 상태
        if self.state == GameState.HELP:
            mouse_pos = pygame.mouse.get_pos()
            action = self.help_screen.handle_event(event, mouse_pos)
            if action == "back":
                self.state = GameState.MENU
            return
        
        if event.type == pygame.KEYDOWN:
            # ESC: 일시정지/재개
            if event.key == pygame.K_ESCAPE:
                if self.state == GameState.PLAYING:
                    self.state = GameState.PAUSED
                elif self.state == GameState.PAUSED:
                    self.state = GameState.PLAYING
            
            # 게임 오버/클리어 상태
            if self.state in [GameState.GAME_OVER, GameState.STAGE_CLEAR]:
                if event.key == pygame.K_r:
                    # 재시작 또는 다음 스테이지
                    if self.state == GameState.STAGE_CLEAR and self.stage_num < 10:
                        self.stage_num += 1  # 다음 스테이지
                    else:
                        self.stage_num = 1  # 처음부터
                    self.init_stage()
                elif event.key == pygame.K_ESCAPE:
                    # 메뉴로 돌아가기
                    self.state = GameState.MENU
            
            # 플레이 중 스킬 사용
            if self.state == GameState.PLAYING:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    if self.player.try_dash():
                        # 대시 이펙트
                        self.particles.emit_dash_trail(self.player.x, self.player.y, 
                                                      (0, 255, 255))
                        self.sound.play_sound('dash')
                elif event.key == pygame.K_e:
                    if self.player.try_wall_skill(self.level):
                        # 장벽 설치 이펙트
                        self.particles.emit_wall_place(self.player.x, self.player.y)
                        self.sound.play_sound('wall')
                elif event.key == pygame.K_q:
                    if self.player.try_noise_skill():
                        # 노이즈 효과
                        self.particles.emit_burst(self.player.x, self.player.y, 30,
                                                 (255, 255, 100), speed_range=(150, 300))
                        self.sound.play_sound('noise')
                        # Belief 적들에게 노이즈 적용
                        for enemy in self.enemies:
                            if isinstance(enemy, BeliefEnemy):
                                enemy.apply_noise_effect(3.0)
                elif event.key == pygame.K_SPACE:
                    self.player.try_slowmo_skill()
    
    def update(self, dt):
        """게임 업데이트"""
        # 메뉴 업데이트
        if self.state == GameState.MENU:
            mouse_pos = pygame.mouse.get_pos()
            self.main_menu.update(dt, mouse_pos)
            return
        
        # 도움말 화면 업데이트
        if self.state == GameState.HELP:
            mouse_pos = pygame.mouse.get_pos()
            self.help_screen.update(dt, mouse_pos)
            return
        
        if self.state != GameState.PLAYING:
            return
        
        # 타이머 감소
        self.time_left -= dt
        if self.time_left <= 0:
            self.state = GameState.GAME_OVER
            return
        
        # 플레이어 입력
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        
        # 플레이어 업데이트
        self.player.update(dt, self.level)
        
        # 레벨 업데이트
        self.level.update(dt)
        
        # 열쇠 수집 체크
        player_gx, player_gy = world_to_grid(self.player.x, self.player.y)
        if self.level.collect_key(player_gx, player_gy):
            # 열쇠 수집 이펙트
            self.particles.emit_key_collect(self.player.x, self.player.y)
            self.sound.play_sound('key')
        
        # 출구 도달 체크
        if self.level.can_exit():
            exit_gx, exit_gy = self.level.exit_pos
            dist = abs(player_gx - exit_gx) + abs(player_gy - exit_gy)
            if dist < 2:
                self.state = GameState.STAGE_CLEAR
                self.sound.play_sound('clear')
                return
        
        # 적 업데이트
        for enemy in self.enemies:
            enemy.update(dt, self.player, self.level)
            
            # 충돌 체크
            if enemy.collides_with(self.player):
                if self.player.take_damage():
                    # 피격 이펙트
                    self.particles.emit_hit_effect(self.player.x, self.player.y)
                    self.sound.play_sound('hit')
                    
                    if not self.player.is_alive():
                        self.state = GameState.GAME_OVER
                        self.sound.play_sound('game_over')
                        return
        
        # 파티클 업데이트
        self.particles.update(dt)
        
        # 대시 트레일 자동 생성
        if self.player.is_dashing:
            self.particles.emit_dash_trail(self.player.x, self.player.y, (0, 255, 255))
        
        # 카메라 업데이트 (플레이어 중심)
        self.camera_x = self.player.x - SCREEN_WIDTH // 2
        self.camera_y = self.player.y - SCREEN_HEIGHT // 2
        
        # 카메라 경계 제한
        self.camera_x = max(0, min(self.camera_x, SCREEN_WIDTH - SCREEN_WIDTH))
        self.camera_y = max(0, min(self.camera_y, SCREEN_HEIGHT - SCREEN_HEIGHT))
    
    def draw(self):
        """게임 그리기"""
        # 배경
        self.screen.fill(COLOR_BLACK)
        
        # 메뉴 화면
        if self.state == GameState.MENU:
            self.main_menu.draw(self.screen)
            return
        
        # 도움말 화면
        if self.state == GameState.HELP:
            self.help_screen.draw(self.screen)
            return
        
        if self.state == GameState.PLAYING:
            # 레벨 그리기
            self._draw_level()
            
            # 파티클 그리기 (배경층)
            self.particles.draw(self.screen, (self.camera_x, self.camera_y))
            
            # 플레이어 그리기
            self.player.draw(self.screen, (self.camera_x, self.camera_y))
            
            # 적 그리기
            for enemy in self.enemies:
                enemy.draw(self.screen, (self.camera_x, self.camera_y))
                if DEBUG_SHOW_PATHS:
                    enemy.draw_path(self.screen, (self.camera_x, self.camera_y))
            
            # UI 그리기
            self.ui.draw_hud(self.screen, self.player, self.level, self.time_left, self)
        
        elif self.state == GameState.PAUSED:
            # 일시정지 화면
            self._draw_level()
            self.player.draw(self.screen, (self.camera_x, self.camera_y))
            for enemy in self.enemies:
                enemy.draw(self.screen, (self.camera_x, self.camera_y))
            self.ui.draw_pause(self.screen)
        
        elif self.state in [GameState.GAME_OVER, GameState.STAGE_CLEAR]:
            # 게임 오버/클리어 화면
            self._draw_level()
            self.player.draw(self.screen, (self.camera_x, self.camera_y))
            for enemy in self.enemies:
                enemy.draw(self.screen, (self.camera_x, self.camera_y))
            
            won = self.state == GameState.STAGE_CLEAR
            self.ui.draw_game_over(self.screen, won, self.player.stats, self.stage_num)
    
    def _draw_level(self):
        """레벨 그리기"""
        # 타일 그리기
        for gy in range(self.level.grid_map.shape[0]):
            for gx in range(self.level.grid_map.shape[1]):
                tile = self.level.grid_map[gy][gx]
                
                if tile == 0:  # 빈 공간
                    continue
                
                # 화면 좌표
                screen_x = gx * TILE_SIZE - self.camera_x
                screen_y = gy * TILE_SIZE - self.camera_y
                
                # 화면 밖이면 스킵
                if screen_x + TILE_SIZE < 0 or screen_x > SCREEN_WIDTH:
                    continue
                if screen_y + TILE_SIZE < 0 or screen_y > SCREEN_HEIGHT:
                    continue
                
                # 타일 색상
                if tile == TILE_WALL:
                    color = COLOR_DARK_GRAY
                elif tile == TILE_TEMP_WALL:
                    color = (100, 100, 200)  # 파란 장벽
                elif tile == TILE_KEY:
                    color = (255, 255, 0)  # 노랑 열쇠
                elif tile == TILE_EXIT:
                    color = (0, 255, 0) if self.level.can_exit() else (100, 100, 100)
                else:
                    color = COLOR_WHITE
                
                # 타일 그리기
                pygame.draw.rect(self.screen, color, 
                               (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
                
                # 그리드 선 (디버그)
                if DEBUG_SHOW_GRID:
                    pygame.draw.rect(self.screen, (80, 80, 80),
                                   (screen_x, screen_y, TILE_SIZE, TILE_SIZE), 1)
