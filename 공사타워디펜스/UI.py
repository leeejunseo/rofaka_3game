import pygame
from Lib import (
    get_korean_font,
    TEXT_COLOUR,
    SHOP_BACKGROUND_COLOUR,
    MOUSE_SELECTOR_COLOUR,
    adjustCoordsByOffset
)


class Button(pygame.sprite.Sprite):
    def __init__(self, rect, text, background_colour, text_colour, text_size):
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.text = text
        self.__background_colour = background_colour
        self.text_colour = text_colour
        self.text_size = text_size
        self.create_image()

    @property
    def background_colour(self):
        return self.__background_colour

    @background_colour.setter
    def background_colour(self, colour):
        self.__background_colour = colour
        self.create_image()

    def contains(self, point):
        """Used to test if the mouse clicked on the button"""
        return self.rect.collidepoint(point)

    def create_image(self):
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(self.background_colour)

        # Write the text to the button
        font = get_korean_font(self.text_size)
        text_surf = font.render(self.text, 1, self.text_colour)
        self.image.blit(text_surf, (self.rect.width / 2 - text_surf.get_width() / 2,
                                    self.rect.height / 2 - text_surf.get_height() / 2))


class TextDisplay(pygame.sprite.Sprite):
    def __init__(self, rect, text, text_colour, text_size):
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect
        self.image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.__text = text
        self.text_colour = text_colour
        self.text_size = text_size
        self.create_image()

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, new_text):
        self.__text = new_text
        self.create_image()

    def create_image(self):
        self.image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)

        # Create text
        font = get_korean_font(self.text_size)
        text_surf = font.render(self.text, 1, self.text_colour)
        self.image.blit(text_surf, (self.rect.width / 2 - text_surf.get_width() / 2,
                                    self.rect.height / 2 - text_surf.get_height() / 2))


class ShopButton(Button):
    def __init__(self, tower_model, pos, text_size, text_colour):
        pygame.sprite.Sprite.__init__(self)
        self.model = tower_model
        self.text_size = text_size
        sprite = pygame.image.load(tower_model.sprite_location)
        font = get_korean_font(self.text_size)
        text_surf = font.render(tower_model.name, 1, text_colour)
        self.rect = pygame.Rect(pos, (text_surf.get_rect().width + sprite.get_rect().width + 10, sprite.get_rect().height + 10))
        self.image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.image.blit(sprite, (0, 5))
        self.image.blit(text_surf, (sprite.get_rect().width + 10, 0))


class Shop():
    def __init__(self, screen, rect, tower_models):
        self.rect = rect
        screen_width, screen_height = screen.get_size()

        # Shop UI 위치 및 크기 설정 (오른쪽 상단에 위치하도록)
        shop_width = 400
        shop_height = 800  # ← 화면 높이에 맞게 조정
        shop_x = screen_width - shop_width - 20  # 오른쪽에서 약간 떨어지게
        shop_y = 100  # 위에서부터의 거리

        # 잘리는 오류 방지: 범위 체크
        if shop_x < 0 or shop_y < 0 or shop_x + shop_width > screen_width or shop_y + shop_height > screen_height:
            raise ValueError("Shop UI 영역이 화면 범위를 벗어납니다!")

        rect = pygame.Rect(shop_x, shop_y, shop_width, shop_height)
        self.image = screen.subsurface(rect)
        self.title = TextDisplay(pygame.Rect(50, 50, 300, 80), "Shop", TEXT_COLOUR, 60)
        self.tower_models = tower_models
        self.buttons = []
        self.info_popups = []
        current_y = 250
        for tower in tower_models:
            self.buttons.append(ShopButton(tower, (30, current_y), 30, TEXT_COLOUR))
            popup_x = 20               # x 위치 왼쪽으로
            popup_y = current_y - 80   # 버튼보다 위에 띄우기
            bg_color = (30, 30, 30)    # 어두운 회색
            text_color = (255, 255, 0) # 노란색

            self.info_popups.append([
                Button(pygame.Rect(popup_x, popup_y, 360, 40), f"Cost: {tower.value}", bg_color, text_color, 25),
                Button(pygame.Rect(popup_x, popup_y + 45, 360, 40), tower.description, bg_color, text_color, 20)
            ])

            current_y += 60

    def render(self, selected):
        mouse_pos = adjustCoordsByOffset(pygame.mouse.get_pos(), self.image.get_abs_offset())
        self.image.fill(SHOP_BACKGROUND_COLOUR)
        self.image.blit(self.title.image, self.title.rect)
        for button in self.buttons:
            self.image.blit(button.image, button.rect)
        pygame.draw.rect(self.image, MOUSE_SELECTOR_COLOUR, self.buttons[selected].rect, 2)

        for i in range(len(self.buttons)):
            button = self.buttons[i]
            if button.contains(mouse_pos):
                popup = self.info_popups[i]
                for p in popup:
                    self.image.blit(p.image, p.rect)


    def button_pressed(self, point):
        """Returns the index of the button if one was pressed, or -1 if not"""
        for i in range(len(self.buttons)):
            if self.buttons[i].contains(point):
                return i
        return -1
