import pygame
import random

class PowerUp:
    def __init__(self):
        self.type = random.choice(['shield', 'power'])  # Two types: shield or power
        self.image = pygame.Surface((30, 30))
        self.collect_sound = pygame.mixer.Sound("audio/power-up-type-1.mp3")
        if self.type == 'shield':
            self.original_image = pygame.image.load("images/shield.jpg").convert_alpha()
            self.original_image = pygame.transform.scale(self.original_image, (35, 35))
            self.image = self.original_image
        else:
            self.original_image = pygame.image.load("images/powerup.jpg").convert_alpha()
            self.original_image = pygame.transform.scale(self.original_image, (35, 35))
            self.image = self.original_image

        self.rect = self.image.get_rect(center=(random.randint(0, 800), 0))
        self.speed = random.randint(3, 5)

    def move(self):
        self.rect.y += self.speed

    def draw(self, window):
        window.blit(self.image, self.rect)

    def playSoundEffect(self):
        self.collect_sound.play()
