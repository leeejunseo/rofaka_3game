import pygame as pg
from doc.conf import *
from objects.bullet import Bullet
import math

class Player:
    def __init__(self, game):
        self.size = 64
        self.image = pg.image.load("assets/player.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (self.size * 2, self.size * 2))
        self.game = game

        self.pos_x = self.game.main.screen.get_width() // 2
        self.pos_y = self.game.main.screen.get_height() // 2

        self.ang = 0
        self.ac_x = 0
        self.ac_y = 0
        self.ac_ang = 0
        self.bullets: list[Bullet] = list()
        self.ammo = 4
        self.reload_timer = 0  # 🔄 자동 리로드 타이머 (0이면 비활성)

    def update(self):
        keys = pg.key.get_pressed()

        # Vertical movement
        if keys[pg.K_w]:
            self.ac_y -= 0.05 if self.ac_y > -2 else 0
        elif keys[pg.K_s]:
            self.ac_y += 0.05 if self.ac_y < 2 else 0
        else:
            if abs(self.ac_y) < 0.2:
                self.ac_y = 0
            elif self.ac_y > 0:
                self.ac_y -= 0.05
            elif self.ac_y < 0:
                self.ac_y += 0.05

        # Horizontal movement
        if keys[pg.K_a]:
            self.ac_x -= 0.05 if self.ac_x > -2 else 0
        elif keys[pg.K_d]:
            self.ac_x += 0.05 if self.ac_x < 2 else 0
        else:
            if abs(self.ac_x) < 0.2:
                self.ac_x = 0
            elif self.ac_x > 0:
                self.ac_x -= 0.05
            elif self.ac_x < 0:
                self.ac_x += 0.05

        # Angular movement
        if keys[pg.K_RIGHT]:
            self.ac_ang -= 0.09 if self.ac_ang > -2 else 0
        elif keys[pg.K_LEFT]:
            self.ac_ang += 0.09 if self.ac_ang < 2 else 0
        else:
            if abs(self.ac_ang) < 0.2:
                self.ac_ang = 0
            elif self.ac_ang > 0:
                self.ac_ang -= 0.09
            elif self.ac_ang < 0:
                self.ac_ang += 0.09

        # 🔫 총 쏘기 (스페이스바 누르면 샷건처럼 4발 퍼지게 발사)
        if keys[pg.K_SPACE]:
            if self.ammo > 0:
                self.ammo -= 1
                spread_angles = [-10, -5, 5, 10]  # 샷건 퍼짐 각도 조절

                for offset in spread_angles:
                    angle = self.ang + offset
                    self.bullets.append(Bullet(
                        self.game,
                        self.pos_x + 40 * math.sin(math.radians(angle)),
                        self.pos_y + 40 * math.cos(math.radians(angle)),
                        angle
                    ))

                # 중심 각도 기준 반동 적용
                self.ac_x += 1 * -math.sin(math.radians(self.ang))
                self.ac_y += 1 * -math.cos(math.radians(self.ang))

                # 🔄 총알 다 떨어지면 타이머 시작
                if self.ammo == 0:
                    self.reload_timer = pg.time.get_ticks()



        # 🔁 자동 리로드 (1초 후)
        if self.ammo == 0 and self.reload_timer > 0:
            if pg.time.get_ticks() - self.reload_timer >= 1000:
                self.ammo = 4
                self.reload_timer = 0

        # 🔄 수동 리로드 (R 키)
        if keys[pg.K_r]:
            if self.ammo < 4:
                self.ammo = 4
                self.reload_timer = 0  # 수동 리로드 시 타이머 초기화

        # Updating position and angle
        self.pos_y += self.ac_y
        self.pos_x += self.ac_x
        self.ang += self.ac_ang

        # Correcting angle
        if self.ang > 359:
            self.ang -= 360
        elif self.ang < 0:
            self.ang += 360

        # Updating each bullet
        for bullet in self.bullets[:]:
            bullet.update()
            screen_w = self.game.main.screen.get_width()
            screen_h = self.game.main.screen.get_height()
            if (bullet.pos_x < -100 or bullet.pos_x > screen_w + 100 or
                bullet.pos_y < -100 or bullet.pos_y > screen_h + 100):
                self.bullets.remove(bullet)

        # 📌 화면 밖으로 나가지 못하게 제한
        screen_w = self.game.main.screen.get_width()
        screen_h = self.game.main.screen.get_height()
        self.pos_x = max(self.size, min(self.pos_x, screen_w - self.size))
        self.pos_y = max(self.size, min(self.pos_y, screen_h - self.size))

    def draw(self):
        # 🧍 플레이어 이미지
        self.game.main.screen.blit(self.image, (self.pos_x - self.size, self.pos_y - self.size))

        # ➖ 총구 방향선
        pg.draw.line(
            self.game.main.screen,
            WHITE,
            (self.pos_x, self.pos_y),
            (
                self.pos_x + 40 * math.sin(math.radians(self.ang)),
                self.pos_y + 40 * math.cos(math.radians(self.ang))
            ),
            5
        )

        # 🔫 총알 그리기
        for bullet in self.bullets:
            bullet.draw()

        # 🔢 탄약 수 표시
        if self.ammo == 0:
            ammo_text = "총알 장착중..."
        else:
            ammo_text = f"발사 가능 ({self.ammo})"
        ammo_left = self.game.main.font.render(ammo_text, True, WHITE)

        screen_width = self.game.main.screen.get_width()
        ammo_left_pos = ammo_left.get_rect(topright=(screen_width - 10, 10))
        self.game.main.screen.blit(ammo_left, ammo_left_pos)
