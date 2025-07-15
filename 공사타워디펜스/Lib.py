import pygame, math, os  # pygame: 게임 그래픽/입력 처리, math: 수학 연산, os: 파일 경로 관리 등

# ==========================
# 🎨 색상 상수 정의
# ==========================

FRAME_COLOUR = pygame.Color("BLACK")  # UI 테두리 등 프레임용 색상 (검정)
BACKGROUND_COLOUR = pygame.Color(0, 100, 0)  # 배경색: 어두운 녹색
BUTTON_COLOUR = pygame.Color(66, 235, 244, 0)  # 버튼 색: 밝은 아쿠아, 투명도 포함
TEXT_COLOUR = pygame.Color("WHITE")  # 텍스트 색상: 흰색
SHOP_BACKGROUND_COLOUR = pygame.Color(60, 60, 60, 0)  # 상점 배경색: 어두운 회색 + 투명
BUTTON_DISABLED_COLOUR = pygame.Color("RED")  # 비활성 버튼 색: 빨간색
PATH_COLOUR = pygame.Color("BLUE")  # 적 이동 경로 색: 파란색
MOUSE_SELECTOR_COLOUR = pygame.Color("WHITE")  # 마우스 셀렉터 표시 색: 흰색

# ==========================
# 📐 기본 상수 정의
# ==========================

GRID_SIZE = 50  # 격자의 한 칸 크기 (픽셀 단위) → 50x50 픽셀

# ==========================
# 🔀 방향 상수 정의
# ==========================

UP = 0     # 위쪽 방향
RIGHT = 1  # 오른쪽 방향
DOWN = 2   # 아래쪽 방향
LEFT = 3   # 왼쪽 방향

# ==========================
# 🎮 게임 상태 코드
# ==========================

STATE_MAIN_MENU = 1     # 메인 메뉴 상태
STATE_PRE_WAVE = 2      # 웨이브 준비 상태 (전투 시작 전)
STATE_WAVE = 3          # 웨이브 진행 중 상태
STATE_PAUSED = 4        # 게임 일시정지 상태
STATE_GAME_OVER = 5     # 게임 오버 상태

# ==========================
# 🧩 사용자 정의 이벤트
# ==========================

ENEMY_REACHED_END = pygame.USEREVENT + 1      # 적이 경로 끝에 도달했을 때 발생
ENEMY_KILLED = pygame.USEREVENT + 2           # 적이 죽었을 때 발생
TOWER_BOUGHT = pygame.USEREVENT + 3           # 타워를 구매했을 때 발생
EVENT_STATE_CHANGED = pygame.USEREVENT + 4    # 게임 상태가 전환될 때 발생

# ==========================
# 🈷 한글 폰트 로드 함수
# ==========================

def get_korean_font(size):
    font_path = os.path.join("assets", "TmonMonsori.ttf.ttf")  # assets 폴더 내 한글 폰트 파일 경로
    return pygame.font.Font(font_path, size)  # 해당 경로의 폰트를 지정한 크기로 불러오기

# ==========================
# 🧭 좌표 관련 유틸 함수
# ==========================

# (x, y) 좌표의 부호를 반전 → (-x, -y)로 반환
def negateCoords(coords):
    return tuple([-coords[0], -coords[1]])

# offset만큼 좌표를 보정 (ex: 마우스 좌표 - 화면 오프셋)
def adjustCoordsByOffset(coords, offset):
    return tuple([coords[0] - offset[0], coords[1] - offset[1]])

