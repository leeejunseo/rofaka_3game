import pygame
from Lib import (
    UP, DOWN, LEFT, RIGHT,
    gridCoordToPos, posToGridCoords, getDirection,
    ENEMY_REACHED_END
)

# 적 유닛 객체를 생성하는 함수
def createEnemy(pos):
    return Enemy(pos, 2, 3)  # 위치, 속도 2, 체력 3으로 적 생성

# 적 유닛 클래스 정의
class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, speed, health, current_waypoint=1):
        super().__init__()  # 부모 클래스 초기화 (Sprite)

        # 방향에 따라 적 이미지 설정 (50x50 크기로 조정)
        self.images = {
            UP: pygame.transform.scale(pygame.image.load('assets/enemy_back.png').convert_alpha(), (50, 50)),
            DOWN: pygame.transform.scale(pygame.image.load('assets/enemy_front.png').convert_alpha(), (50, 50)),
            LEFT: pygame.transform.scale(pygame.image.load('assets/enemy_left.png').convert_alpha(), (50, 50)),
            RIGHT: pygame.transform.scale(pygame.image.load('assets/enemy_right.png').convert_alpha(), (50, 50)),
        }

        self.direction = DOWN  # 초기 방향은 아래로
        self.image = self.images[self.direction]  # 현재 방향의 이미지로 설정
        self.rect = self.image.get_rect()  # 이미지에서 사각형 영역 얻기
        self.rect.center = pos  # 적의 중심 위치 지정

        self.speed = speed  # 현재 속도
        self.original_speed = speed  # 원래 속도 (슬로우 복원용)
        self.health = health  # 체력
        self.current_waypoint = current_waypoint  # 현재 목표 웨이포인트 인덱스
        self.value = 5  # 적 처치 시 획득 점수 또는 자원
        self.distance_travelled = 0  # 이동 거리 누적
        self.is_dead = False  # 죽었는지 여부
        self.slow_timer = 0  # 슬로우 효과 지속 시간 (프레임 단위)

    # 적에게 슬로우 효과 적용
    def apply_slow(self, duration, factor):
        self.speed = self.original_speed * factor  # 속도 감소
        self.slow_timer = duration * 60  # 초 단위를 프레임 단위로 변환 (예: 2초 → 120프레임)

    # 매 프레임마다 적 상태 업데이트
    def update(self, waypoints, grid_size):
        if self.slow_timer > 0:
            self.slow_timer -= 1  # 슬로우 타이머 감소
        else:
            self.speed = self.original_speed  # 복원

        waypoint = waypoints[self.current_waypoint]  # 현재 목표 웨이포인트

        # 방향 변경 조건 확인 및 이미지 변경
        if self.direction is None or self.rect.collidepoint(gridCoordToPos(waypoint, grid_size)):
            if self.rect.collidepoint(gridCoordToPos(waypoint, grid_size)):
                if self.current_waypoint < len(waypoints) - 1:
                    self.current_waypoint += 1  # 다음 웨이포인트로 이동
                else:
                    # 마지막 도착지에 도달한 경우 이벤트 발생
                    pygame.event.post(pygame.event.Event(ENEMY_REACHED_END, enemy=self))

            waypoint = waypoints[self.current_waypoint]  # 다음 웨이포인트
            current_grid = posToGridCoords(self.rect.center, grid_size)  # 현재 위치의 격자 좌표
            self.direction = getDirection(current_grid, waypoint)  # 다음 방향 계산

            if self.direction in self.images:
                self.image = self.images[self.direction]  # 방향에 맞는 이미지로 변경

        # 방향에 따라 적 이동
        self.distance_travelled += self.speed  # 누적 거리 증가
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
