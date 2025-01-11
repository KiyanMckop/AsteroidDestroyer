import pygame


class Spaceship:
    def __init__(self):
        # Load spaceship image and transform it
        self.original_image = pygame.image.load("images/spaceship.jpg").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (50, 40))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(400, 950))

        # Initialize attributes for movement and shooting
        self.shield = 0
        self.speed = 5
        self.power = 0
        self.last_shot_time = 0
        self.shoot_delay = 500  # Delay in milliseconds

        # Load shooting sound
        self.shoot_sound = pygame.mixer.Sound("audio/laser-45816.mp3")
        pygame.mixer.Sound.set_volume(self.shoot_sound, 0.4)
        self.shoot_sound.play()


    def move(self, dx):
        self.rect.x += dx
        self.rect.clamp_ip(pygame.Rect(0, 0, 800, 1000))

    def can_shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shoot_delay:
            self.last_shot_time = current_time
            self.shoot_sound.play()  # Play shooting sound when shooting
            return True
        return False


    def draw(self, window):
        window.blit(self.image, self.rect)

    def change_image(self, imagePath):
        self.image = pygame.image.load(imagePath).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=self.rect.center)  # Keep position consistent
