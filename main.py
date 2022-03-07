import pygame
import requests
import sys
import os
from geocoder import get_coordinates, get_address, get_mail
from UTINGAME import ULabel, ULineEdit, URadioButtons, UButton
from SupportFuncs import load_image, SpriteMouseLocation


def main():
    # coords = input('Введите координаты (через запятую):\n')
    # z = input('Введите маштаб (18 > x > 0):\n')
    coords, z = '30,30', '17'
    mapapp = MapApp(ll=coords, z=z)
    mapapp.mainloop()


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


class MapApp:
    def __init__(self, ll=None, z=None, map_type="map", add_params=None):
        self.ll = ll
        self.z = int(z)
        self.map_type = map_type
        self.add_params = add_params
        pygame.init()
        self.screen = pygame.display.set_mode((600, 450))

        self.all_sprites = pygame.sprite.Group()

        self.radios = URadioButtons(self.screen, (400, 0), self.all_sprites)
        self.radios.add_button('map', lambda: self.change_map_type('map'))
        self.radios.add_button('sat', lambda: self.change_map_type('sat'))
        self.radios.add_button('skl', lambda: self.change_map_type('skl'))
        self.line_edit = ULineEdit(self.screen, (10, 0), self.all_sprites)
        self.label_address = ULabel(self.screen, (10, 60), self.all_sprites, '', height=30, font_size=15)
        self.label_mail = ULabel(self.screen, (10, 100), self.all_sprites, '', height=30, font_size=15)
        self.button1 = UButton(self.screen, (220, 0), self.all_sprites, 'Искать',
                               lambda: self.search_map(self.line_edit.get_text(), self.label_address, self.label_mail))
        self.button2 = UButton(self.screen, (291, 0), self.all_sprites, 'Сброс',
                               lambda: self.reset_mark(self.line_edit, self.label_address, self.label_mail),
                               image_name='ui_images/ButtonRed.png')
        self.button3 = UButton(self.screen, (10, 380), self.all_sprites, 'Почта',
                               lambda: (self.label_mail.off_on(), self.label_mail.draw()),
                               image_name='ui_images/ButtonRed.png')
        self.mouse_sprite = SpriteMouseLocation()

        generate_img(ll=self.ll, z=self.z, map_type=self.map_type, add_params=self.add_params)

        self.running = True

    def change_map_type(self, new_map_type):
        self.map_type = new_map_type
        self.screen.fill((0, 0, 0))
        generate_img(ll=self.ll, z=self.z, map_type=self.map_type, add_params=self.add_params)

    def search_map(self, text_to_search, label1, label2):
        if text_to_search:
            crds = get_coordinates(text_to_search)
            if not self.add_params:
                self.add_params = 'pt='
            else:
                self.add_params += '~'
            self.add_params += f'{crds[0]},{crds[1]},pm2dbm'
            self.ll = f'{crds[0]},{crds[1]}'
            self.screen.fill((0, 0, 0))
            address = get_address(self.ll)
            mail = get_mail(address)
            label1.set_text(address)
            label2.set_text(mail)

            generate_img(ll=self.ll, z=self.z, map_type=self.map_type, add_params=self.add_params)

    def reset_mark(self, lineedit, label1, label2):
        if self.add_params:
            if '~' in self.add_params:
                self.add_params = '~'.join(self.add_params.split('~')[:-1])
            else:
                self.add_params = None

        lineedit.set_text('')
        label1.set_text('')
        label2.set_text('')

        self.screen.fill((0, 0, 0))
        generate_img(ll=self.ll, z=self.z, map_type=self.map_type, add_params=self.add_params)

    def close(self):
        self.running = False
        os.remove('map.png')
        sys.exit(0)

    def event_handler(self, event):
        if event.type == pygame.QUIT:
            self.close()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                if self.z - 1 > 0:
                    self.z = self.z - 1
                generate_img(ll=self.ll, z=self.z, map_type=self.map_type, add_params=self.add_params)
            if event.key == pygame.K_PAGEDOWN:
                if self.z < 18:
                    self.z = self.z + 1
                generate_img(ll=self.ll, z=self.z, map_type=self.map_type, add_params=self.add_params)
            if event.key == pygame.K_UP:
                long, lat = (float(i) for i in self.ll.split(','))
                lat = lat + 0.5
                self.ll = f'{long},{lat}'
                generate_img(ll=self.ll, z=self.z, map_type=self.map_type, add_params=self.add_params)
            if event.key == pygame.K_DOWN:
                long, lat = (float(i) for i in self.ll.split(','))
                lat = lat - 0.5
                self.ll = f'{long},{lat}'
                generate_img(ll=self.ll, z=self.z, map_type=self.map_type, add_params=self.add_params)
            if event.key == pygame.K_RIGHT:
                long, lat = (float(i) for i in self.ll.split(','))
                long = long + 0.5
                self.ll = f'{long},{lat}'
                generate_img(ll=self.ll, z=self.z, map_type=self.map_type, add_params=self.add_params)
            if event.key == pygame.K_LEFT:
                long, lat = (float(i) for i in self.ll.split(','))
                long = long - 0.5
                self.ll = f'{long},{lat}'
                generate_img(ll=self.ll, z=self.z, map_type=self.map_type, add_params=self.add_params)
            self.screen.fill((0, 0, 0))
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_sprite.rect.x, self.mouse_sprite.rect.y = pygame.mouse.get_pos()
            self.radios.click_check(self.mouse_sprite)
            self.button1.click_check(self.mouse_sprite)
            self.button2.click_check(self.mouse_sprite)
            self.button3.click_check(self.mouse_sprite)
        if event.type == pygame.KEYDOWN:
            self.mouse_sprite.rect.x, self.mouse_sprite.rect.y = pygame.mouse.get_pos()
            self.line_edit.hover_check(self.mouse_sprite, event)

    def mainloop(self):
        while self.running:
            self.screen.blit(pygame.image.load('map.png'), (0, 0))
            for event in pygame.event.get():
                self.event_handler(event)

            self.radios.draw()
            self.button1.draw()
            self.button2.draw()
            self.button3.draw()
            self.line_edit.draw()
            self.label_address.draw()
            self.label_mail.draw()
            pygame.display.flip()

        pygame.quit()
        os.remove('map.png')


if __name__ == '__main__':
    main()
