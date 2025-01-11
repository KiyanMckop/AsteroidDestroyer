import pygame

class ParallaxLayer:
    def __init__(self, image_path, scroll_speed):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.scroll_speed = scroll_speed
        self.y1 = 0
        self.y2 = -self.image.get_height()  # Start the second image right above the first

    def update(self):
        # Move each image down by scroll_speed
        self.y1 += self.scroll_speed
        self.y2 += self.scroll_speed

        # Reset positions to create a seamless scroll effect
        if self.y1 >= self.image.get_height():
            self.y1 = self.y2 - self.image.get_height()
        if self.y2 >= self.image.get_height():
            self.y2 = self.y1 - self.image.get_height()

    def draw(self, window):
        window.blit(self.image, (0, self.y1))
        window.blit(self.image, (0, self.y2))
