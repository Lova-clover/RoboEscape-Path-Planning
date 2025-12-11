"""
RoboEscape: Algorithm Hunters
메인 진입점
"""

import pygame
import sys
from game.engine import Game
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS


def main():
    """게임 메인 함수"""
    # Pygame 초기화
    pygame.init()
    pygame.mixer.init()
    
    # 화면 설정
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("RoboEscape: Algorithm Hunters")
    
    # FPS 제어
    clock = pygame.time.Clock()
    
    # 게임 인스턴스 생성
    game = Game(screen)
    
    # 메인 루프
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # 델타 타임 (초)
        
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game.handle_event(event)
        
        # 게임 업데이트
        game.update(dt)
        
        # 화면 그리기
        screen.fill((20, 20, 30))  # 어두운 배경
        game.draw()
        
        # 화면 업데이트
        pygame.display.flip()
    
    # 종료
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
