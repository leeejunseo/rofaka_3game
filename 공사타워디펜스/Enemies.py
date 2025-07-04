import pygame
from Lib import *

def createEnemy(pos):
    return Enemy(pos, 2, 3)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, speed, health, current_waypoint=1):
        super().__init__()

        # 방향별 이미지 불러오기 (50x50 크기 조절)
        self.images = {
            UP: pygame.transform.scale(pygame.image.load('assets/enemy_back.png').convert_alpha(), (50, 50)),
            DOWN: pygame.transform.scale(pygame.image.load('assets/enemy_front.png').convert_alpha(), (50, 50)),
            LEFT: pygame.transform.scale(pygame.image.load('assets/enemy_left.png').convert_alpha(), (50, 50)),
            RIGHT: pygame.transform.scale(pygame.image.load('assets/enemy_right.png').convert_alpha(), (50, 50)),
        }

        self.direction = DOWN  # 초기 방향
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.speed = speed
        self.original_speed = speed
        self.health = health
        self.current_waypoint = current_waypoint
        self.value = 5
        self.distance_travelled = 0
        self.is_dead = False
        self.slow_timer = 0

    def apply_slow(self, duration, factor):
        self.speed = self.original_speed * factor
        self.slow_timer = duration * 60  # 60프레임 기준

    def update(self, waypoints, grid_size):
        if self.slow_timer > 0:
            self.slow_timer -= 1
        else:
            self.speed = self.original_speed

        waypoint = waypoints[self.current_waypoint]

        # 방향 계산 및 이미지 갱신
        if self.direction is None or self.rect.collidepoint(gridCoordToPos(waypoint, grid_size)):
            if self.rect.collidepoint(gridCoordToPos(waypoint, grid_size)):
                if self.current_waypoint < len(waypoints) - 1:
                    self.current_waypoint += 1
                else:
                    pygame.event.post(pygame.event.Event(ENEMY_REACHED_END, enemy=self))

            waypoint = waypoints[self.current_waypoint]
            current_grid = posToGridCoords(self.rect.center, grid_size)
            self.direction = getDirection(current_grid, waypoint)

            if self.direction in self.images:
                self.image = self.images[self.direction]

        # 이동 처리
        self.distance_travelled += self.speed
        if self.direction == UP:
            self.rect.y -= self.speed
            self.rect.centerx = waypoint[0] * grid_size + grid_size // 2
        elif self.direction == DOWN:
            self.rect.y += self.speed
            self.rect.centerx = waypoint[0] * grid_size + grid_size // 2
        elif self.direction == LEFT:
            self.rect.x -= self.speed
            self.rect.centery = waypoint[1] * grid_size + grid_size // 2
        elif self.direction == RIGHT:
            self.rect.x += self.speed
            self.rect.centery = waypoint[1] * grid_size + grid_size // 2
