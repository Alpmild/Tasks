import os
import sys

import pygame as pg
import requests

map_request = "http://static-maps.yandex.ru/1.x/"
params = {'ll': '133.377150,-26.974007',
          'spn': '13.0,13.0',
          'l': 'map'}
map_file = "map.png"


class Map(pg.sprite.Sprite):
    def __init__(self, image: pg.Surface):
        super(Map, self).__init__()
        self.image = image
        self.rect = pg.Rect(0, 0, *image.get_size())


def load_image(params_: dict) -> pg.Surface:
    response = requests.get(map_request, params=params_)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    with open(map_file, "wb") as file:
        file.write(response.content)

    image = pg.image.load(map_file)
    return image


def set_params(params_: dict, value: float):
    spn_ = float(params_['spn'].split(',')[0])
    if 1 <= spn_ + value <= 25:
        params_['spn'] = ','.join([str(spn_ + value)] * 2)
    return params_


if __name__ == '__main__':
    chart_group = pg.sprite.Group(Map(load_image(params)))

    pg.init()
    screen = pg.display.set_mode((600, 450))
    pg.display.flip()

    while 1:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                os.remove(map_file)
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_PAGEUP:
                    params = set_params(params, 0.5)
                    chart_group = pg.sprite.Group(Map(load_image(params)))

                if event.key == pg.K_PAGEDOWN:
                    params = set_params(params, -0.5)
                    chart_group = pg.sprite.Group(Map(load_image(params)))

        pg.display.flip()
        screen.fill((255, 255, 255))
        chart_group.draw(screen)

