"""
메인 메뉴 시스템
"""

import pygame
import math
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_WHITE, COLOR_BLACK


class MenuButton:
    """메뉴 버튼 클래스"""
    
    def __init__(self, text, x, y, width, height, action):
        self.text = text
        self.rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
        self.action = action
        self.hovered = False
        self.glow_intensity = 0
        self.scale = 1.0
        
    def update(self, dt, mouse_pos):
        """버튼 업데이트"""
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        # 호버 애니메이션
        target_glow = 1.0 if self.hovered else 0.0
        self.glow_intensity += (target_glow - self.glow_intensity) * 8 * dt
        
        target_scale = 1.1 if self.hovered else 1.0
        self.scale += (target_scale - self.scale) * 10 * dt
    
    def draw(self, surface, font):
        """버튼 그리기"""
        # 스케일 적용된 rect
        scaled_rect = self.rect.inflate(
            int((self.scale - 1.0) * self.rect.width),
            int((self.scale - 1.0) * self.rect.height)
        )
        
        # 외곽 글로우 효과
        if self.glow_intensity > 0:
            glow_color = (
                int(0 + 255 * self.glow_intensity),
                int(200 + 55 * self.glow_intensity),
                int(255 * self.glow_intensity)
            )
            for i in range(3):
                offset = 4 - i
                glow_rect = scaled_rect.inflate(offset * 4, offset * 4)
                alpha = int(100 * self.glow_intensity * (3 - i) / 3)
                glow_surf = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
                pygame.draw.rect(glow_surf, (*glow_color, alpha), glow_surf.get_rect(), border_radius=12)
                surface.blit(glow_surf, glow_rect.topleft)
        
        # 메인 버튼 배경
        bg_color = (40, 50, 70) if not self.hovered else (60, 80, 110)
        pygame.draw.rect(surface, bg_color, scaled_rect, border_radius=10)
        
        # 테두리
        border_color = (100, 150, 255) if self.hovered else (80, 100, 140)
        pygame.draw.rect(surface, border_color, scaled_rect, 3, border_radius=10)
        
        # 내부 빛 효과
        if self.hovered:
            inner_rect = scaled_rect.inflate(-10, -10)
            inner_surf = pygame.Surface((inner_rect.width, inner_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(inner_surf, (100, 180, 255, 30), inner_surf.get_rect(), border_radius=8)
            surface.blit(inner_surf, inner_rect.topleft)
        
        # 텍스트
        text_color = (200, 230, 255) if self.hovered else (180, 200, 220)
        text_surface = font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=scaled_rect.center)
        surface.blit(text_surface, text_rect)
    
    def is_clicked(self, mouse_pos, mouse_pressed):
        """클릭 감지"""
        return self.rect.collidepoint(mouse_pos) and mouse_pressed


class ParticleField:
    """배경 파티클 필드"""
    
    def __init__(self, num_particles=100):
        self.particles = []
        for _ in range(num_particles):
            self.particles.append({
                'x': pygame.math.Vector2(
                    pygame.math.Vector2(0, 0).lerp(
                        pygame.math.Vector2(SCREEN_WIDTH, SCREEN_HEIGHT),
                        pygame.math.Vector2(0.5, 0.5).angle_to(
                            pygame.math.Vector2(1, 1)
                        ) / 360
                    ).x + (hash(_) % SCREEN_WIDTH),
                    (hash(_) % SCREEN_HEIGHT)
                ).x if _ % 2 == 0 else hash(_) % SCREEN_WIDTH,
                'y': (hash(_) % SCREEN_HEIGHT),
                'vx': (hash(_ * 2) % 40 - 20) * 0.5,
                'vy': (hash(_ * 3) % 40 - 20) * 0.5,
                'size': (hash(_ * 4) % 3) + 1,
                'alpha': (hash(_ * 5) % 150) + 50,
                'phase': hash(_ * 6) % 360
            })
    
    def update(self, dt):
        """파티클 업데이트"""
        for p in self.particles:
            p['x'] += p['vx'] * dt * 20
            p['y'] += p['vy'] * dt * 20
            p['phase'] += dt * 100
            
            # 화면 밖으로 나가면 반대편에서 등장
            if p['x'] < -10:
                p['x'] = SCREEN_WIDTH + 10
            elif p['x'] > SCREEN_WIDTH + 10:
                p['x'] = -10
            if p['y'] < -10:
                p['y'] = SCREEN_HEIGHT + 10
            elif p['y'] > SCREEN_HEIGHT + 10:
                p['y'] = -10
    
    def draw(self, surface):
        """파티클 그리기"""
        for p in self.particles:
            # 펄스 효과
            pulse = math.sin(math.radians(p['phase'])) * 0.3 + 0.7
            size = int(p['size'] * pulse)
            alpha = int(p['alpha'] * pulse)
            
            # 파티클 그리기
            color = (100, 150, 255, alpha)
            particle_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, color, (size, size), size)
            surface.blit(particle_surf, (int(p['x']) - size, int(p['y']) - size))


