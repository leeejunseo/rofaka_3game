import pygame as pg
import subprocess
import sys
import os

def launch_game(script_path):
    folder = os.path.dirname(script_path)
    # 음악 정지 후 게임 실행
    pg.mixer.music.stop()
    subprocess.run([sys.executable, "main.py"], cwd=folder)
    # 음악 다시 재생 (게임 끝나고 돌아왔을 때)
    pg.mixer.music.play(-1)


def draw_text_boxed_shadow(surface, text, font, center_x, y, padding=10):
    text_surface = font.render(text, True, (255, 255, 255))
    text_width, text_height = text_surface.get_size()
    box_surface = pg.Surface((text_width + padding * 2, text_height + padding * 2), pg.SRCALPHA)
    box_surface.fill((0, 0, 0, 160))
    shadow = font.render(text, True, (0, 0, 0))

    x = center_x - text_width // 2
    box_x = center_x - (text_width + padding * 2) // 2

    surface.blit(box_surface, (box_x, y - padding))
    surface.blit(shadow, (x + 2, y + 2))
    surface.blit(text_surface, (x, y))

def main_menu():
    pg.init()
    pg.mixer.init()

    info = pg.display.Info()
    screen_width, screen_height = info.current_w, info.current_h
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    pg.display.set_caption("🎮 게임 선택 메뉴")
    pg.mouse.set_visible(False)

    font = pg.font.Font("TmonMonsori.ttf.ttf", 60)
    clock = pg.time.Clock()

    # 배경 이미지 로드
    bg_image = pg.image.load("menu_bg.png").convert()
    bg_image = pg.transform.scale(bg_image, (screen_width, screen_height))

    # 🎵 배경음악 설정
    music_path = os.path.join(os.path.dirname(__file__), "헌시.mp3")
    if os.path.exists(music_path):
        try:
            pg.mixer.music.load(music_path)
            pg.mixer.music.set_volume(0.6)
            pg.mixer.music.play(-1)  # 무한 반복
        except Exception as e:
            print("배경음악 로딩 실패:", e)
    else:
        print("배경음악 파일을 찾을 수 없습니다.")

    while True:
        screen.blit(bg_image, (0, 0))

        draw_text_boxed_shadow(screen, "게임 선택하기", font, screen_width // 2, screen_height // 6)
        draw_text_boxed_shadow(screen, "1. 저학년으로 플레이하기", font, screen_width // 2, screen_height // 3)
        draw_text_boxed_shadow(screen, "2. 고학년으로 플레이하기", font, screen_width // 2, screen_height // 3 + 70)
        draw_text_boxed_shadow(screen, "3. 조종사로 플레이하기", font, screen_width // 2, screen_height // 3 + 140)
        draw_text_boxed_shadow(screen, "ESC. 종료하기", font, screen_width // 2, screen_height - 100)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    launch_game("탕탕_생도대/main.py")
                elif event.key == pg.K_2:
                    launch_game("공사타워디펜스/main.py")
                elif event.key == pg.K_3:
                    launch_game("War-Plane/main.py")
                elif event.key == pg.K_ESCAPE:
                    pg.mixer.music.stop()
                    pg.quit()
                    sys.exit()

        pg.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main_menu()
