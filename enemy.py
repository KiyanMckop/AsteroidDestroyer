import pygame
import random

class Enemy:
    def __init__(self):
        self.health = 3
        self.original_image = pygame.image.load("images/enemy.jpg").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (40, 40))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(random.randint(40, 760), 0))
        self.speed = random.randint(1, 2)
        self.direction = random.choice([-1, 1])  # Move left or right

        # Load asteroid hit sound once
        try:
            self.shoot_sound = pygame.mixer.Sound("audio/spaceship_shoot.wav")
            self.shoot_sound.set_volume(0.5)
        except pygame.error as e:
            print(f"Error loading asteroid sound: {e}")
            self.shoot_sound = None  # Placeholder for when sound fails to load



    def move(self):
        self.rect.x += self.direction * self.speed
        self.rect.y += self.speed

        # Change direction when hitting screen edges
        if self.rect.left <= 0 or self.rect.right >= 800:
            self.direction *= -1

    def draw(self, window):
        window.blit(self.image, self.rect)

    def shoot(self):
        """Enemy shoots a bullet downward."""
        self.shoot_sound.play()
        return EnemyBullet(self.rect.centerx, self.rect.bottom)

    def hit_effect(self):
        self.rect.x += 2
        self.rect.x -= 2


    def change_image(self, imagePath):
        self.image = pygame.image.load(imagePath).convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(center=self.rect.center)



class EnemyBullet:
    def __init__(self, x, y):
        self.image = pygame.Surface((2, 5))
        self.original_image = pygame.image.load("images/enemy_bullet.jpg").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (10, 20))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

    def move(self):
        self.rect.y += self.speed

    def draw(self, window):
        window.blit(self.image, self.rect)

