# pygame 모듈을 가져와서 스프라이트 처리, 이미지 렌더링 등 기능 사용
import pygame

# Lib.py에서 방향 상수, 좌표 변환 함수, 적 도달 이벤트를 가져옴
from Lib import (
    UP, DOWN, LEFT, RIGHT,                    # 방향 상수 (상, 하, 좌, 우)
    gridCoordToPos, posToGridCoords,          # 격자 좌표 <-> 픽셀 좌표 변환 함수
    getDirection,                             # 현재 위치에서 다음 웨이포인트까지의 방향 계산 함수
    ENEMY_REACHED_END                         # 적이 맵의 끝에 도달했을 때 발생시키는 사용자 정의 이벤트
)

# 적 유닛을 생성하는 팩토리 함수 정의
def createEnemy(pos):
    return Enemy(pos, 2, 3)  # Enemy 클래스 객체 생성: 위치 pos, 속도 2, 체력 3

# 적 유닛 클래스 정의 (Pygame의 Sprite를 상속받아 그룹에 포함 가능)
class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, speed, health, current_waypoint=1):
        super().__init__()  # 부모 클래스(Sprite)의 초기화 호출

        # 각 방향별로 사용할 이미지 불러오기 및 크기 50x50으로 조정
        self.images = {
            UP: pygame.transform.scale(pygame.image.load('assets/enemy_back.png').convert_alpha(), (50, 50)),
            DOWN: pygame.transform.scale(pygame.image.load('assets/enemy_front.png').convert_alpha(), (50, 50)),
            LEFT: pygame.transform.scale(pygame.image.load('assets/enemy_left.png').convert_alpha(), (50, 50)),
            RIGHT: pygame.transform.scale(pygame.image.load('assets/enemy_right.png').convert_alpha(), (50, 50)),
        }

        self.direction = DOWN  # 초기 방향을 아래(DOWN)로 설정
        self.image = self.images[self.direction]  # 현재 방향에 해당하는 이미지 설정
        self.rect = self.image.get_rect()         # 이미지로부터 위치 및 크기 정보를 가진 rect 객체 생성
        self.rect.center = pos                    # 초기 위치 설정 (중심 좌표를 pos로 지정)

        self.speed = speed                        # 적의 이동 속도 설정
        self.original_speed = speed               # 원래 속도 보존 (슬로우 적용 후 복원용)
        self.health = health                      # 체력 설정
        self.current_waypoint = current_waypoint  # 현재 목표 웨이포인트 인덱스 (기본값: 1번 지점부터 시작)
        self.value = 5                            # 적이 죽었을 때 플레이어가 얻는 보상값 (돈 또는 점수)
        self.distance_travelled = 0               # 적이 이동한 거리 누적값 (추적용)
        self.is_dead = False                      # 적이 죽었는지 여부를 표시 (게임 오브젝트 제거 여부)
        self.slow_timer = 0                       # 슬로우 효과 남은 시간 (프레임 단위)

    # 적에게 슬로우 효과를 적용하는 함수
    def apply_slow(self, duration, factor):
        self.speed = self.original_speed * factor  # 현재 속도를 원래 속도의 factor배로 감소
        self.slow_timer = duration * 60            # 초 단위를 프레임 수로 환산하여 타이머 설정 (1초=60프레임 기준)

    # 매 프레임마다 호출되는 업데이트 함수 (위치 이동, 슬로우 관리, 웨이포인트 이동 등 포함)
    def update(self, waypoints, grid_size):
        if self.slow_timer > 0:
            self.slow_timer -= 1             # 슬로우 효과 지속 시간 감소
        else:
            self.speed = self.original_speed # 슬로우 끝나면 원래 속도로 복원

        waypoint = waypoints[self.current_waypoint]  # 현재 목표 웨이포인트 좌표 가져오기

        # 방향 전환 지점에 도달했는지 확인하고 방향 및 이미지 갱신
        if self.direction is None or self.rect.collidepoint(gridCoordToPos(waypoint, grid_size)):
            if self.rect.collidepoint(gridCoordToPos(waypoint, grid_size)):
                # 다음 웨이포인트로 이동할 수 있는 경우
                if self.current_waypoint < len(waypoints) - 1:
                    self.current_waypoint += 1  # 다음 웨이포인트 인덱스로 이동
                else:
                    # 마지막 웨이포인트에 도달한 경우 → 적이 맵 끝에 도달
                    pygame.event.post(pygame.event.Event(ENEMY_REACHED_END, enemy=self))  # 적 도달 이벤트 전송

            # (도달 후) 다음 웨이포인트를 새 목표로 설정
            waypoint = waypoints[self.current_waypoint]
            current_grid = posToGridCoords(self.rect.center, grid_size)  # 현재 위치를 격자 좌표로 변환
            self.direction = getDirection(current_grid, waypoint)        # 현재 위치에서 다음 웨이포인트까지의 방향 계산

            if self.direction in self.images:
                self.image = self.images[self.direction]  # 방향에 맞는 이미지로 전환

        # 방향에 따라 적의 위치를 이동시킴
        self.distance_travelled += self.speed  # 누적 이동 거리 증가

        if self.direction == UP:
            self.rect.y -= self.speed  # 위로 이동
            self.rect.centerx = waypoint[0] * grid_size + grid_size // 2  # 중심 x좌표 정렬 (격자 중앙)
        elif self.direction == DOWN:
            self.rect.y += self.speed  # 아래로 이동
            self.rect.centerx = waypoint[0] * grid_size + grid_size // 2  # 중심 x좌표 정렬
        elif self.direction == LEFT:
            self.rect.x -= self.speed  # 왼쪽으로 이동
            self.rect.centery = waypoint[1] * grid_size + grid_size // 2  # 중심 y좌표 정렬
        elif self.direction == RIGHT:
            self.rect.x += self.speed  # 오른쪽으로 이동
            self.rect.centery = waypoint[1] * grid_size + grid_size // 2  # 중심 y좌표 정렬
