import pygame as pg
from doc.conf import *
from objects.player import Player
from objects.enemy import Enemy
from time import sleep

class Game:
    def __init__(self, main):
        self.game_cleared = False
        self.clear_time = None  # 클리어 시각 저장
        self.main = main
        self.player = Player(self)
        self.enemys = list()
        self.score = 0

        # ✅ 배경 이미지 불러오기
        self.bg_image = pg.image.load("assets/game_bg.png").convert()
        self.bg_image = pg.transform.scale(self.bg_image, (
            self.main.screen.get_width(),
            self.main.screen.get_height()
        ))

        # 이벤트 등록: 적 생성
        self.spawn_enemy = pg.USEREVENT + 1
        pg.time.set_timer(self.spawn_enemy, 1500)

    def delete(self):
        pg.time.set_timer(self.spawn_enemy, 0)  # 타이머 제거

    def event_handler(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.delete()
                self.main.layers.pop()
                return

        if event.type == self.spawn_enemy:
            if len(self.enemys) < 20:
                self.enemys.append(Enemy(self))

    def update(self):
        self.player.update()
        
        # 점수에 따라 게임 클리어
        if not self.game_cleared and self.score >= 20:
            self.game_cleared = True
            self.clear_time = pg.time.get_ticks()  # 현재 시각 저장
            self.delete()  # 적 생성 중지
            print("🎉 게임 클리어!")

        
        for enemy in self.enemys[:]:  # 리스트 수정 방지
            enemy.update()

            # 총알 충돌 판정
            for bullet in self.player.bullets[:]:
                distance = (enemy.pos_x - bullet.pos_x) ** 2 + (enemy.pos_y - bullet.pos_y) ** 2
                if distance < 2500:  # 충돌 판정 거리
                    self.enemys.remove(enemy)
                    self.player.bullets.remove(bullet)
                    self.score += 1
                    break

            # 플레이어 충돌 → 게임 종료
            distance_to_player = (enemy.pos_x - self.player.pos_x) ** 2 + (enemy.pos_y - self.player.pos_y) ** 2
            if distance_to_player < 2500:
                sleep(2)
                self.delete()
                self.main.layers.pop()

    def draw(self):
        # ✅ 배경 이미지로 화면 채우기
        self.main.screen.blit(self.bg_image, (0, 0))

        # 플레이어와 적 그리기
        self.player.draw()
        for enemy in self.enemys:
            enemy.draw()

        # ✅ 점수 출력 (항상 마지막에!)
        score = self.main.font.render(f"Score: {self.score}", True, WHITE)
        screen_width = self.main.screen.get_width()
        score_pos = score.get_rect(topright=(screen_width - 20, 50))
        self.main.screen.blit(score, score_pos)
        
        # ✅ 게임 클리어 메시지 출력
        if self.game_cleared:
            clear_text = self.main.font.render("🎉 CLEARED! 🎉", True, (255, 255, 0))
            clear_text = pg.transform.scale(clear_text, (700, 300))  # 크게 만들기
            clear_rect = clear_text.get_rect(center=(self.main.screen.get_width() // 2, self.main.screen.get_height() // 2))
            self.main.screen.blit(clear_text, clear_rect)
