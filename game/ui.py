"""
UI 및 HUD 시스템
"""

import pygame
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, HUD_MARGIN, HUD_FONT_SIZE,
    COLOR_WHITE, COLOR_RED, COLOR_GREEN, COLOR_BLUE, COLOR_YELLOW,
    COLOR_GRAY, MINIMAP_SIZE, MINIMAP_ALPHA, GRID_WIDTH, GRID_HEIGHT,
    TILE_WALL, TILE_KEY, TILE_EXIT
)


class UI:
    """게임 UI 관리"""
    
    def __init__(self):
        self.font_large = pygame.font.Font(None, HUD_FONT_SIZE + 8)
        self.font_medium = pygame.font.Font(None, HUD_FONT_SIZE)
        self.font_small = pygame.font.Font(None, HUD_FONT_SIZE - 4)
        
        # 미니맵 설정
        self.minimap_enabled = True
        self.show_debug = False
        
    def draw_hud(self, surface, player, level, time_left, game_state):
        """HUD 그리기"""
        # 체력
        self._draw_health(surface, player.health)
        
        # 스킬 쿨타임
        self._draw_skills(surface, player)
        
        # 열쇠 수집 현황
        self._draw_keys(surface, level.keys_collected, level.key_positions)
        
        # 타이머
        self._draw_timer(surface, time_left)
        
        # 미니맵
        if self.minimap_enabled:
            self._draw_minimap(surface, player, level, game_state.enemies)
    
    def _draw_health(self, surface, health):
        """체력 표시"""
        x = HUD_MARGIN
        y = HUD_MARGIN
        
        # 배경
        pygame.draw.rect(surface, (50, 50, 50), (x, y, 150, 30))
        pygame.draw.rect(surface, COLOR_WHITE, (x, y, 150, 30), 2)
        
        # 체력 바
        health_width = 140 * (health / 3)
        pygame.draw.rect(surface, COLOR_RED, (x + 5, y + 5, health_width, 20))
        
        # 텍스트
        text = self.font_medium.render(f"HP: {health}/3", True, COLOR_WHITE)
        surface.blit(text, (x + 10, y + 7))
    
    def _draw_skills(self, surface, player):
        """스킬 쿨타임 표시"""
        x = HUD_MARGIN
        y = HUD_MARGIN + 40
        
        skills = [
            ("Dash [Shift]", player.dash_cooldown, 2.0, COLOR_BLUE),
            ("Wall [E]", player.wall_skill_cooldown, 5.0, COLOR_GREEN),
            ("Noise [Q]", player.noise_skill_cooldown, 10.0, COLOR_YELLOW)
        ]
        
        for i, (name, cooldown, max_cd, color) in enumerate(skills):
            skill_y = y + i * 35
            
            # 배경
            pygame.draw.rect(surface, (50, 50, 50), (x, skill_y, 180, 28))
            pygame.draw.rect(surface, COLOR_WHITE, (x, skill_y, 180, 28), 1)
            
            # 쿨타임 바
            if cooldown > 0:
                cd_ratio = cooldown / max_cd
                cd_width = 170 * cd_ratio
                pygame.draw.rect(surface, COLOR_GRAY, (x + 5, skill_y + 5, cd_width, 18))
            else:
                # 준비 완료
                pygame.draw.rect(surface, color, (x + 5, skill_y + 5, 170, 18))
            
            # 텍스트
            if cooldown > 0:
                text = self.font_small.render(f"{name}: {cooldown:.1f}s", True, COLOR_WHITE)
            else:
                text = self.font_small.render(f"{name}: READY", True, COLOR_WHITE)
            surface.blit(text, (x + 10, skill_y + 7))
    
    def _draw_keys(self, surface, collected, remaining_positions):
        """열쇠 수집 현황"""
        x = SCREEN_WIDTH - 200
        y = HUD_MARGIN
        
        # 배경
        pygame.draw.rect(surface, (50, 50, 50), (x, y, 190, 40))
        pygame.draw.rect(surface, COLOR_WHITE, (x, y, 190, 40), 2)
        
        # 텍스트
        text = self.font_medium.render(f"Keys: {collected}/3", True, COLOR_YELLOW)
        surface.blit(text, (x + 10, y + 10))
        
        # 열쇠 아이콘
        for i in range(3):
            icon_x = x + 110 + i * 25
            icon_y = y + 12
            if i < collected:
                pygame.draw.circle(surface, COLOR_YELLOW, (icon_x, icon_y), 8)
            else:
                pygame.draw.circle(surface, COLOR_GRAY, (icon_x, icon_y), 8)
            pygame.draw.circle(surface, COLOR_WHITE, (icon_x, icon_y), 8, 1)
    
    def _draw_timer(self, surface, time_left):
        """타이머"""
        x = SCREEN_WIDTH // 2 - 60
        y = HUD_MARGIN
        
        # 배경
        pygame.draw.rect(surface, (50, 50, 50), (x, y, 120, 35))
        pygame.draw.rect(surface, COLOR_WHITE, (x, y, 120, 35), 2)
        
        # 시간 색상 (30초 이하면 빨강)
        color = COLOR_RED if time_left < 30 else COLOR_WHITE
        
        # 텍스트
        minutes = int(time_left // 60)
        seconds = int(time_left % 60)
        text = self.font_large.render(f"{minutes}:{seconds:02d}", True, color)
        text_rect = text.get_rect(center=(x + 60, y + 17))
        surface.blit(text, text_rect)
    
    def _draw_minimap(self, surface, player, level, enemies):
        """미니맵"""
        size = MINIMAP_SIZE
        x = SCREEN_WIDTH - size - HUD_MARGIN
        y = SCREEN_HEIGHT - size - HUD_MARGIN
        
        # 반투명 배경
        minimap_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        minimap_surface.fill((30, 30, 40, MINIMAP_ALPHA))
        
        # 스케일 계산
        scale_x = size / GRID_WIDTH
        scale_y = size / GRID_HEIGHT
        
        # 맵 그리기
        for gy in range(GRID_HEIGHT):
            for gx in range(GRID_WIDTH):
                tile = level.grid_map[gy][gx]
                mx = int(gx * scale_x)
                my = int(gy * scale_y)
                
                if tile == TILE_WALL:
                    pygame.draw.rect(minimap_surface, COLOR_GRAY, 
                                   (mx, my, max(2, int(scale_x)), max(2, int(scale_y))))
                elif tile == TILE_KEY:
                    pygame.draw.circle(minimap_surface, COLOR_YELLOW,
                                     (mx + int(scale_x/2), my + int(scale_y/2)), 3)
                elif tile == TILE_EXIT:
                    pygame.draw.rect(minimap_surface, COLOR_GREEN,
                                   (mx, my, max(3, int(scale_x)), max(3, int(scale_y))))
        
        # 적 표시
        for enemy in enemies:
            ex = int(enemy.x / SCREEN_WIDTH * GRID_WIDTH * scale_x)
            ey = int(enemy.y / SCREEN_HEIGHT * GRID_HEIGHT * scale_y)
            pygame.draw.circle(minimap_surface, enemy.color, (ex, ey), 3)
        
        # 플레이어 표시
        px = int(player.x / SCREEN_WIDTH * GRID_WIDTH * scale_x)
        py = int(player.y / SCREEN_HEIGHT * GRID_HEIGHT * scale_y)
        pygame.draw.circle(minimap_surface, COLOR_GREEN, (px, py), 4)
        pygame.draw.circle(minimap_surface, COLOR_WHITE, (px, py), 4, 1)
        
        # 테두리
        pygame.draw.rect(minimap_surface, COLOR_WHITE, (0, 0, size, size), 2)
        
        # 표면에 그리기
        surface.blit(minimap_surface, (x, y))
    
    def draw_game_over(self, surface, won, stats, stage_num):
        """게임 오버 화면"""
        # 반투명 오버레이
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))
        
        # 결과 텍스트
        if won:
            if stage_num == 6:
                title = self.font_large.render("🏆 BOSS DEFEATED! 🏆", True, COLOR_YELLOW)
                subtitle = self.font_medium.render("You are a Path-Planning Master!", True, COLOR_GREEN)
            else:
                title = self.font_large.render(f"STAGE {stage_num} CLEAR!", True, COLOR_GREEN)
                subtitle = self.font_medium.render(f"Stage {stage_num + 1} Unlocked!", True, COLOR_WHITE)
        else:
            title = self.font_large.render("GAME OVER", True, COLOR_RED)
            subtitle = self.font_medium.render(f"Failed at Stage {stage_num}", True, COLOR_GRAY)
        
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 130))
        surface.blit(title, title_rect)
        
        if won:
            subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 90))
            surface.blit(subtitle, subtitle_rect)
        else:
            subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
            surface.blit(subtitle, subtitle_rect)
        
        # 통계
        y_offset = SCREEN_HEIGHT // 2 - 30
        stats_texts = [
            f"Distance Traveled: {stats.get('distance_traveled', 0):.1f}",
            f"Dodges: {stats.get('dodges', 0)}",
            f"Walls Placed: {stats.get('walls_placed', 0)}",
            f"Noise Used: {stats.get('noise_used', 0)}"
        ]
        
        for text_str in stats_texts:
            text = self.font_medium.render(text_str, True, COLOR_WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            surface.blit(text, text_rect)
            y_offset += 35
        
        # 안내 메시지
        if won and stage_num < 6:
            restart_text = self.font_medium.render("Press R for Next Stage or ESC to Quit", True, COLOR_YELLOW)
        else:
            restart_text = self.font_medium.render("Press R to Restart or ESC to Quit", True, COLOR_YELLOW)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 130))
        surface.blit(restart_text, restart_rect)
    
    def draw_pause(self, surface):
        """일시정지 화면"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))
        
        title = self.font_large.render("PAUSED", True, COLOR_WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        surface.blit(title, title_rect)
        
        hint = self.font_medium.render("Press ESC to Resume", True, COLOR_GRAY)
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        surface.blit(hint, hint_rect)
