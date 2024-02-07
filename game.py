import pygame
import pymunk
import pymunk.pygame_util
from sys import exit
from load_img import ImgLoader
from fruit import Fruit
from random import randint
from consts import *
import logging


class GameSpace(pymunk.Space):
    def init(self):
        super().__init__()

    def create_boundaries(self, screen_width, screen_height, floor_height, elasticity, friction):
        rects = [
            ((screen_width / 2, screen_height - floor_height / 2), (screen_width, floor_height)),
            ((-10, screen_height / 2), (20, screen_height)),
            ((screen_width + 10, screen_height / 2), (20, screen_height))
        ]

        for pos, size in rects:
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = pos
            shape = pymunk.Poly.create_box(body, size)
            shape.elasticity = elasticity  # 设置弹性
            shape.friction = friction  # 设置摩擦
            shape.collision_type = COLLISION_TYPE_FLOOR
            self.add(body, shape)

    def create_circle(self, radius, mass, pos: tuple[float, float], elasticity=0.9, friction=0.5,
                      collision_type=COLLISION_TYPE_FRUIT) -> pymunk.Shape:
        body = pymunk.Body()
        body.position = pos
        shape = pymunk.Circle(body, radius)
        shape.mass = mass
        shape.color = 255, 0, 0, 100
        shape.elasticity = elasticity
        shape.friction = friction
        shape.collision_type = collision_type
        self.add(body, shape)
        return shape


class Game:
    def __init__(self, settings):
        self.settings = settings

        # 初始化pygame窗口
        pygame.init()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        # 初始化计时器
        self.clock = pygame.time.Clock()

        # 初始化pymunk空间
        self.space = GameSpace()
        self.space.gravity = 0, 981
        self.space.add_collision_handler(COLLISION_TYPE_FRUIT, COLLISION_TYPE_FRUIT).post_solve = \
            self.post_collision_fruit_fruit
        self.space.create_boundaries(
            self.settings.screen_width, self.settings.screen_height, self.settings.floor_height,
            self.settings.boundary_elasticity, self.settings.boundary_friction)

        # 初始化图像
        self.fruit_imgs = ImgLoader()
        self.fruit_imgs.load(settings.fruit_imgs, settings.img_path, self.settings.fruit_size)
        self.fruits = []

        self.floor = pygame.transform.scale(
            pygame.image.load(self.settings.img_path + self.settings.floor_img),
            (self.settings.screen_width, self.settings.floor_height)
        )
        self.floor_rect = self.floor.get_rect()
        self.floor_rect.x = 0
        self.floor_rect.bottom = self.screen.get_rect().bottom

        self.line = pygame.transform.scale(
            pygame.image.load(self.settings.img_path + self.settings.line_img),
            (self.settings.screen_width, self.settings.line_size)
        )
        self.line_rect = self.line.get_rect()
        self.line_rect.x = 0
        self.line_rect.y = self.settings.top_blank_height

        self.id = 0
        self.next_type = 0
        self.set_fruit_preview()

    def main_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # 退出
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.fruits.append(
                        Fruit(self.next_type, self.fruit_imgs.imgs, self.space,
                              (pygame.mouse.get_pos()[0], self.settings.top_blank_height / 2)
                              )
                    )
                    self.next_type = self.get_next_type()
                    self.set_fruit_preview()

            self.fruit_preview_rect.centerx = pygame.mouse.get_pos()[0]
            self.draw()
            self.space.step(1 / self.settings.fps)
            self.clock.tick(self.settings.fps)

    def draw(self):
        self.screen.fill("white")
        for fruit in self.fruits:
            fruit.draw(self.screen)
        self.screen.blit(self.floor, self.floor_rect)
        self.screen.blit(self.line, self.line_rect)
        self.screen.blit(self.fruit_preview, self.fruit_preview_rect)
        pygame.display.update()

    def get_next_type(self):
        self.id += 1
        if self.id < 4:
            return 0
        else:
            return randint(0, 3)

    def set_fruit_preview(self):
        self.fruit_preview = self.fruit_imgs.imgs[self.next_type]
        self.fruit_preview_rect = self.fruit_preview.get_rect()
        self.fruit_preview_rect.centery = self.settings.top_blank_height / 2

    def post_collision_fruit_fruit(self, arbiter: pymunk.Arbiter, space, data):
        if arbiter.shapes[0].wrapper.type == arbiter.shapes[1].wrapper.type:
            logging.info(f"两类型为{arbiter.shapes[0].wrapper.type}的水果碰撞。")
            pos = tuple(
                (n + m) / 2 for n, m in zip(arbiter.shapes[0].body.position, arbiter.shapes[1].body.position))
            type = arbiter.shapes[1].wrapper.type + 1
            try:
                self.fruits.remove(arbiter.shapes[0].wrapper)
            except ValueError as e:
                logging.error(f"{repr(e)}:试图在self.fruits中删除{arbiter.shapes[0].wrapper},但没有")
            try:
                self.fruits.remove(arbiter.shapes[1].wrapper)
            except ValueError as e:
                logging.error(f"{repr(e)}:试图在self.fruits中删除{arbiter.shapes[0].wrapper},但没有")
            self.space.remove(arbiter.shapes[0], arbiter.shapes[1])
            self.fruits.append(Fruit(type, self.fruit_imgs.imgs, self.space, pos))
            return
