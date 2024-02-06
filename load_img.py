import pygame


class ImgLoader:
    def load(self, file_names: list, path):
        self.imgs = []
        for file in file_names:
            self.imgs.append(pygame.image.load(path + file))