class GridBackground:
    """그리드 배경 효과"""
    
    def __init__(self):
        self.offset_x = 0
        self.offset_y = 0
        self.grid_size = 40
    
    def update(self, dt):
        """그리드 애니메이션"""
        self.offset_x = (self.offset_x + dt * 10) % self.grid_size
        self.offset_y = (self.offset_y + dt * 10) % self.grid_size
    
    def draw(self, surface):
        """그리드 그리기"""
        # 수평선
        for i in range(int(SCREEN_HEIGHT / self.grid_size) + 2):
            y = int(i * self.grid_size - self.offset_y)
            alpha = 20
            pygame.draw.line(surface, (100, 150, 255, alpha), (0, y), (SCREEN_WIDTH, y), 1)
        
        # 수직선
        for i in range(int(SCREEN_WIDTH / self.grid_size) + 2):
            x = int(i * self.grid_size - self.offset_x)
            alpha = 20
            pygame.draw.line(surface, (100, 150, 255, alpha), (x, 0), (x, SCREEN_HEIGHT), 1)


class MainMenu:
    """메인 메뉴"""
    
    def __init__(self):
        # 폰트
        self.title_font = pygame.font.Font(None, 120)
        self.subtitle_font = pygame.font.Font(None, 48)
        self.button_font = pygame.font.Font(None, 42)
        self.info_font = pygame.font.Font(None, 28)
        
        # 버튼
        center_x = SCREEN_WIDTH // 2
        button_width = 300
        button_height = 70
        button_spacing = 90
        start_y = SCREEN_HEIGHT // 2 + 50
        
        self.buttons = [
            MenuButton("START GAME", center_x, start_y, button_width, button_height, "start"),
            MenuButton("HOW TO PLAY", center_x, start_y + button_spacing, button_width, button_height, "help"),
            MenuButton("EXIT", center_x, start_y + button_spacing * 2, button_width, button_height, "exit")
        ]
        
        # 배경 효과
        self.particles = ParticleField(120)
        self.grid = GridBackground()
        
        # 애니메이션 타이머
        self.time = 0
        self.title_glow = 0
        
        # 화면 페이드인
        self.fade_alpha = 255
    
    def update(self, dt, mouse_pos):
        """메뉴 업데이트"""
        self.time += dt
        
        # 배경 업데이트
        self.particles.update(dt)
        self.grid.update(dt)
        
        # 버튼 업데이트
        for button in self.buttons:
            button.update(dt, mouse_pos)
        
        # 타이틀 글로우
        self.title_glow = math.sin(self.time * 2) * 0.5 + 0.5
        
        # 페이드인
        if self.fade_alpha > 0:
            self.fade_alpha = max(0, self.fade_alpha - dt * 300)
    
    def draw(self, surface):
        """메뉴 그리기"""
        # 배경 그라디언트
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            color = (
                int(10 + 15 * ratio),
                int(15 + 25 * ratio),
                int(25 + 35 * ratio)
            )
            pygame.draw.line(surface, color, (0, y), (SCREEN_WIDTH, y))
        
        # 그리드 배경
        self.grid.draw(surface)
        
        # 파티클 필드
        self.particles.draw(surface)
        
        # 대형 장식 요소
        self._draw_decorations(surface)
        
        # 타이틀
        self._draw_title(surface)
        
        # 버튼
        for button in self.buttons:
            button.draw(surface, self.button_font)
        
        # 하단 정보
        self._draw_footer(surface)
        
        # 페이드인 효과
        if self.fade_alpha > 0:
            fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            fade_surface.fill((0, 0, 0, int(self.fade_alpha)))
            surface.blit(fade_surface, (0, 0))
    
    def _draw_title(self, surface):
        """타이틀 그리기"""
        # 메인 타이틀
        title_text = "ROBOESCAPE"
        subtitle_text = "Algorithm Hunters"
        
        # 타이틀 글로우 효과
        glow_intensity = int(100 * self.title_glow)
        glow_color = (0 + glow_intensity, 200 + glow_intensity // 2, 255)
        
        # 외부 글로우
        for offset in [(0, 4), (0, -4), (4, 0), (-4, 0), (3, 3), (-3, -3), (3, -3), (-3, 3)]:
            glow_surf = self.title_font.render(title_text, True, glow_color)
            glow_surf.set_alpha(30 + glow_intensity // 3)
            glow_rect = glow_surf.get_rect(center=(SCREEN_WIDTH // 2 + offset[0], 150 + offset[1]))
            surface.blit(glow_surf, glow_rect)
        
        # 메인 타이틀
        title_surface = self.title_font.render(title_text, True, (200, 240, 255))
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 150))
        surface.blit(title_surface, title_rect)
        
        # 언더라인 효과
        line_width = title_rect.width + 40
        line_y = title_rect.bottom + 15
        line_x = SCREEN_WIDTH // 2 - line_width // 2
        
        # 그라디언트 라인
        for i in range(3):
            alpha = 255 - i * 60
            line_color = (*glow_color, alpha)
            line_surf = pygame.Surface((line_width, 3 - i), pygame.SRCALPHA)
            pygame.draw.rect(line_surf, line_color, line_surf.get_rect())
            surface.blit(line_surf, (line_x, line_y + i))
        
        # 서브타이틀
        subtitle_surface = self.subtitle_font.render(subtitle_text, True, (150, 200, 255))
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, 220))
        surface.blit(subtitle_surface, subtitle_rect)
    
    def _draw_decorations(self, surface):
        """장식 요소"""
        # 좌상단 코너 디테일
        self._draw_corner_detail(surface, 40, 40, 1)
        # 우상단 코너 디테일
        self._draw_corner_detail(surface, SCREEN_WIDTH - 40, 40, 2)
        # 좌하단 코너 디테일
        self._draw_corner_detail(surface, 40, SCREEN_HEIGHT - 40, 3)
        # 우하단 코너 디테일
        self._draw_corner_detail(surface, SCREEN_WIDTH - 40, SCREEN_HEIGHT - 40, 4)
    
    def _draw_corner_detail(self, surface, x, y, corner):
        """코너 장식"""
        size = 60
        color = (100, 150, 255, 100)
        
        # 펄스 효과
        pulse = math.sin(self.time * 3 + corner) * 0.2 + 0.8
        current_size = int(size * pulse)
        
        detail_surf = pygame.Surface((current_size, current_size), pygame.SRCALPHA)
        
        # 각 코너별 디자인
        if corner == 1:  # 좌상단
            pygame.draw.lines(detail_surf, color, False, [(0, current_size), (0, 0), (current_size, 0)], 3)
            pygame.draw.line(detail_surf, color, (10, 10), (current_size - 10, 10), 2)
            pygame.draw.line(detail_surf, color, (10, 10), (10, current_size - 10), 2)
        elif corner == 2:  # 우상단
            pygame.draw.lines(detail_surf, color, False, [(0, 0), (current_size, 0), (current_size, current_size)], 3)
            pygame.draw.line(detail_surf, color, (10, 10), (current_size - 10, 10), 2)
            pygame.draw.line(detail_surf, color, (current_size - 10, 10), (current_size - 10, current_size - 10), 2)
        elif corner == 3:  # 좌하단
            pygame.draw.lines(detail_surf, color, False, [(current_size, 0), (0, 0), (0, current_size)], 3)
            pygame.draw.line(detail_surf, color, (10, current_size - 10), (current_size - 10, current_size - 10), 2)
            pygame.draw.line(detail_surf, color, (10, 10), (10, current_size - 10), 2)
        else:  # 우하단
            pygame.draw.lines(detail_surf, color, False, [(0, current_size), (current_size, current_size), (current_size, 0)], 3)
            pygame.draw.line(detail_surf, color, (10, current_size - 10), (current_size - 10, current_size - 10), 2)
            pygame.draw.line(detail_surf, color, (current_size - 10, 10), (current_size - 10, current_size - 10), 2)
        
        # 센터링
        rect = detail_surf.get_rect(center=(x, y))
        surface.blit(detail_surf, rect)
    
    def _draw_footer(self, surface):
        """하단 정보"""
        # 컨트롤 힌트
        controls = "WASD: Move  |  Shift: Dash  |  E: Wall  |  Q: Noise  |  Space: Slow Motion"
        controls_surface = self.info_font.render(controls, True, (120, 150, 180))
        controls_rect = controls_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
        surface.blit(controls_surface, controls_rect)
        
        # 버전 정보
        version = "v1.0  |  Press ESC to Pause"
        version_surface = self.info_font.render(version, True, (100, 130, 160))
        version_rect = version_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        surface.blit(version_surface, version_rect)
    
    def handle_event(self, event, mouse_pos):
        """이벤트 처리"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button.is_clicked(mouse_pos, True):
                    return button.action
        return None


class HelpScreen:
    """도움말 화면"""
    
    def __init__(self):
        self.title_font = pygame.font.Font(None, 72)
        self.heading_font = pygame.font.Font(None, 48)
        self.text_font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 28)
        
        self.back_button = MenuButton("BACK", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80, 200, 60, "back")
        
        # 배경 효과
        self.particles = ParticleField(60)
        self.grid = GridBackground()
        self.time = 0
    
    def update(self, dt, mouse_pos):
        """업데이트"""
        self.time += dt
        self.particles.update(dt)
        self.grid.update(dt)
        self.back_button.update(dt, mouse_pos)
    
    def draw(self, surface):
        """그리기"""
        # 배경
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            color = (int(10 + 15 * ratio), int(15 + 25 * ratio), int(25 + 35 * ratio))
            pygame.draw.line(surface, color, (0, y), (SCREEN_WIDTH, y))
        
        self.grid.draw(surface)
        self.particles.draw(surface)
        
        # 타이틀
        title = self.title_font.render("HOW TO PLAY", True, (200, 240, 255))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
        surface.blit(title, title_rect)
        
        # 내용
        y_offset = 160
        
        sections = [
            ("OBJECTIVE", [
                "Collect 3 keys and reach the exit before time runs out!",
                "Avoid enemies powered by path-planning algorithms."
            ]),
            ("CONTROLS", [
                "WASD - Move your robot",
                "SHIFT - Dash (cooldown: 2.5s)",
                "E - Place temporary wall (cooldown: 6s, lasts 7s)",
                "Q - Noise bomb - confuses enemies (cooldown: 12s)",
                "SPACE - Slow motion (cooldown: 18s)",
                "ESC - Pause game"
            ]),
            ("TIPS", [
                "Use walls to block enemy paths and create safe zones",
                "Dash to escape tight situations",
                "Noise bombs make enemies lose track of you",
                "Plan your route carefully - time is limited!"
            ])
        ]
        
        for section_title, items in sections:
            # 섹션 타이틀
            heading = self.heading_font.render(section_title, True, (150, 200, 255))
            surface.blit(heading, (100, y_offset))
            y_offset += 50
            
            # 아이템
            for item in items:
                text = self.text_font.render(f"• {item}", True, (180, 210, 240))
                surface.blit(text, (120, y_offset))
                y_offset += 35
            
            y_offset += 15
        
        # 뒤로가기 버튼
        self.back_button.draw(surface, self.text_font)
    
    def handle_event(self, event, mouse_pos):
        """이벤트 처리"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.back_button.is_clicked(mouse_pos, True):
                return "back"
        return None
