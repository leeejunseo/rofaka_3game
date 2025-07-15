# Lib.py의 모든 변수 및 상수(GRID_SIZE 등)를 불러옴
#타워 공격/폭발 이펙트 시각화 전용 클래스 정의 파일
from Lib import *

# 총알 발사 이펙트를 구현하는 클래스 정의
class ShootEffect(pygame.sprite.Sprite):  # Pygame의 Sprite 클래스를 상속받아 사용
    def __init__(self, colour, startpos, endpos, timeout, screen_size):
        pygame.sprite.Sprite.__init__(self)  # 부모 클래스(Sprite)의 초기화 함수 호출
        self.colour = colour                 # 발사 이펙트의 색상 (예: 빨간색, 노란색 등)
        self.startpos = startpos             # 선의 시작 위치 (x, y 좌표)
        self.endpos = endpos                 # 선의 끝 위치 (x, y 좌표)
        self.timeout = timeout               # 이펙트가 유지되는 시간 (프레임 단위)
        self.image = pygame.Surface(screen_size, pygame.SRCALPHA)  # 투명 배경을 가진 전체 화면 크기의 Surface 생성
        pygame.draw.line(self.image, self.colour, self.startpos, self.endpos, 5)  # 시작~끝 좌표까지 굵기 5의 선을 그림
        self.rect = self.image.get_rect()    # 이미지에서 사용될 rect(위치/크기) 정보 생성
        self.time_alive = 0                  # 화면에 존재한 시간(프레임 수)을 추적하는 변수

    def update(self):                        # 매 프레임마다 호출되는 메서드
        self.time_alive += 1                 # 화면에 존재한 시간을 1 증가시킴
        if self.time_alive > self.timeout:   # 설정된 시간을 초과하면
            self.kill()                      # 이펙트를 화면에서 제거함 (Sprite 그룹에서도 제거됨)

# 폭발 애니메이션 등을 위한 스프라이트 시트 애니메이션 클래스 정의
class SpriteSheet(pygame.sprite.Sprite):  # 역시 Pygame의 Sprite를 상속
    def __init__(self, pos, sprite_location):
        pygame.sprite.Sprite.__init__(self)     # 부모 Sprite 초기화
        self.pos = pos                          # 애니메이션이 출력될 중심 위치 (x, y 좌표)
        self.spritesheet = pygame.image.load(sprite_location)  # 지정된 경로의 스프라이트 이미지 파일 로드
        self.time_alive = self.current_image = (0, 0)  # 현재 프레임 좌표 (x, y)와 생존 시간 초기화
        self.image = None                        # 화면에 실제로 표시될 이미지 (초기에는 None)
        self.rect = pygame.Rect((0, 0), (GRID_SIZE, GRID_SIZE))  # 애니메이션 한 프레임 크기를 GRID_SIZE 기준으로 설정
        self.rect.center = pos                   # 스프라이트의 중심 좌표를 지정된 위치에 맞춤

    def update(self):                            # 프레임마다 애니메이션을 한 단계씩 진행
        self.image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)  # 투명 배경의 이미지 Surface 생성
        self.image.blit(self.spritesheet, (0, 0),  # 전체 스프라이트 시트에서 현재 프레임에 해당하는 영역만 잘라서 출력
                        pygame.Rect(
                            self.current_image[0] * self.rect.width,  # x 위치 = 열 인덱스 * 프레임 너비
                            self.current_image[1] * self.rect.height, # y 위치 = 행 인덱스 * 프레임 높이
                            self.rect.width, self.rect.height         # 잘라낼 크기 = 한 프레임 크기
                        ))

        # 현재 행에서 마지막 열까지 다 돌았는지 확인
        if self.current_image[0] + 1 >= self.spritesheet.get_width() // self.rect.width:
            # 현재 행이 마지막 행인지 확인
            if self.current_image[1] + 1 >= self.spritesheet.get_height() // self.rect.height:
                self.kill()  # 마지막 프레임까지 재생했으면 스프라이트 삭제 (애니메이션 종료)
            else:
                self.current_image = (0, self.current_image[1] + 1)  # 다음 행의 첫 번째 열로 이동
        else:
            self.current_image = (self.current_image[0] + 1, self.current_image[1])  # 다음 열로 이동 (같은 행)
