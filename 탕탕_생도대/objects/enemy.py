import pygame as pg
import random

# 기본 색 정의 (필요시 외부에서 import 해도 됨)
RED = (255, 0, 0)

class Enemy:
    def __init__(self, game):
        self.game = game
        self.speed = 1

        # 이미지 로딩 및 크기 조절
        self.image = pg.image.load("assets/enemy.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (100, 100))

        # 화면 크기 얻기
        screen_w = self.game.main.screen.get_width()
        screen_h = self.game.main.screen.get_height()

        # 화면 밖에서 생성 (왼쪽/오른쪽/위/아래 랜덤)
        side = random.choice(['left', 'right', 'top', 'bottom'])

        if side == 'left':
            self.pos_x = -100
            self.pos_y = random.randint(0, screen_h)
        elif side == 'right':
            self.pos_x = screen_w + 100
            self.pos_y = random.randint(0, screen_h)
        elif side == 'top':
            self.pos_x = random.randint(0, screen_w)
            self.pos_y = -100
        elif side == 'bottom':
            self.pos_x = random.randint(0, screen_w)
            self.pos_y = screen_h + 100

    def update(self):
        # 플레이어 방향으로 이동
        if self.pos_x > self.game.player.pos_x:
            self.pos_x -= self.speed
        elif self.pos_x < self.game.player.pos_x:
            self.pos_x += self.speed
        if self.pos_y > self.game.player.pos_y:
            self.pos_y -= self.speed
        elif self.pos_y < self.game.player.pos_y:
            self.pos_y += self.speed

    def draw(self):
        # 중심 정렬해서 이미지 출력
        self.game.main.screen.blit(self.image, (self.pos_x - 50, self.pos_y - 50))
