import pygame
import pygame.transform as pt
from math import degrees
import pymunk
from settings import settings


class Fruit:
    def __init__(self, type, imgs, space, pos):
        self.type = type
        self.img = imgs[self.type]
        self.position = pos
        self.body = pymunk.Body()
        self.body.position = self.position
        self.shape = pymunk.Circle(self.body, self.img.get_size()[0] / 2)
        self.shape.mass = 10
        self.shape.elasticity = 0.9
        self.shape.friction = 0.4
        space.add(self.body, self.shape)

    def draw(self, screen: pygame.Surface):
        img = pt.rotate(self.img, -degrees(self.body.angle))
        rect: pygame.Rect = img.get_rect()
        rect.x, rect.y = (n - m / 2 for n, m in zip(self.body.position, img.get_size()))
        screen.blit(img, rect)
