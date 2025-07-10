import pygame, math, os  # 게임 화면 구성, 수학 연산, 경로 접근을 위한 모듈

# 색상 정의
FRAME_COLOUR = pygame.Color("BLACK")  # 테두리 색
BACKGROUND_COLOUR = pygame.Color(0, 100, 0)  # 어두운 녹색 배경
BUTTON_COLOUR = pygame.Color(66, 235, 244, 0)  # 버튼 색 (AQUA)
TEXT_COLOUR = pygame.Color("WHITE")  # 흰색 텍스트
SHOP_BACKGROUND_COLOUR = pygame.Color(60, 60, 60, 0)  # 상점 배경 (짙은 회색)
BUTTON_DISABLED_COLOUR = pygame.Color("RED")  # 비활성화된 버튼 색
PATH_COLOUR = pygame.Color("BLUE")  # 경로 색상
MOUSE_SELECTOR_COLOUR = pygame.Color("WHITE")  # 마우스 선택 표시 색

# 전역 상수: 격자 크기
GRID_SIZE = 50  # 한 칸의 픽셀 크기

# 방향 상수 정의
UP = 0     # 위쪽
RIGHT = 1  # 오른쪽
DOWN = 2   # 아래쪽
LEFT = 3   # 왼쪽

# 게임 상태 정의
STATE_MAIN_MENU = 1     # 메인 메뉴 상태
STATE_PRE_WAVE = 2      # 웨이브 시작 전
STATE_WAVE = 3          # 웨이브 중
STATE_PAUSED = 4        # 일시 정지
STATE_GAME_OVER = 5     # 게임 오버

# 사용자 정의 이벤트 정의
ENEMY_REACHED_END = pygame.USEREVENT + 1  # 적이 끝점에 도달함
ENEMY_KILLED = pygame.USEREVENT + 2       # 적이 처치됨
TOWER_BOUGHT = pygame.USEREVENT + 3       # 타워 구매됨
EVENT_STATE_CHANGED = pygame.USEREVENT + 4  # 상태 전환 이벤트

# 한글 폰트 불러오기 함수
def get_korean_font(size):
    font_path = os.path.join("assets", "TmonMonsori.ttf.ttf")  # 폰트 경로 지정
    return pygame.font.Font(font_path, size)  # 폰트 객체 반환

# 좌표 반전 함수
def negateCoords(coords):
    return tuple([-coords[0], -coords[1]])  # x, y 모두 부호 반전

# 오프셋 보정 좌표 계산 함수
def adjustCoordsByOffset(coords, offset):
    return tuple([coords[0] - offset[0], coords[1] - offset[1]])  # 오프셋만큼 좌표 보정

# 픽셀 좌표 → 격자 좌표 변환
def posToGridCoords(pos, grid_size):
    return tuple([pos[0] // grid_size, pos[1] // grid_size])

# 격자 좌표 → 픽셀 좌표 변환 (격자 중심 기준)
def gridCoordToPos(grid_coord, grid_size):
    return tuple([grid_coord[0] * grid_size + grid_size // 2,
                  grid_coord[1] * grid_size + grid_size // 2])

# 두 좌표 사이의 거리 계산
def getDistance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

# 두 좌표의 상대적 방향 계산
def getDirection(pos1, pos2):
    if abs(pos1[0] - pos2[0]) > abs(pos1[1] - pos2[1]):
        if pos1[0] > pos2[0]:
            return LEFT
        else:
            return RIGHT
    else:
        if pos1[1] > pos2[1]:
            return UP
        else:
            return DOWN

# 경로 클래스 정의
class Path(pygame.sprite.Sprite):
    def __init__(self, colour, waypoints=[], grid_size=50):
        pygame.sprite.Sprite.__init__(self)

        # 가장 오른쪽, 아래쪽 좌표를 기반으로 Surface 크기 설정
        highest_x = max(point[0] for point in waypoints)
        highest_y = max(point[1] for point in waypoints)

        self.grid_size = grid_size
        self.image = pygame.Surface(((highest_x + 3) * grid_size,
                                     (highest_y + 3) * grid_size), pygame.SRCALPHA)
        self.image.fill(BACKGROUND_COLOUR)  # 배경 채우기
        self.rect = self.image.get_rect()

        self.colour = colour  # 경로 색상
        self.waypoints = waypoints  # 경유지 리스트
        self.rectangles = []  # 경로 박스 저장용
        self.blocked_areas = []  # 설치 불가 영역

        self.generateRectangles()  # 초기 경로 박스 생성

        # 탑 이미지 및 정문 이미지 불러오기
        self.monument_img = pygame.image.load("assets/성무탑.png").convert_alpha()
        self.af_emblem_img = pygame.image.load("assets/정문.png").convert_alpha()

        # 탑과 정문의 위치 설정
        self.monument_pos = (10 * grid_size, 2 * grid_size)
        self.image.blit(self.monument_img, self.monument_pos)

        self.af_emblem_pos = (2 * grid_size, 1 * grid_size)
        self.image.blit(self.af_emblem_img, self.af_emblem_pos)

        # 이미지가 차지하는 영역을 설치 금지 영역으로 등록
        monument_rect = pygame.Rect(self.monument_pos[0], self.monument_pos[1], 200, 300)
        self.blocked_areas.append(monument_rect)

        af_emblem_rect = pygame.Rect(self.af_emblem_pos[0], self.af_emblem_pos[1], 100, 100)
        self.blocked_areas.append(af_emblem_rect)

    # 새로운 좌표를 경로에 추가
    def addToPath(self, coords):
        self.waypoints.append(coords)
        self.generateRectangles()

    # 경로 사각형 생성 (waypoints 기준)
    def generateRectangles(self):
        self.rectangles = []
        for i in range(len(self.waypoints) - 1):
            first_pos = self.waypoints[i]
            second_pos = self.waypoints[i + 1]
            top_left = (min(first_pos[0], second_pos[0]), min(first_pos[1], second_pos[1]))
            bottom_right = (max(first_pos[0], second_pos[0]), max(first_pos[1], second_pos[1]))
            rect = pygame.Rect(top_left[0] * self.grid_size,
                               top_left[1] * self.grid_size,
                               (bottom_right[0] + 1 - top_left[0]) * self.grid_size,
                               (bottom_right[1] + 1 - top_left[1]) * self.grid_size)
            pygame.draw.rect(self.image, self.colour, rect)  # 경로 칠하기
            self.rectangles.append(rect)

    # 특정 점이 경로 혹은 설치 금지 구역에 포함되는지 확인
    def contains(self, point):
        for rect in self.rectangles:
            if rect.collidepoint(point):
                return True
        for rect in self.blocked_areas:
            if rect.collidepoint(point):
                return True
        return False
