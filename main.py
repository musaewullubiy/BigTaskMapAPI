import pygame
import requests
import sys
import os


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


def show_map(ll=None, z=None, map_type="sat", add_params=None):
    z = int(z)
    generate_img(ll=ll, z=z, map_type=map_type, add_params=add_params)
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load('map.png'), (0, 0))
    pygame.display.flip()
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
        screen.blit(pygame.image.load('map.png'), (0, 0))
        pygame.display.flip()

    pygame.quit()
    os.remove('map.png')


if __name__ == '__main__':
    main()
