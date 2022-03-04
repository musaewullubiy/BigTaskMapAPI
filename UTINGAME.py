import pygame
from SupportFuncs import load_image


class URadioButtons(pygame.sprite.Sprite):
    def __init__(self, screen, coords, group):
        super(URadioButtons, self).__init__(group)
        self.coords = coords
        self.buttons = []
        self.checked_button = 0
        self.font = pygame.font.Font('font/arial.ttf', 15)
        self.screen = screen
        self.draw()

    def draw(self):
        self.image = pygame.Surface((65 * len(self.buttons), 50), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = self.coords[0]
        self.rect.y = self.coords[1]
        for i in range(len(self.buttons)):
            color = (0, 0, 0)
            image_name = 'ui_images/RadioButtonDefault.png'
            if i == self.checked_button:
                color = (255, 0, 0)
                image_name = 'ui_images/RadioButtonChecked.png'
            text_pg = self.font.render(self.buttons[i][0], True, color)
            btn_img = pygame.transform.scale(load_image(image_name, colorkey=-1),
                                             (50, 50))
            self.image.blit(btn_img, (50 * i + 5 * (i + 1), 0))
            self.image.blit(text_pg, (50 * i + 10 + 5 * (i + 1), 40 - text_pg.get_height()))
            self.screen.blit(self.image, (self.coords[0], self.coords[1]))

    def click_check(self, pos):
        if pygame.sprite.collide_rect(pos, self):
            cell_x = (pos.rect.x - 10) // 50 - self.coords[0] // 50
            cell_y = (pos.rect.y - 10) // 50
            if cell_x < 0 or cell_x >= len(self.buttons) or cell_y != 0:
                return
            self.checked_button = cell_x
            self.buttons[cell_x][1]()
            self.draw()

    def hover_check(self, pos):
        pass

    def add_button(self, text, func):
        self.buttons.append([text, func])


class ULineEdit(pygame.sprite.Sprite):
    def __init__(self, screen, coords, group):
        super(ULineEdit, self).__init__(group)
        self.font = pygame.font.Font('font/arial.ttf', 15)
        self.screen = screen
        self.coords = coords
        self.text = ''
        self.en_to_ru = {'A': 'ф', 'B': 'и', 'C': 'с',
                         'D': 'в', 'E': 'у', 'F': 'а',
                         'G': 'п', 'H': 'р', 'I': 'ш',
                         'J': 'о', 'K': 'л', 'L': 'д',
                         'M': 'ь', 'N': 'т', 'O': 'щ',
                         'P': 'з', 'Q': 'й', 'R': 'к',
                         'S': 'ы', 'T': 'е', 'U': 'г',
                         'V': 'м', 'W': 'ц', 'X': 'ч',
                         'Y': 'н', 'Z': 'я', ',': 'б',
                         '.': 'ю', ';': 'ж', '\'': 'э',
                         '[': 'х', ']': 'ъ', '/': ','}
        self.draw()

    def draw(self):
        self.image = pygame.Surface((200, 50), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = self.coords[0]
        self.rect.y = self.coords[1]
        self.image.blit(pygame.transform.scale(load_image('ui_images/LineEdit.png', colorkey=-1), (200, 50)), (0, 0))
        text_pg = self.font.render(self.text, True, (0, 0, 0))
        self.image.blit(text_pg, (10, 40 - text_pg.get_height()))
        self.screen.blit(self.image, (self.coords[0], self.coords[1]))

    def click_check(self, pos):
        pass

    def hover_check(self, pos, event):
        if pygame.sprite.collide_rect(pos, self):
            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                if key == 'backspace':
                    if len(self.text) >= 1:
                        self.text = self.text[:-1]
                elif key.upper() in self.en_to_ru:
                    self.text += self.en_to_ru[key.upper()]
                elif key.isdigit():
                    self.text += key
                elif key == 'space':
                    self.text += ' '

    def get_text(self):
        return self.text

    def set_text(self, text):
        self.text = text


class UButton(pygame.sprite.Sprite):
    def __init__(self, screen, coords, group, text, func, image_name='ui_images/ButtonBlue.png'):
        super(UButton, self).__init__(group)
        self.font = pygame.font.Font('font/arial.ttf', 15)
        self.screen = screen
        self.coords = coords
        self.text = text
        self.func = func
        self.image_name = image_name
        self.draw()

    def draw(self):
        self.image = pygame.Surface((70, 50), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = self.coords[0]
        self.rect.y = self.coords[1]
        self.image.blit(pygame.transform.scale(load_image(self.image_name, colorkey=-1), (70, 50)), (0, 0))
        text_pg = self.font.render(self.text, True, (0, 0, 0))
        self.image.blit(text_pg, (10, 40 - text_pg.get_height()))
        self.screen.blit(self.image, (self.coords[0], self.coords[1]))

    def hover_check(self, pos):
        pass

    def click_check(self, pos):
        if pygame.sprite.collide_rect(pos, self):
            self.func()


class ULabel(pygame.sprite.Sprite):
    def __init__(self, screen, coords, group, text, height=40, font_size=10):
        super(ULabel, self).__init__(group)
        self.font_size = font_size
        self.font = pygame.font.Font('font/arial.ttf', self.font_size)
        self.screen = screen
        self.coords = coords
        self.text = text
        self.height = height
        self.on_flag = True
        self.draw()

    def draw(self):
        if self.on_flag:
            self.image = pygame.Surface((len(self.text) * self.font_size * 0.55, self.height), pygame.SRCALPHA)
            self.rect = self.image.get_rect()
            self.rect.x = self.coords[0]
            self.rect.y = self.coords[1]
            self.image.blit(pygame.transform.scale(load_image('ui_images/Label.png', colorkey=-1),
                                                   (len(self.text) * self.font_size * 0.55, self.height)), (0, 0))
            text_pg = self.font.render(self.text, True, (0, 0, 0))
            self.image.blit(text_pg, (10, self.height - text_pg.get_height()))
            self.screen.blit(self.image, (self.coords[0], self.coords[1]))

    def set_text(self, text):
        self.text = text

    def off_on(self):
        self.on_flag = not self.on_flag
        print(self.on_flag)
