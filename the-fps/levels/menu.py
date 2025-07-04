import pygame as pg
from time import time
from doc import conf  # 여기서 WIDTH, HEIGHT, 색상 상수 불러옴
from levels.game import Game

class Menu:
    def __init__(self, main):
        self.main = main

        # ✅ conf에서 해상도 동기화된 값을 직접 사용
        width = conf.WIDTH
        height = conf.HEIGHT

        # ✅ 폰트가 너무 작다면 여기서도 비율로 만들어볼 수 있음
        # self.font = pg.font.Font(None, int(height * 0.03))
        # self.font2 = pg.font.Font(None, int(height * 0.12))
        # self.font3 = pg.font.Font(None, int(height * 0.06))

        # 텍스트 생성
        self.title_text = self.main.font2.render("THE FPS", True, conf.RED)
        self.play_text = self.main.font3.render("Press ENTER to Play", True, conf.GREEN)
        self.controls_text = self.main.font.render(
            "WASD to Move, SPACE to shoot, R to reload, ESC to exit, Good Luck!", True, conf.WHITE)

        # ✅ 화면 비율 기반 위치 조정
        self.title_rect = self.title_text.get_rect(center=(width // 2, int(height * 0.25)))
        self.play_rect = self.play_text.get_rect(center=(width // 2, int(height * 0.8)))
        self.controls_rect = self.controls_text.get_rect(bottomleft=(int(width * 0.02), height - 20))

        self.time = time()
        self.toggle = True

    def delete(self):
        pass

    def event_handler(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.main.layers.append(Game(self.main))
            elif event.key == pg.K_ESCAPE:
                self.main.game_over()

    def update(self):
        # 마우스 hover 시 핸드 커서
        if self.play_rect.collidepoint(pg.mouse.get_pos()):
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
            if pg.mouse.get_pressed()[0]:
                self.main.layers.append(Game(self.main))
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
        else:
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

        # 깜빡이는 텍스트 처리
        if time() - self.time > 0.5:
            self.toggle = not self.toggle
            self.time = time()

    def draw(self):
        self.main.screen.blit(self.title_text, self.title_rect)
        if self.toggle:
            self.main.screen.blit(self.play_text, self.play_rect)
        self.main.screen.blit(self.controls_text, self.controls_rect)
