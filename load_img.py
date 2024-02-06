import pygame


class ImgLoader:
    def load(self, file_names: list, path, size):
        self.imgs = []
        for file in file_names:
            img = pygame.image.load(path + file)
            self.imgs.append(pygame.transform.scale(img, tuple(n * size for n in img.get_size())))
