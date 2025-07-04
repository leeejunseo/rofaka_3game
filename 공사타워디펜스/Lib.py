import pygame, math, os

# Colours
FRAME_COLOUR = pygame.Color("BLACK")
BACKGROUND_COLOUR = pygame.Color(0, 100, 0)  # 어두운 녹색
BUTTON_COLOUR = pygame.Color(66, 235, 244, 0)  # AQUA
TEXT_COLOUR = pygame.Color("WHITE")
SHOP_BACKGROUND_COLOUR = pygame.Color(60, 60, 60, 0)  # Dark Grey
BUTTON_DISABLED_COLOUR = pygame.Color("RED")
PATH_COLOUR = pygame.Color("BLUE")
MOUSE_SELECTOR_COLOUR = pygame.Color("WHITE")

# Global variables
GRID_SIZE = 50

# Directions
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

# Game states
STATE_MAIN_MENU = 1
STATE_PRE_WAVE = 2
STATE_WAVE = 3
STATE_PAUSED = 4
STATE_GAME_OVER = 5

# Custom events
ENEMY_REACHED_END = pygame.USEREVENT+1
ENEMY_KILLED = pygame.USEREVENT+2
TOWER_BOUGHT = pygame.USEREVENT+3
EVENT_STATE_CHANGED = pygame.USEREVENT+4

def get_korean_font(size):
    font_path = os.path.join("assets", "TmonMonsori.ttf.ttf")
    return pygame.font.Font(font_path, size)

def negateCoords(coords):
    return tuple([-coords[0], -coords[1]])


def adjustCoordsByOffset(coords, offset):
    return tuple([coords[0]-offset[0], coords[1]-offset[1]])


def posToGridCoords(pos, grid_size):
    return tuple([pos[0] // grid_size, pos[1] // grid_size])


def gridCoordToPos(grid_coord, grid_size):
    return tuple([grid_coord[0]*grid_size + grid_size//2, grid_coord[1]*grid_size + grid_size//2])


def getDistance(pos1, pos2):
    return math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)


def getDirection(pos1, pos2):
    if abs(pos1[0]-pos2[0]) > abs(pos1[1]-pos2[1]):
        if pos1[0] > pos2[0]:
            return LEFT
        else:
            return RIGHT
    else:
        if pos1[1] > pos2[1]:
            return UP
        else:
            return DOWN

class Path(pygame.sprite.Sprite):
    def __init__(self, colour, waypoints=[], grid_size=50):
        pygame.sprite.Sprite.__init__(self)

        # 경로 크기 계산
        highest_x = max(point[0] for point in waypoints)
        highest_y = max(point[1] for point in waypoints)

        self.grid_size = grid_size
        self.image = pygame.Surface(((highest_x + 3) * grid_size, (highest_y + 3) * grid_size), pygame.SRCALPHA)
        self.image.fill(BACKGROUND_COLOUR)
        self.rect = self.image.get_rect()

        self.colour = colour
        self.waypoints = waypoints
        self.rectangles = []
        self.blocked_areas = []

        self.generateRectangles()

        # 🎨 이미지 삽입 (200x300)
        self.monument_img = pygame.image.load("assets/성무탑.png").convert_alpha()
        self.af_emblem_img = pygame.image.load("assets/정문.png").convert_alpha()

        
      
        # 지도 상 위치 설정 (격자 5,2 → 픽셀 250,100)
        self.monument_pos = (10 * grid_size, 2 * grid_size)
        self.image.blit(self.monument_img, self.monument_pos)
        self.af_emblem_pos = (2 * grid_size, 1 * grid_size)
        self.image.blit(self.af_emblem_img, self.af_emblem_pos)

        # 설치 금지 영역 등록 (200x300)
        monument_rect = pygame.Rect(self.monument_pos[0], self.monument_pos[1], 200, 300)
        self.blocked_areas.append(monument_rect)       
        af_emblem_rect = pygame.Rect(self.af_emblem_pos[0], self.af_emblem_pos[1], 100, 100)
        self.blocked_areas.append(af_emblem_rect)

    def addToPath(self, coords):
        self.waypoints.append(coords)
        self.generateRectangles()

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
            pygame.draw.rect(self.image, self.colour, rect)
            self.rectangles.append(rect)

    def contains(self, point):
        for rect in self.rectangles:
            if rect.collidepoint(point):
                return True
        for rect in self.blocked_areas:
            if rect.collidepoint(point):
                return True
        return False
