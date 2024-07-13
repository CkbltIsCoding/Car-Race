import sys

import pygame
from pygame.font import Font
from pygame.locals import *
from pygame.math import Vector2
from pygame.surface import Surface
from pygame.time import Clock

from car import Car


class App:
    def __init__(self):
        self.screen_size = self.screen_width, self.screen_height = 1920, 1080
        self.screen: Surface | None = None

        self.running = True
        self.debug_mode = True

        self.camera_pos = Vector2(120, 0)
        self.finish_flag_pos = Vector2(120, 0)
        self.checkpoints_pos = ((99.4694, 505.304),
                                (-829.933, 491.377),
                                (-1355.96, 646.198),
                                (-1204.36, 1258.16),
                                (-719.489, 1246.05),
                                (-503.975, 1032.64),
                                (-102.776, 1046.57),
                                (340.539, 1079.28),
                                (800.983, 1404.48),
                                (1328.09, 1102.1),
                                (1314.64, 691.101),
                                (671.056, 249.145),
                                (1151.34, -21.1044),
                                (1826.04, -195.074),
                                (1264.6, -881.13),
                                (-120.972, -1450.15),
                                (-878.867, -1184.43),
                                (-1850.7, -293.919),
                                (-1409.28, -94.5578),
                                (-508.358, -412.136),
                                (97.9214, -487.338))
        self.checkpoints_state = [False for _ in range(21)]
        self.lap = 1

        self.car: Car | None = None
        self.image_road: Surface | None = None
        self.image_minimap: Surface | None = None

        self.font_debug: Font | None = None
        self.font_lap: Font | None = None

        self.FPS = 60

        self.clock: Clock | None = None

    def on_init(self):
        pygame.init()

        self.screen = pygame.display.set_mode(self.screen_size, FULLSCREEN | HWSURFACE)
        pygame.display.set_caption('Race')

        self.car = Car(self, self.finish_flag_pos.copy(), 90) # 车朝上
        self.image_road = pygame.image.load('image/road.svg').convert_alpha()
        self.image_road = pygame.transform.scale_by(self.image_road, 10)
        self.image_minimap = pygame.image.load('image/minimap.svg').convert_alpha()
        self.image_minimap = pygame.transform.scale_by(self.image_minimap, 0.5)
        self.image_minimap.set_alpha(127)

        self.font_debug = pygame.font.SysFont('Microsoft YaHei', 16)
        self.font_lap = pygame.font.SysFont('Microsoft YaHei', 48)

        self.clock = Clock()

        return True

    def on_execute(self):
        if not self.on_init():
            self.running = False

        while self.running:
            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop()
            self.on_render()

            self.clock.tick(self.FPS)

        self.on_cleanup()

    def on_event(self, event):
        if event.type == QUIT:
            self.running = False
        if event.type == KEYDOWN:
            if event.dict['key'] == K_SPACE and self.debug_mode:
                print(self.car.pos)

    def on_loop(self):
        key_pressed = pygame.key.get_pressed()
        self.car.update(forward=key_pressed[K_w],
                        backward=key_pressed[K_s],
                        turn_left=key_pressed[K_a],
                        turn_right=key_pressed[K_d])

        # 检测检查点
        for index in range(len(self.checkpoints_pos)):
            pos = self.checkpoints_pos[index]
            if self.car.pos.distance_to(pos) <= 300:
                self.checkpoints_state[index] = True

        # 检测终点
        if self.car.pos.distance_to(self.finish_flag_pos + Vector2(0, 200)) <= 300:
            if self.checkpoints_state.count(False) <= 1:
                self.lap += 1
                self.checkpoints_state = [False for _ in range(21)] # 将检查点状态清零

        # 相机
        self.camera_pos += (self.car.pos - self.camera_pos) / 2 # 非线性移动到车

    def on_render(self):
        self.screen.fill('#000000')

        self.render_road()
        self.render_finish_flag()
        self.car.render()

        self.render_minimap()

        text_lap = self.font_lap.render(f'Lap: {self.lap}', True, '#ffffff')
        self.screen.blit(text_lap, text_lap.get_rect(top=10, centerx=self.screen_width / 2))

        # 调试模式
        if self.debug_mode:
            self.render_checkpoints()
            text_debug = self.font_debug.render(
                f'FPS: {round(self.clock.get_fps(), 2)} Car{tuple(round(self.car.pos, 2))}',
                True,
                '#ffffff')
            self.screen.blit(text_debug, (0, 0))

        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()
        sys.exit()

    def render_road(self):
        pos = self.game_pos2screen_pos(Vector2(0, 0))
        self.screen.blit(self.image_road, self.image_road.get_rect(center=pos))

    def render_finish_flag(self):
        pos = self.game_pos2screen_pos(self.finish_flag_pos)
        for y in range(2):
            for x in range(7):
                color = '#ffffff' if (x + y) % 2 == 0 else '#000000'
                pygame.draw.rect(self.screen, color, (pos.x - x * 50 + 135, pos.y - y * 50, 50, 50))

    def render_checkpoints(self):
        for index in range(len(self.checkpoints_pos)):
            checkpoint_pos = self.checkpoints_pos[index]
            pos = self.game_pos2screen_pos(checkpoint_pos)

            color = '#000000' if self.checkpoints_state[index] else '#ffffff' # 检测检查点状态

            pygame.draw.circle(self.screen, color, pos, 10)

    def render_minimap(self):
        # 渲染小地图
        minimap_pos = Vector2(self.screen_width - 50, 50)
        self.screen.blit(self.image_minimap, self.image_minimap.get_rect(topright=minimap_pos))

        # 渲染小地图上的车
        pos = self.car.pos / 10 * 0.5 # 为什么? 请参照on_init里的image_road和image_minimap的赋值语句.
        pos.y *= -1
        pos += minimap_pos
        pygame.draw.circle(self.screen, '#ffffff', self.image_minimap.get_rect(topright=pos).center, 10)

    # 将游戏中的坐标转换为屏幕上的坐标
    def game_pos2screen_pos(self, game_pos: Vector2):
        screen_pos = game_pos - self.camera_pos # 相机影响
        screen_pos.y *= -1 # 原: 正方向朝上 现: 正方向朝下
        screen_pos += (self.screen_width / 2, self.screen_height / 2) # 居中
        return screen_pos


if __name__ == '__main__':
    app = App()
    app.on_execute()
