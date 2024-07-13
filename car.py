import math

import pygame
from pygame.locals import *
from pygame.math import Vector2


def deg2rad(deg):
    return deg / 180 * math.pi


class Car(pygame.sprite.Sprite):
    def __init__(self, app, pos: Vector2, angle: float):
        super().__init__()
        self.o_image = pygame.image.load('image/car.svg').convert_alpha()
        self.image = self.o_image.copy()
        self.rect = self.image.get_rect()
        self.pos = pos
        self.v_pos = Vector2()
        self.angle = angle
        self.v_angle = 0.0
        self.app = app

    def update(self, *args, **kwargs):
        self.v_pos *= 0.9
        self.v_angle *= 0.8

        if kwargs['forward']:
            self.v_pos += Vector2(math.cos(deg2rad(self.angle)), math.sin(deg2rad(self.angle)))
        if kwargs['backward']:
            self.v_pos -= Vector2(math.cos(deg2rad(self.angle)), math.sin(deg2rad(self.angle)))
        if kwargs['turn_left']:
            self.v_angle += 1
        if kwargs['turn_right']:
            self.v_angle -= 1

        self.pos += self.v_pos
        self.angle += self.v_angle

    def render(self):
        self.image = pygame.transform.rotate(self.o_image, self.angle)

        pos = self.pos - self.app.camera_pos
        pos.y *= -1
        pos += (self.app.screen_width / 2, self.app.screen_height / 2)
        self.rect = self.image.get_rect(center=pos)

        self.app.screen.blit(self.image, self.rect)

