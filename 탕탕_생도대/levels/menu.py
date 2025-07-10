import os
import pygame as pg
from time import time
from doc import conf  # 여기서 WIDTH, HEIGHT, 색상 상수 불러옴
from levels.game import Game

# ✅ 폰트 경로 설정
FONT_PATH = os.path.join(os.path.dirname(__file__), "TmonMonsori.ttf.ttf")

class Menu:
    def __init__(self, main):
        self.main = main

        width = conf.WIDTH
        height = conf.HEIGHT

        # ✅ TmonMonsori.ttf 폰트 로드 및 크기 설정 (비율 기반)
        self.font = pg.font.Font(FONT_PATH, int(height * 0.03))   # 작은 글씨
        self.font2 = pg.font.Font(FONT_PATH, int(height * 0.12))  # 제목
        self.font3 = pg.font.Font(FONT_PATH, int(height * 0.06))  # 중간 안내문

        # ✅ 텍스트 렌더링
        self.title_text = self.font2.render("탕탕 생도대", True, conf.RED)
        self.play_text = self.font3.render("Enter 누르면 시작", True, conf.GREEN)
        self.controls_text = self.font.render(
            "WASD 로 움직이기, SPACE 발사, 자동 재장전(1초), ESC 나가기", True, conf.WHITE)

        # ✅ 텍스트 위치 계산
        self.title_rect = self.title_text.get_rect(center=(width // 2, int(height * 0.25)))
        self.play_rect = self.play_text.get_rect(center=(width // 2, int(height * 0.8)))
        self.controls_rect = self.controls_text.get_rect(bottomleft=(int(width * 0.02), height - 20))

        self.time = time()
        self.toggle = True  # 깜빡임 토글

    def delete(self):
        pass

    def event_handler(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.main.layers.append(Game(self.main))
            elif event.key == pg.K_ESCAPE:
                self.main.game_over()

    def update(self):
        # 마우스가 플레이 버튼 위에 있을 때 커서 변경 + 클릭 처리
        if self.play_rect.collidepoint(pg.mouse.get_pos()):
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
            if pg.mouse.get_pressed()[0]:
                self.main.layers.append(Game(self.main))
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
        else:
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

        # 텍스트 깜빡임 시간 조절
        if time() - self.time > 0.5:
            self.toggle = not self.toggle
            self.time = time()

    def draw(self):
        self.main.screen.blit(self.title_text, self.title_rect)
        if self.toggle:
            self.main.screen.blit(self.play_text, self.play_rect)
        self.main.screen.blit(self.controls_text, self.controls_rect)
