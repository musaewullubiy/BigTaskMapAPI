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
    def change_map_type(new_map_type):
        nonlocal map_type
        nonlocal screen
        map_type = new_map_type
        screen.fill((0, 0, 0))
        generate_img(ll=ll, z=z, map_type=map_type, add_params=add_params)
        screen.blit(pygame.image.load('map.png'), (0, 0))

    def search_map(text_to_search, label1, label2):
        nonlocal screen
        nonlocal add_params
        nonlocal ll
        crds = get_coordinates(text_to_search)
        if not add_params:
            add_params = 'pt='
        else:
            add_params += '~'
        add_params += f'{crds[0]},{crds[1]},pm2dbm'
        ll = f'{crds[0]},{crds[1]}'
        screen.fill((0, 0, 0))
        address = get_address(ll)
        mail = get_mail(address)
        label1.set_text(address)
        label2.set_text(mail)

        generate_img(ll=ll, z=z, map_type=map_type, add_params=add_params)
        screen.blit(pygame.image.load('map.png'), (0, 0))

    def reset_mark(lineedit, label1, label2):
        nonlocal screen
        nonlocal add_params
        if add_params:
            if '~' in add_params:
                add_params = '~'.join(add_params.split('~')[:-1])
            else:
                add_params = None

        lineedit.set_text('')
        label1.set_text('')
        label2.set_text('')

        screen.fill((0, 0, 0))
        generate_img(ll=ll, z=z, map_type=map_type, add_params=add_params)
        screen.blit(pygame.image.load('map.png'), (0, 0))

    z = int(z)
    generate_img(ll=ll, z=z, map_type=map_type, add_params=add_params)
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load('map.png'), (0, 0))

    all_sprites = pygame.sprite.Group()

    radios = URadioButtons(screen, (400, 0), all_sprites)
    radios.add_button('map', lambda: change_map_type('map'))
    radios.add_button('sat', lambda: change_map_type('sat'))
    radios.add_button('skl', lambda: change_map_type('skl'))
    line_edit = ULineEdit(screen, (10, 0), all_sprites)
    label_address = ULabel(screen, (10, 60), all_sprites, '', height=30, font_size=15)
    label_mail = ULabel(screen, (10, 100), all_sprites, '', height=30, font_size=15)
    button1 = UButton(screen, (220, 0), all_sprites, 'Искать', lambda: search_map(line_edit.get_text(), label_address, label_mail))
    button2 = UButton(screen, (291, 0), all_sprites, 'Сброс', lambda: reset_mark(line_edit, label_address, label_mail),
                      image_name='ui_images/ButtonRed.png')
    button3 = UButton(screen, (10, 380), all_sprites, 'Почта', lambda: (label_mail.off_on(), label_mail.draw()),
                      image_name='ui_images/ButtonRed.png')
    mouse_sprite = SpriteMouseLocation()

    running = True
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
                radios.click_check(mouse_sprite)
                button1.click_check(mouse_sprite)
                button2.click_check(mouse_sprite)
                button3.click_check(mouse_sprite)
            if event.type == pygame.KEYDOWN:
                mouse_sprite.rect.x, mouse_sprite.rect.y = pygame.mouse.get_pos()
                line_edit.hover_check(mouse_sprite, event)
        mouse_sprite.rect.x, mouse_sprite.rect.y = pygame.mouse.get_pos()

        radios.draw()
        button1.draw()
        button2.draw()
        button3.draw()
        line_edit.draw()
        label_address.draw()
        label_mail.draw()

        pygame.display.flip()

    pygame.quit()
    os.remove('map.png')


if __name__ == '__main__':
    main()
