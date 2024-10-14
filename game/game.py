# Game made with AI assistance by:
# Miguel Sosa
# Marcos Sanchez

import random
import sys
import os
import pygame
import math

# Initialize pygame
pygame.init()

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombies Warrior")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)

# Player setup
player_size = 30
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT // 2 - player_size // 2
player_speed = 4 
player_lives = 5  

# Constants for game balance
DIFFICULTY_INCREASE_THRESHOLD = 300  # Increased from 200 to make the game easier
MAX_ENEMY_SPEED = player_speed - 2  # Reduced to make the game easier
ENEMY_SPAWN_RATE = 180  # Increased from 120 to make enemies spawn less frequently
POWER_UP_INTERVAL = 15 * 60  # Reduced from 20 seconds to 15 seconds
SHOOT_COOLDOWN = 30  # Increased from 15 to decrease shoot rate
TRAIL_DURATION = 30

# Additional setup
power_up_timer = 0
power_up_pos = None
last_shot_time = 0
player_trail = []

# Enemy setup
enemy_size = 20
enemies = []
enemy_speed = 1.5  # Reduced from 2 to make the game easier

# Big enemy setup
big_enemy_size = 40
big_enemies = []
big_enemy_speed = 1
big_enemy_health = 20
BIG_ENEMY_SPAWN_RATE = 600  # Lower rate of appearance

# Bullet setup
bullet_size = 5
bullets = []
bullet_speed = 8  # Reduced from 10 to make the game slightly more challenging

# Game variables
score = 0
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Initialize the mixer
pygame.mixer.init()

# Load and play background music
pygame.mixer.music.load('background_music.mp3')  # Make sure to replace with your actual music file
pygame.mixer.music.play(-1)  # -1 means loop indefinitely

# Set the volume (0.0 to 1.0)
pygame.mixer.music.set_volume(0.1)  # Adjust this value to decrease volume as needed


# Load sounds
current_dir = os.path.dirname(os.path.abspath(__file__))
background_music = pygame.mixer.music.load(os.path.join(current_dir, "background_music.mp3"))
game_over_sound = pygame.mixer.Sound(os.path.join(current_dir, "game_over.mp3"))
enemy_destroy_sound = pygame.mixer.Sound(os.path.join(current_dir, "zombie.mp3"))
player_hit_sound = pygame.mixer.Sound(os.path.join(current_dir, "damage.mp3"))
power_up_sound = pygame.mixer.Sound(os.path.join(current_dir, "boom.mp3"))
#shoot_sound = pygame.mixer.Sound(os.path.join(current_dir, "pew.mp3"))

# Load the jumpscare image
jumpscare_image = pygame.image.load(os.path.join(current_dir, "jumpscare.png"))
jumpscare_image = pygame.transform.scale(jumpscare_image, (WIDTH, HEIGHT))  # Scale to fit the screen

# Load background image
background_image = pygame.image.load(os.path.join(current_dir, "title_screen.png"))
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
# Load title screen image
title_screen = pygame.image.load(os.path.join(current_dir, "screen.png"))
title_screen = pygame.transform.scale(title_screen, (WIDTH, HEIGHT))

# Level variables
current_level = 1
POINTS_PER_LEVEL = 200
# Start playing background music
pygame.mixer.music.play(-1)  # -1 means loop indefinitely

