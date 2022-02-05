import requests
import pygame as pg
import sys
import os

"""
Большая задача по Maps API. Часть №7
Чтобы выбирать слой, надо нажимать на кнопки 1, 2, 3
Метка удаляется при нажатии на Enter, который под Backspace :)
"""
message = "Введите название объекта: "

map_request = "http://static-maps.yandex.ru/1.x/"
map_params = {'ll': '',  # долгота и широта
              'spn': '0.02,0.02',
              'l': 'map'}
map_file = "map.png"

coors_request = "http://geocode-maps.yandex.ru/1.x/"
coors_params = {'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
                'geocode': '',
                'format': 'json'}


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


def change_spn(params_: dict, value: float):
    spn_ = float(params_['spn'].split(',')[0])
    if 1 <= spn_ + value <= 40:
        params_['spn'] = ','.join([str(spn_ + value)] * 2)


def change_coors(params_: dict, n: int, value: float):
    coors = list(map(float, params_['ll'].split(',')))
    if -80 * (2 - n) < coors[n] + value < 80 * (2 - n):
        coors[n] += value
        params_['ll'] = ','.join(map(str, coors))


def change_map(params_: dict, type_: str):
    params_['l'] = type_


if __name__ == '__main__':
    t = 1
    while t:
        coors_params['geocode'] = input(message)
        res = requests.get(coors_request, params=coors_params)

        t = 0
        try:
            map_params['ll'] = ','.join(res.json()['response']['GeoObjectCollection']['featureMember'][0]
                                        ['GeoObject']['Point']['pos'].split())
        except IndexError:
            message = "Введите корректное название объекта: "
            t = 1

    map_params['pt'] = f'{map_params["ll"]},pm2ntl'

    clock = pg.time.Clock()
    chart_group = pg.sprite.Group(Map(load_image(map_params)))

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
                    change_spn(map_params, 2.0)
                    chart_group = pg.sprite.Group(Map(load_image(map_params)))

                if event.key == pg.K_PAGEDOWN:
                    change_spn(map_params, -2.0)
                    chart_group = pg.sprite.Group(Map(load_image(map_params)))

                if event.key == pg.K_UP:
                    change_coors(map_params, 1, 5)
                    chart_group = pg.sprite.Group(Map(load_image(map_params)))

                if event.key == pg.K_DOWN:
                    change_coors(map_params, 1, -5)
                    chart_group = pg.sprite.Group(Map(load_image(map_params)))

                if event.key == pg.K_RIGHT:
                    change_coors(map_params, 0, 5)
                    chart_group = pg.sprite.Group(Map(load_image(map_params)))

                if event.key == pg.K_LEFT:
                    change_coors(map_params, 0, -5)
                    chart_group = pg.sprite.Group(Map(load_image(map_params)))

                if event.key == pg.K_1:
                    change_map(map_params, 'map')
                    chart_group = pg.sprite.Group(Map(load_image(map_params)))

                if event.key == pg.K_2:
                    change_map(map_params, 'sat')
                    chart_group = pg.sprite.Group(Map(load_image(map_params)))

                if event.key == pg.K_3:
                    change_map(map_params, 'skl')
                    chart_group = pg.sprite.Group(Map(load_image(map_params)))

                if event.key == pg.K_RETURN:
                    map_params.pop('pt')
                    chart_group = pg.sprite.Group(Map(load_image(map_params)))

        pg.display.flip()
        clock.tick(5)

        screen.fill((255, 255, 255))
        chart_group.draw(screen)
