# 외부 모듈 및 다른 파일에서 정의한 함수와 클래스들을 가져옴
from Lib import *                # 게임 설정값 및 유틸리티 함수들 포함
from Effects import *           # 발사 이펙트 등 그래픽 효과 관련 클래스
import pygame                   # 파이게임 기본 모듈
from Lib import (               # 필요한 상수 및 함수만 선택적으로 import
    getDistance,                # 두 점 사이 거리 계산 함수
    GRID_SIZE,                  # 격자 한 칸의 크기 (타워 사거리 계산 등)
    ENEMY_KILLED                # 적 사망 이벤트 정의
)

# 타워를 생성하는 함수: 사용자가 클릭한 위치에 타워를 배치할 수 있는지 확인 후 생성
def createTower(pos, tower_choice, tower_models, path, towers):
    # 만약 클릭한 위치가 경로가 아니라면 (즉, 설치 가능 지역이라면)
    if not path.contains(pos):
        # 이미 다른 타워가 설치된 위치인지 확인
        for tower in towers.sprites():
            if tower.rect.collidepoint(pos):
                return None  # 이미 설치된 타워가 있다면 아무것도 반환하지 않음

        # 선택한 타워 모델 정보를 불러옴
        model = tower_models[tower_choice]
        # 해당 모델이 FireTower라면
        if model.name == "Fire Tower":
            return FireTower(pos, model)
        # IceTower라면
        elif model.name == "Ice Tower":
            return IceTower(pos, model)
        # 그 외 일반 타워 생성
        else:
            return Tower(pos, model)
    # 경로 위라면 설치 불가
    return None


# 타워 모델 클래스: 타워의 특성(스탯)을 정의하는 설계도
class TowerModel:
    def __init__(self, name, damage, fire_rate, range, value, fire_colour, sprite_location, description):
        self.name = name                      # 타워 이름
        self.damage = damage                  # 공격력
        self.fire_rate = fire_rate            # 공격 주기 (낮을수록 자주 공격함)
        self.range = range                    # 사거리 (격자 수)
        self.value = value                    # 비용
        self.fire_colour = fire_colour        # 공격 이펙트 색상
        self.sprite_location = sprite_location  # 이미지 경로
        self.description = description        # 설명


# 기본 타워 클래스: 게임 화면에 배치되는 개별 타워 객체
class Tower(pygame.sprite.Sprite):
    def __init__(self, pos, model):
        pygame.sprite.Sprite.__init__(self)       # 파이게임 스프라이트 초기화
        self.model = model                        # 타워 설계도 정보를 저장
        self.image = pygame.image.load(model.sprite_location)  # 이미지 불러오기
        self.rect = self.image.get_rect()         # 이미지 사각형(위치 정보)
        self.rect.center = pos                    # 중심 좌표를 타워 위치로 설정
        self.last_fired = 0                       # 마지막 공격 이후 경과 시간

    # 매 프레임마다 호출되는 업데이트 함수
    def update(self, enemies, effects, screen):
        # 아직 공격 쿨다운 중이면 시간만 증가시킴
        if self.last_fired <= self.model.fire_rate:
            self.last_fired += 1
        else:
            target = None  # 공격할 목표 적
            for sprite in enemies.sprites():
                if not sprite.is_dead:
                    distance = getDistance(self.rect.center, sprite.rect.center)
                    # 적이 사거리 내에 있다면
                    if distance <= self.model.range * GRID_SIZE + 1:
                        # 이동 거리가 가장 긴 적을 우선 공격함
                        if target is None or sprite.distance_travelled > target.distance_travelled:
                            target = sprite
            # 목표가 정해졌다면 공격 실행
            if target is not None:
                target.health -= self.model.damage  # 적 체력 감소
                # 발사 이펙트를 추가 (적 위치 → 타워 위치 방향)
                effects.add(ShootEffect(self.model.fire_colour, target.rect.center, self.rect.center, 2, screen.get_size()))
                if target.health <= 0:
                    target.is_dead = True  # 적을 제거
                    pygame.event.post(pygame.event.Event(ENEMY_KILLED, enemy=target))  # 적 사망 이벤트 발생
                self.last_fired = 0  # 다시 쿨다운 시작


# 범위 피해를 주는 FireTower (화염 타워): 주변 적까지 함께 피해를 줌
class FireTower(Tower):
    def __init__(self, pos, model):
        super().__init__(pos, model)  # 부모 클래스 초기화

    def update(self, enemies, effects, screen):
        if self.last_fired <= self.model.fire_rate:
            self.last_fired += 1
        else:
            target = None
            for sprite in enemies.sprites():
                if not sprite.is_dead:
                    distance = getDistance(self.rect.center, sprite.rect.center)
                    if distance <= self.model.range * GRID_SIZE + 1:
                        target = sprite  # 첫 번째 적 발견 시 바로 공격
                        break

            # 메인 타겟을 기준으로 주변 적에게도 피해를 줌 (스플래시)
            if target:
                splash_radius = 50  # 범위 공격 반경 (픽셀 기준)
                for other in enemies:
                    if not other.is_dead:
                        d = getDistance(target.rect.center, other.rect.center)
                        if d <= splash_radius:
                            other.health -= self.model.damage
                            # 발사 이펙트 생성
                            effects.add(ShootEffect(self.model.fire_colour, other.rect.center, self.rect.center, 2, screen.get_size()))
                            if other.health <= 0:
                                other.is_dead = True
                                pygame.event.post(pygame.event.Event(ENEMY_KILLED, enemy=other))
                self.last_fired = 0


# 적에게 슬로우 효과를 주는 IceTower (빙결 타워)
class IceTower(Tower):
    def __init__(self, pos, model):
        super().__init__(pos, model)

    def update(self, enemies, effects, screen):
        if self.last_fired <= self.model.fire_rate:
            self.last_fired += 1
        else:
            for sprite in enemies.sprites():
                if not sprite.is_dead:
                    distance = getDistance(self.rect.center, sprite.rect.center)
                    if distance <= self.model.range * GRID_SIZE + 1:
                        # 적에게 피해와 슬로우 효과를 동시에 줌
                        sprite.health -= self.model.damage
                        sprite.apply_slow(3, 0.5)  # 3초간 이동 속도 50% 감소
                        effects.add(ShootEffect(self.model.fire_colour, sprite.rect.center, self.rect.center, 2, screen.get_size()))
                        if sprite.health <= 0:
                            sprite.is_dead = True
                            pygame.event.post(pygame.event.Event(ENEMY_KILLED, enemy=sprite))
                        self.last_fired = 0
                        break  # 한 명만 공격하고 종료


# 중복 정의되어 있던 createTower 함수를 정리하여 하나만 남김 (중복 제거 완료)
