import pygame
import pygame.transform as pt
from math import degrees
import pymunk
from settings import settings


class Fruit:
    def __init__(self,
                 type: int,
                 imgs: list[pygame.Surface | pygame.SurfaceType],
                 space,
                 pos: tuple[float, float]
    ):
        self.type = type
        self.img = imgs[self.type]
        self.position = pos
        self.shape: pymunk.Shape = space.create_circle(
            self.img.get_size()[0] / 2, 10, self.position, settings.fruit_elasticity, settings.fruit_friction)
        self.shape.wrapper = self
        self.body = self.shape.body

    def draw(self, screen: pygame.Surface):
        img = pt.rotate(self.img, -degrees(self.body.angle))
        rect: pygame.Rect = img.get_rect()
        rect.x, rect.y = (n - m / 2 for n, m in zip(self.body.position, img.get_size()))
        screen.blit(img, rect)

    def __repr__(self):
        return f"Fruit({self.type}, {self.body.position})"
