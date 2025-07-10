import pygame as pg
import sys
from doc import conf  # doc.conf에서 WIDTH, HEIGHT, RES 설정
from levels.menu import Menu
import os

class Main:
    def __init__(self):
        pg.init()

        # ✅ 전체화면 해상도 얻기
        info = pg.display.Info()
        RES = (info.current_w, info.current_h)

        # ✅ 전체화면으로 창 생성
        self.screen = pg.display.set_mode(RES, pg.FULLSCREEN)
        pg.display.set_caption("Game")
        pg.mouse.set_visible(False)

        self.clock = pg.time.Clock()
        self.show_fps = True
        self.pipe = False

        # ✅ 폰트 설정
        self.font = pg.font.Font("assets/TmonMonsori.ttf.ttf", 18)
        self.font2 = pg.font.Font(pg.font.get_default_font(), 136)
        self.font3 = pg.font.Font(pg.font.get_default_font(), 32)

        # ✅ 전역 변수 동기화
        conf.WIDTH = RES[0]
        conf.HEIGHT = RES[1]
        conf.RES = RES

        self.bg_image = pg.image.load("assets/background.png").convert()
        self.bg_image = pg.transform.scale(self.bg_image, (conf.WIDTH, conf.HEIGHT))

        # ✅ 효과음/배경음 초기화 및 재생
        sound_path = os.path.join("assets", "AK47.mp3")
        try:
            pg.mixer.init()
            pg.mixer.music.load(sound_path)
            pg.mixer.music.set_volume(0.3)  # 볼륨 조절 (0.0 ~ 1.0)
            pg.mixer.music.play(-1)  # -1이면 무한 반복, 0이면 한 번만 재생
        except Exception as e:
            print("사운드 로딩 실패:", e)

        # ✅ 이벤트 설정
        self.spawn_enemy = pg.USEREVENT + 1
        pg.time.set_timer(self.spawn_enemy, 1500)

        # ✅ 메뉴 레이어 추가
        self.layers = list()
        self.layers.append(Menu(self))

    def event_handler(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game_over()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_INSERT:
                    self.show_fps = not self.show_fps
                if event.key == pg.K_p:
                    self.pipe = not self.pipe

            # 현재 레이어에 이벤트 전달
            self.layers[-1].event_handler(event)

    def update(self):
        self.clock.tick(120)
        self.layers[-1].update()

    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))
        self.layers[-1].draw()

        if self.show_fps:
            fps = self.font.render(f"{self.clock.get_fps():.0f}", True, conf.WHITE)
            self.screen.blit(fps, (10, 10))

    def run(self):
        while True:
            self.event_handler()
            self.update()
            self.draw()
            pg.display.update()

    def game_over(self):
        pg.quit()
        sys.exit(0)

if __name__ == '__main__':
    game = Main()
    game.run()
