import pygame as pg
import subprocess
import sys
import os

def launch_game(script_path):
    folder = os.path.dirname(script_path)
    subprocess.run([sys.executable, "main.py"], cwd=folder)

# ✅ 텍스트를 그림자와 반투명 박스로 함께 출력하는 함수
def draw_text_boxed_shadow(surface, text, font, center_x, y, padding=10):
    # 텍스트 렌더링
    text_surface = font.render(text, True, (255, 255, 255))
    text_width, text_height = text_surface.get_size()

    # 반투명 박스 만들기
    box_surface = pg.Surface((text_width + padding * 2, text_height + padding * 2), pg.SRCALPHA)
    box_surface.fill((0, 0, 0, 160))  # 반투명 검정

    # 그림자 만들기 (조금 아래/오른쪽)
    shadow = font.render(text, True, (0, 0, 0))

    # 위치 계산
    x = center_x - text_width // 2
    box_x = center_x - (text_width + padding * 2) // 2

    # 출력
    surface.blit(box_surface, (box_x, y - padding))
    surface.blit(shadow, (x + 2, y + 2))
    surface.blit(text_surface, (x, y))

def main_menu():
    pg.init()
    info = pg.display.Info()
    screen_width, screen_height = info.current_w, info.current_h

    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    pg.display.set_caption("🎮 게임 선택 메뉴")
    pg.mouse.set_visible(False)

    font = pg.font.Font("NanumGothic.ttf", 60)
    clock = pg.time.Clock()

    bg_image = pg.image.load("menu_bg.png").convert()
    bg_image = pg.transform.scale(bg_image, (screen_width, screen_height))

    while True:
        screen.blit(bg_image, (0, 0))

        # 텍스트 출력
        draw_text_boxed_shadow(screen, "게임 선택하기", font, screen_width // 2, screen_height // 6)
        draw_text_boxed_shadow(screen, "1. 고학년으로 플레이하기", font, screen_width // 2, screen_height // 3)
        draw_text_boxed_shadow(screen, "2. 저학년으로 플레이하기", font, screen_width // 2, screen_height // 3 + 70)
        draw_text_boxed_shadow(screen, "3. 조종사로 플레이하기", font, screen_width // 2, screen_height // 3 + 140)
        draw_text_boxed_shadow(screen, "ESC. 종료하기", font, screen_width // 2, screen_height - 100)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    launch_game("공사타워디펜스/main.py")
                elif event.key == pg.K_2:
                    launch_game("the-fps/main.py")
                elif event.key == pg.K_3:
                    launch_game("War-Plane/main.py")
                elif event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

        pg.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main_menu()
