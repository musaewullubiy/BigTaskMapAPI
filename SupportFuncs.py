import pygame
import os
import sys


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
