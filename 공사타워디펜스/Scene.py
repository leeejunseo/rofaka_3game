from UI import *
from Towers import *
from Wave import *
from Enemies import *
from Lib import (
    BUTTON_COLOUR,
    TEXT_COLOUR,
    BUTTON_DISABLED_COLOUR,
    PATH_COLOUR,
    MOUSE_SELECTOR_COLOUR,
    FRAME_COLOUR,
    STATE_PAUSED,
    GRID_SIZE,  # ← 이 줄 추가
    Path
)


class Scene:
    """Abstract class"""
    def __init__(self, screen_size, screen):
        """Override in child classes"""
        # Creates a sub surface as the game screen.
        # This means anything blitted to the game screen is automatically put on the screen (more efficient)
        # Also handles relative coords with get_abs_offset()
        self.rect = pygame.Rect(100, 100, screen_size[0] - 200, screen_size[1] - 100)  # 아래 공간 줄이지 않음

        self.game_screen = screen.subsurface(self.rect)

    def update(self, **kwargs):
        """Updates the scene. Meant to be called once a frame. Override in child classes"""
        pass

    def render(self, **kwargs):
        """Renders the scene. Meant to be called once a frame. Override in child classes"""
        pass


class GameOver(Scene):
    def __init__(self, screen_size, screen):
        self.rect = pygame.Rect(0, 0, screen_size[0], screen_size[1])

        self.screen = screen.subsurface(self.rect)
        self.title = TextDisplay(pygame.Rect((screen_size[0]//2-300, screen_size[1]//3), (600, 100)), "GAME OVER", TEXT_COLOUR, 100)
        self.survival_message = TextDisplay(pygame.Rect((screen_size[0]//2-300, screen_size[1]//2), (600, 100)), "You survived until wave 999", TEXT_COLOUR, 50)
        self.main_menu_button = Button(pygame.Rect((screen_size[0]//2-225, 2*screen_size[1]//3-50), (450, 100)), "Main Menu", BUTTON_COLOUR, TEXT_COLOUR, 100)

    def render(self, **kwargs):
        
        self.screen.blit(self.title.image, self.title.rect)
        self.screen.blit(self.survival_message.image, self.survival_message.rect)
        self.screen.blit(self.main_menu_button.image, self.main_menu_button.rect)


class MainMenu(Scene):
    def __init__(self, screen_size, screen):
        self.rect = pygame.Rect(0, 0, screen_size[0], screen_size[1])
        self.menu_screen = screen.subsurface(self.rect)

        self.title = TextDisplay(pygame.Rect(0, 100, screen_size[0], 100), "공사타워디펜스", TEXT_COLOUR, 100)

        self.instructions = []
        self.instructions.append(TextDisplay(pygame.Rect(0, 300, screen_size[0], 65), "좌클릭으로 타워를 배치할 수 있습니다.", TEXT_COLOUR, 40))
        self.instructions.append(TextDisplay(pygame.Rect(0, 365, screen_size[0], 65), "상점에서 클릭이나 숫자를 눌러 구매가 가능합니다.", TEXT_COLOUR, 40))
        self.instructions.append(TextDisplay(pygame.Rect(0, 430, screen_size[0], 65), "우클릭으로 판매가 가능합니다.", TEXT_COLOUR, 40))
        self.instructions.append(TextDisplay(pygame.Rect(0, 495, screen_size[0], 65), "next wave 또는 스페이스바를 눌러 진행할 수 있습니다.", TEXT_COLOUR, 40))
        self.instructions.append(TextDisplay(pygame.Rect(0, 560, screen_size[0], 65), "최대한 오래 살아남으세요!", TEXT_COLOUR, 40))

        self.play_button = Button(pygame.Rect((screen_size[0]/2) - 150, 630, 150, 80),
                                  "시작", BUTTON_COLOUR, TEXT_COLOUR, 40)
        self.quit_button = Button(pygame.Rect((screen_size[0]/2) + 50, 630, 150, 80),
                                  "끄기", BUTTON_COLOUR, TEXT_COLOUR, 40)

    def render(self, **kwargs):
        self.menu_screen.blit(self.title.image, self.title.rect)
        for instruction in self.instructions:
            self.menu_screen.blit(instruction.image, instruction.rect)
        self.menu_screen.blit(self.play_button.image, self.play_button.rect)
        self.menu_screen.blit(self.quit_button.image, self.quit_button.rect)


class Pause(Scene):
    def __init__(self, screen_size, screen):
        self.rect = pygame.Rect(100, 100, screen_size[0]-200, screen_size[1]-200)
        self.pause_overlay = screen.subsurface(self.rect)
        self.pause_message = TextDisplay(pygame.Rect(360, 200, 180, 60), "PAUSED", TEXT_COLOUR, 40)
        self.resume_button = Button(pygame.Rect(200, 340, 225, 75),
                                    "재개하기", BUTTON_COLOUR, TEXT_COLOUR, 40)
        self.quit_button = Button(pygame.Rect(475, 340, 225, 75),
                                  "메인 메뉴", BUTTON_COLOUR, TEXT_COLOUR, 40)

    def render(self, **kwargs):
        kwargs["SCENE_GAME"].render(screen=kwargs["screen"], current_state=kwargs["current_state"])
        self.pause_overlay.blit(self.pause_message.image, self.pause_message.rect)
        self.pause_overlay.blit(self.resume_button.image, self.resume_button.rect)
        self.pause_overlay.blit(self.quit_button.image, self.quit_button.rect)


class Game(Scene):
    def __init__(self, screen_size, screen):
        self.screen_size = screen_size
        self.rect = pygame.Rect(100, 100, screen_size[0]-200, screen_size[1]-200)
        self.game_screen = screen.subsurface(self.rect)
        self.offset = self.game_screen.get_abs_offset()

        self.special_wave_message = None
        self.special_wave_timer = 0

        # Groups for sprites
        self.towers = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.effects = pygame.sprite.Group()

        # Game variables
        self.lives = 0
        self.money = 999999
        self.selected_tower = 0
        self.path = Path(PATH_COLOUR,
                         [(1, -1), (1, 5), (4, 5), (4, 1), (6, 1), (6, 5), (8, 5), (8, 1), (17, 1), (17, 5), (14, 5),
                          (14, 8), (17, 8), (17, 11), (12, 11), (12, 8), (9, 8), (9, 11), (7, 11), (7, 8), (5, 8),
                          (5, 11), (3, 11), (3, 8), (-1, 8)])
        self.wave_handler = WaveHandler(self.path.waypoints[0])
        self.enemies_alive = 0

        # Tower models (available towers to build)
        self.tower_models = []
        
        # 1. 보좌관 Tower (데미지, 공격속도(높을수록 빠름), 사거리, 비용)
        tower_model = TowerModel("보좌관 Tower", 1, 20, 2, 100, pygame.Color("GREEN"), 'assets/tower1.png', "낮은 공격력, 좁은 범위, 빠른 속도")
        self.tower_models.append(tower_model)

        # 2. 기수 Tower
        tower_model = TowerModel("기수 Tower", 3, 100, 5, 300, pygame.Color("WHITE"), 'assets/tower2.png', "높은 데미지, 넓은 범위, 느린 속도")
        self.tower_models.append(tower_model)

        # 3. 작참 Tower – 중간 사거리, 중간 데미지
        tower_model = TowerModel("작전참모 Tower", 2, 50, 3, 150, pygame.Color("RED"), 'assets/tower3.png', "보통의 데미지와 속도")
        self.tower_models.append(tower_model)

        # 4. 징계 Tower – 느리지만 강력함
        tower_model = TowerModel("징계 Tower", 3, 120, 6, 400, pygame.Color("PURPLE"), 'assets/tower4.png', "느리지만 강력")
        self.tower_models.append(tower_model)

        # 5. 초과벌점 Tower – 빠른 공격 속도
        tower_model = TowerModel("초과벌점 Tower", 0.5, 10, 1, 120, pygame.Color("ORANGE"), 'assets/tower5.png', "매우 빠른 속도")
        self.tower_models.append(tower_model)

        # 6. Ice Tower – 적을 느리게 만듦 (슬로우 효과 구현 필요)
        tower_model = TowerModel("기말고사 Tower", 2, 10, 2, 180, pygame.Color("CYAN"), 'assets/tower6.png', "맞으면 슬로우 효과")
        self.tower_models.append(tower_model)

        

        # Top bar elements
        self.next_wave_button = Button(pygame.Rect(100, 25, 160, 50), "다음 스테이지", BUTTON_COLOUR, TEXT_COLOUR, 20)
        self.pause_button = Button(pygame.Rect(270, 25, 95, 50), "중지", BUTTON_DISABLED_COLOUR, TEXT_COLOUR, 20)
        self.wave_display = TextDisplay(pygame.Rect(375, 25, 210, 50), "현재 웨이브 : " + str(self.wave_handler.current_wave_number), TEXT_COLOUR, 20)
        self.enemy_count_display = TextDisplay(pygame.Rect(595, 25, 280, 50), "남은 메추리 : " + str(self.enemies_alive), TEXT_COLOUR, 20)
        self.lives_display = TextDisplay(pygame.Rect(885, 25, 230, 50), "탈출한 메추리 : " + str(self.lives), TEXT_COLOUR, 20)
        self.money_display = TextDisplay(pygame.Rect(1015, 25, 500, 50), "돈 : " + str(self.money), TEXT_COLOUR, 20)

        # Shop elements
        self.shop = Shop(screen, pygame.Rect(adjustCoordsByOffset(self.path.rect.topright, (-self.offset[0], -self.offset[1])), (400, self.path.rect.height)), self.tower_models)

    def update(self, **kwargs):
        self.wave_handler.update(self.enemies, self)
        self.enemies.update(self.path.waypoints, GRID_SIZE)
        self.towers.update(self.enemies, self.effects, self.game_screen)
        self.effects.update()
        self.money_display.text = "Money: " + str(self.money)
        if self.special_wave_timer > 0:
            self.special_wave_timer -= 1
            if self.special_wave_timer == 0:
                self.special_wave_message = None  # 타이머 끝나면 메시지 제거

    def render(self, **kwargs):
        screen = kwargs['screen']
        screen.fill(pygame.Color("BLACK"))

        # Render top bar
        screen.blit(self.next_wave_button.image, self.next_wave_button.rect)
        screen.blit(self.pause_button.image, self.pause_button.rect)
        screen.blit(self.wave_display.image, self.wave_display.rect)
        screen.blit(self.enemy_count_display.image, self.enemy_count_display.rect)
        screen.blit(self.lives_display.image, self.lives_display.rect)
        screen.blit(self.money_display.image, self.money_display.rect)

        # Render Game
        self.game_screen.fill(FRAME_COLOUR)
        self.game_screen.blit(self.path.image, (0, 0))
        self.enemies.draw(self.game_screen)
        self.towers.draw(self.game_screen)
        self.effects.draw(self.game_screen)

        # Render shop
        self.shop.render(self.selected_tower)
        if self.special_wave_message and self.special_wave_timer > 0:
            font = pygame.font.Font("assets/TmonMonsori.ttf.ttf", 40)
            text_surface = font.render(self.special_wave_message, True, pygame.Color("RED"))
            text_rect = text_surface.get_rect(center=(self.screen_size[0]//2, self.screen_size[1]//2))
            screen.blit(text_surface, text_rect)

        # Update mouse selector
        if kwargs["current_state"] != STATE_PAUSED:  # Won't display mouse selector if game is paused
            mouse_pos = pygame.mouse.get_pos()
            mouse_pos = (mouse_pos[0] - self.offset[0], mouse_pos[1] - self.offset[1])  # Accounts for the border
            if not self.path.contains(mouse_pos):
                if 0 < mouse_pos[0] < self.path.rect.width and 0 < mouse_pos[1] < self.path.rect.height:
                    if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:  # Mouse selector is bigger if the mouse button is down
                        size = 5
                    else:
                        size = 2
                    pygame.draw.rect(self.game_screen, MOUSE_SELECTOR_COLOUR,
                                     pygame.Rect(mouse_pos[0] - (mouse_pos[0] % GRID_SIZE),
                                                 mouse_pos[1] - (mouse_pos[1] % GRID_SIZE),
                                                 GRID_SIZE, GRID_SIZE), size)