# 실제 화면상의 픽셀 좌표를 → 격자 좌표(x칸, y칸)로 변환
def posToGridCoords(pos, grid_size):
    return tuple([pos[0] // grid_size, pos[1] // grid_size])

# 격자 좌표를 중심 기준의 픽셀 좌표로 변환
def gridCoordToPos(grid_coord, grid_size):
    return tuple([
        grid_coord[0] * grid_size + grid_size // 2,  # x 위치
        grid_coord[1] * grid_size + grid_size // 2   # y 위치
    ])

# 두 위치 좌표 간 거리 계산 (피타고라스 정리)
def getDistance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

# pos1에서 pos2 방향을 계산해 UP/DOWN/LEFT/RIGHT 중 하나를 반환
def getDirection(pos1, pos2):
    if abs(pos1[0] - pos2[0]) > abs(pos1[1] - pos2[1]):  # x 차이가 더 크면 수평 방향
        if pos1[0] > pos2[0]:
            return LEFT
        else:
            return RIGHT
    else:  # y 차이가 더 크면 수직 방향
        if pos1[1] > pos2[1]:
            return UP
        else:
            return DOWN

# ==========================
# 🛣️ Path 클래스: 적의 이동 경로 시각화 및 충돌 체크
# ==========================

class Path(pygame.sprite.Sprite):  # Pygame의 Sprite로 생성 가능 (화면에 표시됨)
    def __init__(self, colour, waypoints=[], grid_size=50):
        pygame.sprite.Sprite.__init__(self)  # 부모 초기화

        # 가장 오른쪽, 아래쪽 좌표를 이용해 전체 이미지 크기를 결정
        highest_x = max(point[0] for point in waypoints)  # x 좌표 중 최대값
        highest_y = max(point[1] for point in waypoints)  # y 좌표 중 최대값

        self.grid_size = grid_size  # 격자 크기 설정

        # 전체 경로용 Surface 생성 (여유 있게 +3칸 더 확보)
        self.image = pygame.Surface(((highest_x + 3) * grid_size,
                                     (highest_y + 3) * grid_size), pygame.SRCALPHA)

        self.image.fill(BACKGROUND_COLOUR)  # 배경 색상 채우기
        self.rect = self.image.get_rect()   # rect 생성

        self.colour = colour          # 경로 색상
        self.waypoints = waypoints    # 이동 경로 웨이포인트 리스트
        self.rectangles = []          # 경로 박스(사각형) 리스트
        self.blocked_areas = []       # 설치 불가능한 영역 저장 리스트

        self.generateRectangles()     # 초기 경로 박스 생성

        # 배경 장식용 이미지 로딩 (성무탑, 정문 등)
        self.monument_img = pygame.image.load("assets/성무탑.png").convert_alpha()
        self.af_emblem_img = pygame.image.load("assets/정문.png").convert_alpha()

        # 성무탑 위치 지정 및 그리기
        self.monument_pos = (10 * grid_size, 2 * grid_size)
        self.image.blit(self.monument_img, self.monument_pos)

        # 정문 위치 지정 및 그리기
        self.af_emblem_pos = (2 * grid_size, 1 * grid_size)
        self.image.blit(self.af_emblem_img, self.af_emblem_pos)

        # 이미지 영역을 설치 불가 영역으로 등록 (탑 200x300, 정문 100x100)
        monument_rect = pygame.Rect(self.monument_pos[0], self.monument_pos[1], 200, 300)
        self.blocked_areas.append(monument_rect)

        af_emblem_rect = pygame.Rect(self.af_emblem_pos[0], self.af_emblem_pos[1], 100, 100)
        self.blocked_areas.append(af_emblem_rect)

    # 새로운 웨이포인트를 경로에 추가하고 경로 사각형을 다시 생성
    def addToPath(self, coords):
        self.waypoints.append(coords)     # 웨이포인트 추가
        self.generateRectangles()         # 경로 갱신

    # 경로 사각형 생성 함수 (웨이포인트들을 직선으로 연결하는 사각형 생성)
    def generateRectangles(self):
        self.rectangles = []  # 기존 경로 초기화
        for i in range(len(self.waypoints) - 1):  # 두 점씩 순차 연결
            first_pos = self.waypoints[i]
            second_pos = self.waypoints[i + 1]

            # 연결할 두 점 중 더 작은 좌표 찾기 (사각형 top-left)
            top_left = (min(first_pos[0], second_pos[0]), min(first_pos[1], second_pos[1]))
            bottom_right = (max(first_pos[0], second_pos[0]), max(first_pos[1], second_pos[1]))

            # 경로 사각형 영역 계산 (격자 좌표 → 픽셀 좌표)
            rect = pygame.Rect(
                top_left[0] * self.grid_size,
                top_left[1] * self.grid_size,
                (bottom_right[0] + 1 - top_left[0]) * self.grid_size,
                (bottom_right[1] + 1 - top_left[1]) * self.grid_size
            )

            pygame.draw.rect(self.image, self.colour, rect)  # 이미지에 경로 색상으로 채움
            self.rectangles.append(rect)  # 생성된 사각형 저장

    # 특정 좌표가 경로(또는 금지영역)에 포함되는지 여부 확인
    def contains(self, point):
        for rect in self.rectangles:           # 경로 사각형들 검사
            if rect.collidepoint(point):
                return True
        for rect in self.blocked_areas:        # 금지 영역 검사
            if rect.collidepoint(point):
                return True
        return False                           # 아무 곳에도 포함되지 않으면 False
