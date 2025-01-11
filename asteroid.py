import pygame
import random
import math

class Asteroid:
    def __init__(self):

        self.asteroid_type = random.randint(1, 4)
        self.original_image = pygame.image.load("images/asteroid_" + str(self.asteroid_type) + ".jpg").convert_alpha()

        self.asteroid_size = random.randint(20, 120)
        self.asteroid_rotation = random.randint(0, 180)
        self.original_image = pygame.transform.scale(self.original_image, (self.asteroid_size, self.asteroid_size))
        self.original_image = pygame.transform.rotate(self.original_image, self.asteroid_rotation)

        #asteroid health based on size
        self.health = math.ceil(self.asteroid_size / 30)

        self.image = self.original_image
        self.rect = self.image.get_rect(center=(random.randint(0, 800), 0))

        self.vertical_speed = random.randint(2, 3)

        # Load asteroid hit sound once
        try:
            self.asteroid_hit = pygame.mixer.Sound("audio/asteroid_hit.wav")
            self.asteroid_hit.set_volume(0.5)
        except pygame.error as e:
            print(f"Error loading asteroid sound: {e}")
            self.asteroid_hit = None  # Placeholder for when sound fails to load




    def move(self):
        self.rect.y += self.vertical_speed


    def draw(self, window):
        window.blit(self.image, self.rect)

    def create_debris(self):
        """Create smaller debris when destroyed."""
        debris_list = []
        for _ in range(3):
            debris = Debris(self.rect.centerx, self.rect.centery, 20, 20, self.asteroid_type)
            debris_list.append(debris)
        return debris_list

    def change_image(self, imagePath):
        # Load the new image
        new_image = pygame.image.load("images/asteroid_" + str(self.asteroid_type) + imagePath).convert_alpha()
        new_image = pygame.transform.rotate(new_image, self.asteroid_rotation)
        self.image = pygame.transform.scale(new_image, (self.asteroid_size + 10, self.asteroid_size + 10))
        self.original_image = self.image
        self.rect = self.image.get_rect(center=self.rect.center)

        # play hit sound
        self.asteroid_hit.play()



class Debris:
    def __init__(self, x, y, sizeX, sizeY, asteroidType):
        self.asteroidType = asteroidType
        self.original_image = pygame.image.load("images/asteroid_" + str(self.asteroidType) + "_debris_" + str(random.randint(1, 3)) + ".jpg").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (sizeX, sizeY))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))

        # Randomize horizontal and vertical speeds
        self.horizontal_speed = random.randint(1, 3) * random.choice([-1, 1])  # Move left or right
        self.vertical_speed = random.randint(1, 2) * random.choice([-1, 1])  # Move downwards

    def move(self):
        self.rect.x += self.horizontal_speed  # Move horizontally
        self.rect.y += self.vertical_speed  # Move vertically

    def draw(self, window):
        window.blit(self.image, self.rect)

    def create_debris(self):
        # create smaller debris when destroyed
        debris_list = []
        for _ in range(3):
            debris = Debris(self.rect.centerx, self.rect.centery, 10, 10, self.asteroidType)
            debris_list.append(debris)
        return debris_list