def show_level_screen(level):
    screen.fill(BLACK)
    level_text = font.render(f"Level {level}", True, WHITE)
    continue_text = font.render("Press any key to continue", True, WHITE)
    screen.blit(level_text, (WIDTH//2 - level_text.get_width()//2, HEIGHT//2 - 50))
    screen.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT//2 + 50))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def increase_difficulty():
    global enemy_speed, ENEMY_SPAWN_RATE, big_enemy_speed, BIG_ENEMY_SPAWN_RATE
    enemy_speed *= 1.2
    ENEMY_SPAWN_RATE = max(20, int(ENEMY_SPAWN_RATE * 0.75))  # Increased enemy spawn rate
    big_enemy_speed *= 1.1
    BIG_ENEMY_SPAWN_RATE = max(200, int(BIG_ENEMY_SPAWN_RATE * 0.75))  # Increase big enemy spawn rate


def draw_player():
    pygame.draw.circle(screen, PURPLE, (int(player_x + player_size // 2), int(player_y + player_size // 2)), player_size // 2)

def draw_enemies():
    for enemy in enemies:
        pygame.draw.rect(screen, RED, (enemy[0], enemy[1], enemy_size, enemy_size))
    for big_enemy in big_enemies:
        pygame.draw.rect(screen, ORANGE, (big_enemy[0], big_enemy[1], big_enemy_size, big_enemy_size))

def draw_bullets():
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, (bullet[0], bullet[1], bullet_size, bullet_size))

def draw_power_up():
    if power_up_pos:
        pygame.draw.circle(screen, (0, 0, 255), power_up_pos, 10)

def draw_player_trail():
    for pos, alpha in player_trail:
        s = pygame.Surface((5, 5))
        s.set_alpha(alpha)
        s.fill(PURPLE)
        screen.blit(s, pos)

def update_player_trail():
    global player_trail
    player_trail.insert(0, ((player_x + player_size // 2, player_y + player_size // 2), 255))
    player_trail = [(pos, max(0, alpha - 255 // TRAIL_DURATION)) for pos, alpha in player_trail]
    player_trail = [item for item in player_trail if item[1] > 0]

def move_enemies():
    for enemy in enemies:
        dx = player_x - enemy[0]
        dy = player_y - enemy[1]
        dist = (dx**2 + dy**2)**0.5
        if dist != 0:
            enemy[0] += dx / dist * enemy_speed
            enemy[1] += dy / dist * enemy_speed
    for big_enemy in big_enemies:
        dx = player_x - big_enemy[0]
        dy = player_y - big_enemy[1]
        dist = (dx**2 + dy**2)**0.5
        if dist != 0:
            big_enemy[0] += dx / dist * big_enemy_speed
            big_enemy[1] += dy / dist * big_enemy_speed

def move_bullets():
    for bullet in bullets:
        bullet[0] += bullet[2] * bullet_speed
        bullet[1] += bullet[3] * bullet_speed

def check_collisions():
    global score, player_lives
    for enemy in enemies[:]:
        if (player_x < enemy[0] + enemy_size and
            player_x + player_size > enemy[0] and
            player_y < enemy[1] + enemy_size and
            player_y + player_size > enemy[1]):
            player_lives -= 1
            enemies.remove(enemy)
            player_hit_sound.play()
        for bullet in bullets[:]:
            if (bullet[0] < enemy[0] + enemy_size and
                bullet[0] + bullet_size > enemy[0] and
                bullet[1] < enemy[1] + enemy_size and
                bullet[1] + bullet_size > enemy[1]):
                score += 10
                enemies.remove(enemy)
                bullets.remove(bullet)
                enemy_destroy_sound.play()
                break
    
    for big_enemy in big_enemies[:]:
        if (player_x < big_enemy[0] + big_enemy_size and
            player_x + player_size > big_enemy[0] and
            player_y < big_enemy[1] + big_enemy_size and
            player_y + player_size > big_enemy[1]):
            player_lives -= 2
            big_enemies.remove(big_enemy)
            player_hit_sound.play()
        for bullet in bullets[:]:
            if (bullet[0] < big_enemy[0] + big_enemy_size and
                bullet[0] + bullet_size > big_enemy[0] and
                bullet[1] < big_enemy[1] + big_enemy_size and
                bullet[1] + bullet_size > big_enemy[1]):
                big_enemy[2] -= 1
                bullets.remove(bullet)
                if big_enemy[2] <= 0:
                    score += 50
                    big_enemies.remove(big_enemy)
                    enemy_destroy_sound.play()
                break

def show_game_over():
    pygame.mixer.music.stop()  # Stop background music
    game_over_sound.play()
    screen.fill(BLACK)
    game_over_text = font.render(f"Game Over! Final Score: {score}", True, WHITE)
    restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    pygame.mixer.music.load('background_music.mp3')  # Make sure to replace with your actual music file
                    pygame.mixer.music.play(-1)  # Restart background music
                    return True
                elif event.key == pygame.K_q:
                    return False

def show_welcome_screen():
    screen.blit(background_image, (0, 0))
    # welcome_text = font.render("Welcome to Zombies Warrior", True, WHITE)
    start_text = font.render("Press any key to start", True, WHITE)
    # screen.blit(welcome_text, (WIDTH//2 - welcome_text.get_width()//2, HEIGHT//2 - 50))
    screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2 + 260))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False
                
def show_end_screen():
    pygame.mixer.music.stop()
    pygame.mixer.music.load(os.path.join(current_dir, "end.mp3"))
    pygame.mixer.music.play(-1)
    end_image = pygame.image.load(os.path.join(current_dir, "end.png"))
    end_image = pygame.transform.scale(end_image, (WIDTH, HEIGHT))
    screen.blit(end_image, (0, 0))
    font = pygame.font.Font(None, 50)  # Use a system font, or provide a font file instead of 'None'
    text = font.render("You defeated the darkness, now you can rest.", True, (0, 0, 0))  # White text
    # Get the text's rect and center it on the screen
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 8))
    # Blit the text onto the screen
    screen.blit(text, text_rect)

    pygame.display.flip()
    pygame.time.wait(10000)  # Show the end screen for 10 seconds before exiting
    pygame.quit()
    sys.exit()


def game_loop():
    global player_x, player_y, score, player_lives, enemies, big_enemies, bullets, enemy_speed
    global power_up_timer, power_up_pos, last_shot_time, ENEMY_SPAWN_RATE, current_level

    player_x = WIDTH // 2 - player_size // 2
    player_y = HEIGHT // 2 - player_size // 2
    score = 0
    player_lives = 5
    enemies = []
    big_enemies = []
    bullets = []
    enemy_speed = 1.5
    power_up_timer = 0
    power_up_pos = None
    last_shot_time = 0
    current_level = 1

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x = max(0, player_x - player_speed)
        if keys[pygame.K_RIGHT]:
            player_x = min(WIDTH - player_size, player_x + player_speed)
        if keys[pygame.K_UP]:
            player_y = max(0, player_y - player_speed)
        if keys[pygame.K_DOWN]:
            player_y = min(HEIGHT - player_size, player_y + player_speed)

        update_player_trail()

        # Shooting with cooldown
        current_time = pygame.time.get_ticks()
        if current_time - last_shot_time > SHOOT_COOLDOWN:
            dx, dy = 0, 0
            if keys[pygame.K_a]:
                dx = -1
            elif keys[pygame.K_d]:
                dx = 1
            if keys[pygame.K_w]:
                dy = -1
            elif keys[pygame.K_s]:
                dy = 1
            
            if dx != 0 or dy != 0:
                bullets.append([player_x + player_size // 2, player_y + player_size // 2, dx, dy])
                last_shot_time = current_time
                #shoot_sound.play()

        # Spawn enemies
        if random.randint(1, ENEMY_SPAWN_RATE) == 1:
            side = random.choice(['top', 'bottom', 'left', 'right'])
            if side == 'top':
                enemies.append([random.randint(0, WIDTH - enemy_size), -enemy_size])
            elif side == 'bottom':
                enemies.append([random.randint(0, WIDTH - enemy_size), HEIGHT])
            elif side == 'left':
                enemies.append([-enemy_size, random.randint(0, HEIGHT - enemy_size)])
            else:
                enemies.append([WIDTH, random.randint(0, HEIGHT - enemy_size)])

        # Spawn big enemies
        if random.randint(1, BIG_ENEMY_SPAWN_RATE) == 1:
            side = random.choice(['top', 'bottom', 'left', 'right'])
            if side == 'top':
                big_enemies.append([random.randint(0, WIDTH - big_enemy_size), -big_enemy_size, big_enemy_health])
            elif side == 'bottom':
                big_enemies.append([random.randint(0, WIDTH - big_enemy_size), HEIGHT, big_enemy_health])
            elif side == 'left':
                big_enemies.append([-big_enemy_size, random.randint(0, HEIGHT - big_enemy_size), big_enemy_health])
            else:
                big_enemies.append([WIDTH, random.randint(0, HEIGHT - big_enemy_size), big_enemy_health])

        move_enemies()
        move_bullets()
        check_collisions()

        # Power-up logic
        power_up_timer += 1
        if power_up_timer >= POWER_UP_INTERVAL:
            power_up_timer = 0
            power_up_pos = (random.randint(0, WIDTH), random.randint(0, HEIGHT))

        if power_up_pos:
            if (player_x < power_up_pos[0] + 10 and
                player_x + player_size > power_up_pos[0] - 10 and
                player_y < power_up_pos[1] + 10 and
                player_y + player_size > power_up_pos[1] - 10):
        
                enemies = []  # Kill all enemies
                big_enemies = []  # Kill all big enemies
                power_up_pos = None
                score += 50
                power_up_sound.play()
        
                # Show the jumpscare image
                screen.blit(jumpscare_image, (0, 0))
                pygame.display.flip()
                pygame.time.delay(200)  # Display the jumpscare image for 0.2 seconds


        # Remove off-screen bullets
        bullets = [bullet for bullet in bullets if 0 <= bullet[0] <= WIDTH and 0 <= bullet[1] <= HEIGHT]

        screen.blit(title_screen, (0, 0))  # Draw title screen as background
        draw_player_trail()
        draw_player()
        draw_enemies()
        draw_bullets()
        draw_power_up()

        # Draw score, lives, and level
        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {player_lives}", True, WHITE)
        level_text = font.render(f"Level: {current_level}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (WIDTH - lives_text.get_width() - 10, 10))
        screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, 10))

        pygame.display.flip()
        clock.tick(60)

        # Check for level up
        if score >= current_level * POINTS_PER_LEVEL:
            current_level += 1
            
            if current_level == 6:
                enemies = []  # Clear all existing enemies
                big_enemies = []  # Clear all big enemies
                pygame.mixer.music.stop()
                pygame.mixer.music.load(os.path.join(current_dir, "final_boss.mp3"))
                pygame.mixer.music.play(-1)
                enemy_speed = 3
                
            elif current_level < 6:
                enemies = []  # Clear all enemies on level up
                big_enemies = []  # Clear all big enemies on level up
                show_level_screen(current_level)
                increase_difficulty()
            else:
                show_end_screen()


        if player_lives <= 0:
            running = False

    return show_game_over()

# Main game loop
show_welcome_screen()
while game_loop():
    pass

pygame.quit()
sys.exit()