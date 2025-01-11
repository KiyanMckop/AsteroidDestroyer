import pygame

class Bullet:
    def __init__(self, x, y, direction=0):
        # Use the passed direction
        self.direction = direction
        self.image = pygame.Surface((5, 10), pygame.SRCALPHA)
        self.original_image = pygame.image.load("images/bullet.jpg").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (10, 20))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10

    def move(self):
        self.rect.y -= self.speed
        self.rect.x += self.direction


    def draw(self, window):
        window.blit(self.image, self.rect)
