import pygame
import random
import math
from spaceship import Spaceship
from bullet import Bullet
from asteroid import Asteroid, Debris
from enemy import Enemy, EnemyBullet
from powerup import PowerUp
from parallax import ParallaxLayer

# Initialize Pygame
pygame.init()

#this is a test
# Game window dimensions
WIDTH, HEIGHT = 800, 1000
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("Asteroid Destroyer")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
CYAN = (0, 255, 255)

# Game clock
clock = pygame.time.Clock()

#parallax effect
layer1 = ParallaxLayer("images/parallax_2.jpg", 1)     # Farther background

# Font for text
font = pygame.font.SysFont(None, 35)

# Game States
START_MENU = "start_menu"
GAME_RUNNING = "game_running"
PAUSE_MENU = "pause_menu"
SETTINGS_MENU = "settings_menu"
GAME_OVER = "game_over"

# Current game state
game_state = START_MENU

def draw_text(window, text, size, x, y, color):
    font = pygame.font.SysFont(None, size)
    label = font.render(text, True, color)
    window.blit(label, (x, y))

def start_menu():
    win.fill(BLACK)
    draw_text(win, "ASTEROID DESTROYER", 50, WIDTH // 2 - 200, HEIGHT // 2 - 100, WHITE)
    draw_text(win, "Press ENTER to Start", 35, WIDTH // 2 - 120, HEIGHT // 2, WHITE)
    draw_text(win, "Press Q to Quit", 35, WIDTH // 2 - 100, HEIGHT // 2 + 50, WHITE)
    pygame.display.update()

def pause_menu():
    win.fill(BLACK)
    draw_text(win, "Game Paused", 50, WIDTH // 2 - 120, HEIGHT // 2 - 100, WHITE)
    draw_text(win, "Press R to Resume", 35, WIDTH // 2 - 110, HEIGHT // 2, WHITE)
    draw_text(win, "Press Q to Quit", 35, WIDTH // 2 - 90, HEIGHT // 2 + 100, WHITE)
    pygame.display.update()


def game_over():
    win.fill(BLACK)
    draw_text(win, "Game Over", 50, WIDTH // 2 - 100, HEIGHT // 2 - 100, WHITE)
    draw_text(win, "Press B to go Back", 35, WIDTH // 2 - 120, HEIGHT // 2 + 50, WHITE)

    global game_state, spaceship, bullets, asteroids, debris_list, enemies, enemy_bullets, powerups, score

    game_state = START_MENU
    spaceship = Spaceship()  # Reinitialize the spaceship
    bullets = []  # Clear all bullets
    asteroids = []  # Clear all asteroids
    debris_list = []  # Clear all debris
    enemies = []  # Clear all enemies
    enemy_bullets = []  # Clear all enemy bullets
    powerups = []  # Clear all power-ups
    score = 0  # Reset the score

    pygame.display.update()


def game():
    spaceship = Spaceship()
    bullets = []
    asteroids = []
    debris_list = []
    enemies = []
    enemy_bullets = []
    powerups = []
    score = 0

    # Progression system variables
    difficulty_level = 1
    frames_since_start = 0
    base_asteroid_spawn_rate = 200  # Higher number = slower spawns
    base_enemy_spawn_rate = 500
    base_powerup_spawn_rate = 1000

    def calculate_spawn_rates():
        nonlocal difficulty_level
        # Increase difficulty every 20 points
        new_level = 1 + (score // 10)
        if new_level != difficulty_level:
            difficulty_level = new_level

        # Calculate spawn rates based on difficulty
        asteroid_rate = max(50, base_asteroid_spawn_rate - (difficulty_level * 15))
        enemy_rate = max(100, base_enemy_spawn_rate - (difficulty_level * 25))
        powerup_rate = max(500, base_powerup_spawn_rate - (difficulty_level * 20))

        return asteroid_rate, enemy_rate, powerup_rate

    def spawn_enemies():
        # After level 3, sometimes spawn multiple enemies
        if difficulty_level >= 3 and random.random() < 0.3:
            num_enemies = min(3, difficulty_level - 1)
            spread = 100  # Horizontal spread between enemies

            for i in range(num_enemies):
                enemy = Enemy()
                enemy.health = min(3, 1 + (difficulty_level // 4))  # Increase enemy health with difficulty
                enemies.append(enemy)
        else:
            enemy = Enemy()
            enemy.health = min(3, 1 + (difficulty_level // 4))
            enemies.append(enemy)

    def spawn_asteroids():
        # After level 2, sometimes spawn asteroid clusters
        if difficulty_level >= 2 and random.random() < 0.4:
            num_asteroids = min(3, 1 + (difficulty_level // 2))

            for i in range(num_asteroids):
                asteroid = Asteroid()
                asteroids.append(asteroid)
        else:
            asteroid = Asteroid()
            asteroids.append(asteroid)

    global game_state
    frame_count = 0  # Use frame count to manage random spawns
    while game_state == GAME_RUNNING:
        clock.tick(60)
        win.fill(BLACK)

        # Update and draw the parallax layer
        layer1.update()
        layer1.draw(win)

        # Calculate current spawn rates based on difficulty
        asteroid_spawn_rate, enemy_spawn_rate, powerup_spawn_rate = calculate_spawn_rates()

        # Spawn logic using frame count and difficulty-based rates
        if frames_since_start % asteroid_spawn_rate == 0:
            spawn_asteroids()

        if frames_since_start >= enemy_spawn_rate:  # Don't spawn enemies immediately
            if frames_since_start % enemy_spawn_rate == 0:
                spawn_enemies()

        if frames_since_start % powerup_spawn_rate == 0:
            # Increased chance of shield powerups at higher difficulties
            if random.random() < min(0.7, 0.3 + (difficulty_level * 0.05)):
                powerup = PowerUp()
                powerup.type = "shield"
                powerups.append(powerup)
            else:
                powerups.append(PowerUp())

        frames_since_start += 1

        # Display additional information
        level_text = font.render(f"Level: {difficulty_level}", True, WHITE)
        win.blit(level_text, (WIDTH - 150, 10))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = START_MENU
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_state = PAUSE_MENU

        # Spaceship controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            spaceship.move(-spaceship.speed)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            spaceship.move(spaceship.speed)

        # Shooting with direction
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and spaceship.can_shoot():
            if spaceship.power == 1:
                bullets.append(Bullet(spaceship.rect.left + 20, spaceship.rect.centery))
                bullets.append(Bullet(spaceship.rect.right - 20, spaceship.rect.centery))
            elif spaceship.power == 2:
                bullets.append(Bullet(spaceship.rect.left + 40, spaceship.rect.centery))
                bullets.append(Bullet(spaceship.rect.right - 40, spaceship.rect.centery))
                bullets.append(Bullet(spaceship.rect.centerx, spaceship.rect.centery))
            elif spaceship.power == 3:
                bullets.append(Bullet(spaceship.rect.left + 20, spaceship.rect.centery, -1))
                bullets.append(Bullet(spaceship.rect.right - 20, spaceship.rect.centery, +1))
                bullets.append(Bullet(spaceship.rect.left + 10, spaceship.rect.centery, -1))
                bullets.append(Bullet(spaceship.rect.right - 10, spaceship.rect.centery, +1))
                bullets.append(Bullet(spaceship.rect.centerx, spaceship.rect.centery))
            elif spaceship.power == 0:
                bullets.append(Bullet(spaceship.rect.centerx, spaceship.rect.centery))


        # Update all moving objects
        for bullet in bullets[:]:
            bullet.move()
            if (bullet.rect.top < 0 or bullet.rect.bottom > HEIGHT or
                    bullet.rect.left < 0 or bullet.rect.right > WIDTH):
                bullets.remove(bullet)

        for asteroid in asteroids[:]:
            asteroid.move()
            if asteroid.rect.colliderect(spaceship.rect) and spaceship.shield == 0:
                game_state = GAME_OVER
                break
            elif asteroid.rect.colliderect(spaceship.rect) and spaceship.shield != 0:
                spaceship.shield -= 1
                spaceship.power = 0
                debris_list.extend(asteroid.create_debris())  # Create debris
                asteroids.remove(asteroid)
                # play sound effect asteroid break
                asteroid_destroy_sound = pygame.mixer.Sound("audio/small-rock-break-194553.mp3")
                # volume based on distance
                distance_volume = (asteroid.rect.y / spaceship.rect.y)
                if distance_volume >= 0.5:
                    asteroid_destroy_sound.set_volume(0.5)
                else:
                    asteroid_destroy_sound.set_volume(distance_volume)
                asteroid_destroy_sound.play()
                if spaceship.shield == 0:
                    spaceship.change_image("images/spaceship.jpg")
            if asteroid.rect.top > HEIGHT:
                asteroids.remove(asteroid)
            else:
                for bullet in bullets[:]:
                    if asteroid.rect.colliderect(bullet.rect):
                        asteroid.health -= 1
                        if asteroid.health == 0:
                            debris_list.extend(asteroid.create_debris())  # Create debris
                            asteroids.remove(asteroid)
                            asteroid_destroy_sound = pygame.mixer.Sound("audio/small-rock-break-194553.mp3")
                            # volume based on distance
                            distance_volume = (asteroid.rect.y / spaceship.rect.y)
                            if distance_volume >= 0.5:
                                asteroid_destroy_sound.set_volume(0.5)
                            else:
                                asteroid_destroy_sound.set_volume(distance_volume)
                            asteroid_destroy_sound.play()
                            bullets.remove(bullet)
                            score += 1
                            break
                        else:
                            asteroid.change_image("_crack_" + str(asteroid.health) + ".jpg")
                            bullets.remove(bullet)
                            break


        for debris in debris_list[:]:
            debris.move()
            if (debris.rect.top < 0 or debris.rect.bottom > HEIGHT or
                    debris.rect.left < 0 or debris.rect.right > WIDTH):
                debris_list.remove(debris)
            if debris.rect.top > HEIGHT:
                debris_list.remove(debris)
            else:
                for bullet in bullets[:]:
                    if debris.rect.colliderect(bullet.rect) and len(debris_list) < 15:
                        debris_list.extend(debris.create_debris())
                        debris_list.remove(debris)
                        bullets.remove(bullet)
                        break
                    elif debris.rect.colliderect(bullet.rect) and len(debris_list) >= 15:
                        debris_list.remove(debris)
                        bullets.remove(bullet)


        for enemy in enemies[:]:
            enemy.move()
            if enemy.rect.colliderect(spaceship.rect) and spaceship.shield == 0:
                game_state = GAME_OVER
                break
            elif enemy.rect.colliderect(spaceship.rect) and spaceship.shield != 0:
                spaceship.shield -= 1
                spaceship.power = 0
                enemies.remove(enemy)
                if spaceship.shield == 0:
                    spaceship.change_image("images/spaceship.jpg")
            if random.randint(1, 100) == 1:  # Enemies shoot at random intervals
                enemy_bullets.append(enemy.shoot())
            if enemy.rect.top > HEIGHT:
                enemies.remove(enemy)
            #enemy bullet collision
            for bullet in bullets[:]:
                if enemy.rect.colliderect(bullet.rect) and enemy.health == 1:
                    enemy_death_sound = pygame.mixer.Sound("audio/windy-thud-192374.mp3")
                    # volume based on distance
                    distance_volume = (enemy.rect.y / spaceship.rect.y)
                    if distance_volume >= 0.5:
                        pygame.mixer.Sound.set_volume(enemy_death_sound, 0.5)
                    else:
                        pygame.mixer.Sound.set_volume(enemy_death_sound, distance_volume)

                    enemy_death_sound.play()
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 2
                    break
                elif enemy.rect.colliderect(bullet.rect) and enemy.health != 1:
                    enemy.health -= 1
                    enemy_hit_sound = pygame.mixer.Sound("audio/explosion.wav")
                    enemy_hit_sound.set_volume(0.3)
                    enemy_hit_sound.play()
                    enemy.hit_effect()
                    bullets.remove(bullet)

        for enemy_bullet in enemy_bullets[:]:
            enemy_bullet.move()

            # Check for collision with spaceship
            if enemy_bullet.rect.colliderect(spaceship.rect):
                # If the spaceship has no shield, game over
                if spaceship.shield == 0:
                    game_state = GAME_OVER
                    break
                else:
                    # Decrease the shield and remove the enemy bullet
                    spaceship.shield -= 1
                    enemy_bullets.remove(enemy_bullet)
                    # Optionally play sound or effects here
                    spaceship.change_image("images/spaceship_shield.jpg")  # Change image if shield is hit

            # Remove bullets that go off-screen
            if enemy_bullet.rect.top > HEIGHT:
                enemy_bullets.remove(enemy_bullet)

        for powerup in powerups[:]:
            powerup.move()
            if powerup.rect.colliderect(spaceship.rect):
                if powerup.type == "shield":
                    spaceship.shield += 1
                    spaceship.change_image("images/spaceship_shield.jpg")
                    powerup.playSoundEffect()
                    powerups.remove(powerup)
                if powerup.type == "power":
                    if spaceship.power < 3:
                        spaceship.power += 1
                    powerup.playSoundEffect()
                    powerups.remove(powerup)
            if powerup.rect.top > HEIGHT:
                powerups.remove(powerup)

        # Drawing the game elements
        spaceship.draw(win)
        for bullet in bullets:
            bullet.draw(win)
        for asteroid in asteroids:
            asteroid.draw(win)
        for debris in debris_list:
            debris.draw(win)
        for enemy in enemies:
            enemy.draw(win)
        for enemy_bullet in enemy_bullets:
            enemy_bullet.draw(win)
        for powerup in powerups:
            powerup.draw(win)

        # Display the current score
        score_text = font.render(f"Score: {score}", True, WHITE)
        win.blit(score_text, (10, 10))

        #display shield
        shield_text = font.render(f"Shield: {spaceship.shield * 100}", True, CYAN)
        win.blit(shield_text, (10, 30))


        # Update the display
        pygame.display.update()



def main():
    global game_state
    run = True
    backgroundMusic = pygame.mixer.Sound("audio/background_music.mp3")
    backgroundMusic.set_volume(0.5)
    backgroundMusic.play(1, 0, 1000)
    while run:
        if game_state == START_MENU:
            start_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Start game
                        game_state = GAME_RUNNING
                    elif event.key == pygame.K_q:  # Quit game
                        run = False

            pygame.display.update()

        elif game_state == GAME_OVER:
            game_over()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        run = False

        elif game_state == GAME_RUNNING:
            # Update and draw layers in game mode as well
            layer1.update()
            layer1.draw(win)
            game()

        elif game_state == PAUSE_MENU:
            pause_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Resume game
                        game_state = GAME_RUNNING
                    elif event.key == pygame.K_s:  # Open settings
                        game_state = SETTINGS_MENU
                    elif event.key == pygame.K_q:  # Quit game
                        run = False


    pygame.quit()


if __name__ == "__main__":
    main()

