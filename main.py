import pygame
import requests
import sys
import os


def load_image(path, colorkey=None, flag=True):
    if flag:
        fullname = os.path.join(path)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{path}' не найден")
            sys.exit(0)
        image = pygame.image.load(fullname)
    else:
        image = pygame.image.fromstring(path.tobytes(), path.size, path.mode)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class SpriteMouseLocation(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, 1, 1)


class URadioButtons(pygame.sprite.Sprite):
    def __init__(self, screen, coords, group):
        super(URadioButtons, self).__init__(group)
        self.coords = coords
        self.buttons = []
        self.checked_button = 0
        self.font = pygame.font.Font('font/arial.ttf', 30)
        self.screen = screen
        self.draw()

    def draw(self):
        self.image = pygame.Surface((130 * len(self.buttons), 100), pygame.SRCALPHA)
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
            btn_img = pygame.transform.scale(load_image(image_name, colorkey=(255, 255, 255)),
                                             (100, 100))
            self.image.blit(btn_img, (100 * i + 5 * (i + 1), 0))
            self.image.blit(text_pg, (100 * i + 10 + 5 * (i + 1), 80 - text_pg.get_height()))
            self.screen.blit(self.image, (0, 0))

    def click_check(self, pos):
        if pygame.sprite.collide_rect(pos, self):
            cell_x = (pos.rect.x - 10) // 100
            cell_y = (pos.rect.y - 10) // 100
            if cell_x < 0 or cell_x >= len(self.buttons) or cell_y != 0:
                return
            self.checked_button = cell_x
            self.buttons[cell_x][1]()
            self.draw()

    def add_button(self, text, func):
        self.buttons.append([text, func])


def main():
    # coords = input('Введите координаты (через запятую):\n')
    # z = input('Введите маштаб (18 > x > 0):\n')
    coords, z = '30,30', '18'
    show_map(ll=coords, z=z)
    sys.exit()


def generate_img(ll=None, z=None, map_type="sat", add_params=None):
    if ll and z:
        if int(z) > 18:
            z = 18
        if int(z) < 0:
            z = 0
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&z={z}&l={map_type}"
    else:
        map_request = f"http://static-maps.yandex.ru/1.x/?l={map_type}"
    if add_params:
        map_request += "&" + add_params
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        return
    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)


def show_map(ll=None, z=None, map_type="map", add_params=None):
    def change_map(new_map_type):
        nonlocal map_type
        nonlocal screen
        map_type = new_map_type
        screen.fill((0, 0, 0))
        generate_img(ll=ll, z=z, map_type=map_type, add_params=add_params)
        screen.blit(pygame.image.load('map.png'), (0, 0))
    z = int(z)
    generate_img(ll=ll, z=z, map_type=map_type, add_params=add_params)
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load('map.png'), (0, 0))

    all_sprites = pygame.sprite.Group()
    radios = URadioButtons(screen, (0, 0), all_sprites)
    radios.add_button('map', lambda: change_map('map'))
    radios.add_button('sat', lambda: change_map('sat'))
    radios.add_button('skl', lambda: change_map('skl'))

    pygame.display.flip()
    running = True
    mouse_sprite = SpriteMouseLocation()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    if int(z) - 1 > 0:
                        z = str(int(z) - 1)
                    generate_img(ll=ll, z=z, map_type=map_type, add_params=add_params)
                if event.key == pygame.K_PAGEDOWN:
                    if int(z) < 18:
                        z = str(int(z) + 1)
                    generate_img(ll=ll, z=z, map_type=map_type, add_params=add_params)
                if event.key == pygame.K_UP:
                    long, lat = (float(i) for i in ll.split(','))
                    lat = lat + 0.5
                    ll = f'{long},{lat}'
                    generate_img(ll=ll, z=z, map_type=map_type, add_params=add_params)
                if event.key == pygame.K_DOWN:
                    long, lat = (float(i) for i in ll.split(','))
                    lat = lat - 0.5
                    ll = f'{long},{lat}'
                    generate_img(ll=ll, z=z, map_type=map_type, add_params=add_params)
                if event.key == pygame.K_RIGHT:
                    long, lat = (float(i) for i in ll.split(','))
                    long = long + 0.5
                    ll = f'{long},{lat}'
                    generate_img(ll=ll, z=z, map_type=map_type, add_params=add_params)
                if event.key == pygame.K_LEFT:
                    long, lat = (float(i) for i in ll.split(','))
                    long = long - 0.5
                    ll = f'{long},{lat}'
                    generate_img(ll=ll, z=z, map_type=map_type, add_params=add_params)
                screen.fill((0, 0, 0))
                screen.blit(load_image('map.png'), (0, 0))
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_sprite.rect.x, mouse_sprite.rect.y = pygame.mouse.get_pos()
                for i in all_sprites:
                    i.click_check(mouse_sprite)
        for i in all_sprites:
            i.draw()
        pygame.display.flip()

    pygame.quit()
    os.remove('map.png')


if __name__ == '__main__':
    main()
