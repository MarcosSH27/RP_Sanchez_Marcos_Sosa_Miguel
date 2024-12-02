#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Game made with AI assistance by:
# Miguel Sosa
# Marcos Sanchez

import roslib
import rospy
import rospkg
import time
import random
import sys
import os
import pygame
import math
import numpy as np

from std_msgs.msg import String, Int64
from RP_Sanchez_Marcos_Sosa_Miguel.msg import User_msg
from RP_Sanchez_Marcos_Sosa_Miguel.srv import GetUserScore, SetGameDifficulty

# Initialize pygame
pygame.init()

class Game():
    def __init__(self):
        """
        Init method.
        """
        # Class variables

        self.__sub_user_info = rospy.Subscriber("user_information", User_msg, self.welcome)

        self.__pub_score = rospy.Publisher("result_information", Int64, queue_size=10)

        self.__sub_control_pygame = rospy.Subscriber("keyboard_control", String, self.control)

        self.__sub_control = rospy.Subscriber("keyboard_control", String, self.control)

        self.service_user_score = rospy.Service("user_score", GetUserScore, self.handle_userscore)

        self.__service_difficulty = rospy.Service("difficulty", SetGameDifficulty, self.handle_setgamedifficulty)

        # Screen setup
        self.WIDTH = 800 
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.PURPLE = (128, 0, 128)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.ORANGE = (255, 165, 0)
        self.change_player_color = 2

        # Player setup
        self.player_size = 30
        self.player_x = self.WIDTH // 2 - self.player_size // 2
        self.player_y = self.HEIGHT // 2 - self.player_size // 2
        self.player_speed = 3
        self.player_lives = 5  

        # Constants for game balance
        self.DIFFICULTY_INCREASE_THRESHOLD = 300  # Increased from 200 to make the game easier
        self.MAX_ENEMY_SPEED = self.player_speed - 2  # Reduced to make the game easier
        self.ENEMY_SPAWN_RATE = 180  # Increased from 120 to make enemies spawn less frequently
        self.POWER_UP_INTERVAL = 15 * 60  # Reduced from 20 seconds to 15 seconds
        self.SHOOT_COOLDOWN = 30  # Increased from 15 to decrease shoot rate
        self.TRAIL_DURATION = 30

        # Additional setup
        self.power_up_timer = 0
        self.power_up_pos = None
        self.last_shot_time = 0
        self.player_trail = []

        # Enemy setup
        self.enemy_size = 20
        self.enemies = []
        self.enemy_speed = 1.5  # Reduced from 2 to make the game easier

        # Big enemy setup
        self.big_enemy_size = 40
        self.big_enemies = []
        self.big_enemy_speed = 1
        self.big_enemy_health = 20
        self.BIG_ENEMY_SPAWN_RATE = 600  # Lower rate of appearance

        # Bullet setup
        self.bullet_size = 5
        self.bullets = []
        self.bullet_speed = 10  

        # Game variables
        self.score = 0
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        # Load sounds
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.background_music = pygame.mixer.music.load(os.path.join(self.current_dir, "background_music.mp3"))
        self.game_over_sound = pygame.mixer.Sound(os.path.join(self.current_dir, "game_over.mp3"))
        self.enemy_destroy_sound = pygame.mixer.Sound(os.path.join(self.current_dir, "zombie.mp3"))
        self.player_hit_sound = pygame.mixer.Sound(os.path.join(self.current_dir, "damage.mp3"))
        self.power_up_sound = pygame.mixer.Sound(os.path.join(self.current_dir, "boom.mp3"))
        #shoot_sound = pygame.mixer.Sound(os.path.join(current_dir, "pew.mp3"))

        # Load the jumpscare image
        self.jumpscare_image = pygame.image.load(os.path.join(self.current_dir, "jumpscare.png"))
        self.jumpscare_image = pygame.transform.scale(self.jumpscare_image, (self.WIDTH, self.HEIGHT))  # Scale to fit the screen

        # Load background image
        self.background_image = pygame.image.load(os.path.join(self.current_dir, "title_screen.png"))
        self.background_image = pygame.transform.scale(self.background_image, (self.WIDTH, self.HEIGHT))
        # Load title screen image

        self.title_screen = pygame.image.load(os.path.join(self.current_dir, "screen.png"))
        self.title_screen = pygame.transform.scale(self.title_screen, (self.WIDTH, self.HEIGHT))

        # Level variables
        self.current_level = 1
        self.POINTS_PER_LEVEL = 200

        self.waiting = True

        self.player_trail

        self.score
        self.player_lives

        self.player_x
        self.player_y
        self.score 
        self.player_lives
        self.enemies
        self.big_enemies 
        self.bullets 
        self.enemy_speed
        self.power_up_timer
        self.power_up_pos 
        self.last_shot_time 
        self.difficulty_multiplier = 0
        # self.ENEMY_SPAWN_RATE 
        self.current_level

        # self.end_image
        self.waiting_decision = True
        self.retry = False
        self.quit = False
        self.screen_param = "phase1"

    def game(self, player):

        rospy.loginfo("Zombies Warrior started!")

        pygame.display.set_caption("Zombies Warrior")
        # Initialize the mixer
        pygame.mixer.init()
        # Load and play background music
        pygame.mixer.music.load('background_music.mp3')  
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely

        # Set the volume (0.0 to 1.0)
        pygame.mixer.music.set_volume(0.1)  # Adjust this value to decrease volume as needed

        self.show_welcome_screen(player)
        self.choose_difficulty()
        rospy.loginfo("Game phase started!")
        while self.game_loop():
            pass
        self.final()

        pygame.quit()
        sys.exit()

    def welcome(self, player):
        try:
            rospy.logwarn(f"You are at {self.screen_param}")
            rospy.set_param('screen', self.screen_param)
            rospy.loginfo(" The name is [%s]", player.name)
            rospy.loginfo(" The username is [%s]", player.username)
            rospy.loginfo(" The age is [%s]", player.age)
            self.user_name = player.username
            self.game(player)
        except Exception as e:
            rospy.logerr("Error in callback: %s", str(e))

    def final(self):
        rospy.loginfo("Final phase reached, calculating final score...")
        self.__pub_score.publish(self.score)
    
    def handle_userscore(self, req):
        user = req.username
        # Srv code
        if(str(user) == str(self.user_name)):
            rospy.loginfo(" User is : %s" , str(user) )
        else:
            rospy.logwarn("Wrong username")
            return -99999999
        response = self.score
        print(" The final score is:" + str(self.score))
        return response

    def control(self, msg):
        self.waiting = False

        data = msg.data
        # rospy.loginfo(f"{data} actions recieved!")

        actions = data.split(',')
    
        movement = ""
        shoot_direction = ""
        decision = ""

        self.change_player_color = rospy.get_param('change_player_color')

        if len(actions) == 3:
            movement, shoot_direction, decision = actions
            # rospy.loginfo(f"Movement: {movement}, Shooting Direction: {shoot_direction}")

        if decision == "R":
            self.retry = True
        elif decision == "Q":
            self.quit = True
        """
        elif decision == "1":
            self.change_player_color = 1
            self.draw_player()
            self.draw_player_trail()
        elif decision == "2":
            self.change_player_color = 2
            self.draw_player()
            self.draw_player_trail()
        elif decision == "3":
            self.change_player_color = 3
            self.draw_player()
            self.draw_player_trail()
        """
        elif movement == "LEFT":
            self.player_x = max(0, self.player_x - self.player_speed)
        elif movement == "RIGHT":
            self.player_x = min(self.WIDTH - self.player_size, self.player_x + self.player_speed)
        elif movement == "UP":
            self.player_y = max(0, self.player_y - self.player_speed)
        elif movement == "DOWN":
            self.player_y = min(self.HEIGHT - self.player_size, self.player_y + self.player_speed)
        elif movement == "DOWN_LEFT":
            self.player_y = min(self.HEIGHT - self.player_size, self.player_y + self.player_speed)
            self.player_x = max(0, self.player_x - self.player_speed)
        elif movement == "DOWN_RIGHT":
            self.player_y = min(self.HEIGHT - self.player_size, self.player_y + self.player_speed)
            self.player_x = min(self.WIDTH - self.player_size, self.player_x + self.player_speed)
        elif movement == "UP_RIGHT":
            self.player_y = max(0, self.player_y - self.player_speed)
            self.player_x = min(self.WIDTH - self.player_size, self.player_x + self.player_speed)
        elif movement == "UP_LEFT":
            self.player_y = max(0, self.player_y - self.player_speed)
            self.player_x = max(0, self.player_x - self.player_speed)

        # Shooting with cooldown
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.last_shot_time > self.SHOOT_COOLDOWN:
            self.dx, self.dy = 0, 0
            if shoot_direction == "A":
                self.dx = -1
            elif shoot_direction == "D":
                self.dx = 1
            elif shoot_direction == "W":
                self.dy = -1
            elif shoot_direction == "S":
                self.dy = 1
            elif shoot_direction == "S_A":
                self.dy = 1
                self.dx = -1
            elif shoot_direction == "S_D":
                self.dy = 1
                self.dx = 1
            elif shoot_direction == "W_D":
                self.dy = -1
                self.dx = 1
            elif shoot_direction == "W_A":
                self.dy = -1
                self.dx = -1

            if self.dx != 0 or self.dy != 0:
                self.bullets.append([self.player_x + self.player_size // 2, self.player_y + self.player_size // 2, self.dx, self.dy])
                self.last_shot_time = self.current_time

        
    def show_level_screen(self):
        self.screen.fill(self.BLACK)
        self.level_text = self.font.render(f"Level {self.current_level}", True, self.WHITE)
        self.continue_text = self.font.render("Press any key to continue", True, self.WHITE)
        self.screen.blit(self.level_text, (self.WIDTH//2 - self.level_text.get_width()//2, self.HEIGHT//2 - 50))
        self.screen.blit(self.continue_text, (self.WIDTH//2 - self.continue_text.get_width()//2, self.HEIGHT//2 + 50))
        pygame.display.flip()

        time.sleep(0.5)
        self.waiting = True
        while self.waiting:
            pass

    def increase_difficulty(self):
        # global enemy_speed, ENEMY_SPAWN_RATE, big_enemy_speed, BIG_ENEMY_SPAWN_RATE
        self.enemy_speed *= 1.2
        self.ENEMY_SPAWN_RATE = max(20, int(self.ENEMY_SPAWN_RATE * 0.75))  # Increased enemy spawn rate
        self.big_enemy_speed *= 1.1
        self.BIG_ENEMY_SPAWN_RATE = max(200, int(self.BIG_ENEMY_SPAWN_RATE * 0.75))  # Increase big enemy spawn rate

    def draw_player(self):
        if self.change_player_color == 1:
            pygame.draw.circle(self.screen, self.RED, (int(self.player_x + self.player_size // 2), int(self.player_y + self.player_size // 2)), self.player_size // 2)
        elif self.change_player_color == 2:
            pygame.draw.circle(self.screen, self.PURPLE, (int(self.player_x + self.player_size // 2), int(self.player_y + self.player_size // 2)), self.player_size // 2)
        else:
            pygame.draw.circle(self.screen, self.BLUE, (int(self.player_x + self.player_size // 2), int(self.player_y + self.player_size // 2)), self.player_size // 2)

    def draw_enemies(self):
        for enemy in self.enemies:
            pygame.draw.rect(self.screen, self.RED, (enemy[0], enemy[1], self.enemy_size, self.enemy_size))
        for big_enemy in self.big_enemies:
            pygame.draw.rect(self.screen, self.ORANGE, (big_enemy[0], big_enemy[1], self.big_enemy_size, self.big_enemy_size))

    def draw_bullets(self):
        for self.bullet in self.bullets:
            pygame.draw.rect(self.screen, self.WHITE, (self.bullet[0], self.bullet[1], self.bullet_size, self.bullet_size))

    def draw_power_up(self):
        if self.power_up_pos:
            pygame.draw.circle(self.screen, (0, 0, 255), self.power_up_pos, 10)

    def draw_player_trail(self):
        for self.pos, self.alpha in self.player_trail:
            self.s = pygame.Surface((5, 5))
            self.s.set_alpha(self.alpha)
            if self.change_player_color == 1:
                self.s.fill(self.RED)
            elif self.change_player_color == 2:
                self.s.fill(self.PURPLE)
            else:
                self.s.fill(self.BLUE)
            self.screen.blit(self.s, self.pos)

    def update_player_trail(self):
        # global player_trail
        self.player_trail.insert(0, ((self.player_x + self.player_size // 2, self.player_y + self.player_size // 2), 255))
        self.player_trail = [(self.pos, max(0, self.alpha - 255 // self.TRAIL_DURATION)) for self.pos, self.alpha in self.player_trail]
        self.player_trail = [self.item for self.item in self.player_trail if self.item[1] > 0]

    def move_enemies(self):
        for enemy in self.enemies:
            self.dx = self.player_x - enemy[0]
            self.dy = self.player_y - enemy[1]
            self.dist = (self.dx**2 + self.dy**2)**0.5
            if self.dist != 0:
                enemy[0] += self.dx / self.dist * self.enemy_speed
                enemy[1] += self.dy / self.dist * self.enemy_speed
        for big_enemy in self.big_enemies:
            self.dx = self.player_x - big_enemy[0]
            self.dy = self.player_y - big_enemy[1]
            self.dist = (self.dx**2 + self.dy**2)**0.5
            if self.dist != 0:
                big_enemy[0] += self.dx / self.dist * self.big_enemy_speed
                big_enemy[1] += self.dy / self.dist * self.big_enemy_speed

    def move_bullets(self):
        for self.bullet in self.bullets:
            self.bullet[0] += self.bullet[2] * self.bullet_speed
            self.bullet[1] += self.bullet[3] * self.bullet_speed

    def check_collisions(self):
        # global score, player_lives
        for enemy in self.enemies[:]:
            if (self.player_x < enemy[0] + self.enemy_size and
                self.player_x + self.player_size > enemy[0] and
                self.player_y < enemy[1] + self.enemy_size and
                self.player_y + self.player_size > enemy[1]):
                self.player_lives -= 1
                self.enemies.remove(enemy)
                self.player_hit_sound.play()
            for bullet in self.bullets[:]:
                if (bullet[0] < enemy[0] + self.enemy_size and
                    bullet[0] + self.bullet_size > enemy[0] and
                    bullet[1] < enemy[1] + self.enemy_size and
                    bullet[1] + self.bullet_size > enemy[1]):
                    self.score += 10
                    self.enemies.remove(enemy)
                    self.bullets.remove(bullet)
                    self.enemy_destroy_sound.play()
                    break
        
        for big_enemy in self.big_enemies[:]:
            if (self.player_x < big_enemy[0] + self.big_enemy_size and
                self.player_x + self.player_size > big_enemy[0] and
                self.player_y < big_enemy[1] + self.big_enemy_size and
                self.player_y + self.player_size > big_enemy[1]):
                self.player_lives -= 2
                self.big_enemies.remove(big_enemy)
                self.player_hit_sound.play()
            for bullet in self.bullets[:]:
                if (bullet[0] < big_enemy[0] + self.big_enemy_size and
                    bullet[0] + self.bullet_size > big_enemy[0] and
                    bullet[1] < big_enemy[1] + self.big_enemy_size and
                    bullet[1] + self.bullet_size > big_enemy[1]):
                    big_enemy[2] -= 1
                    self.bullets.remove(bullet)
                    if big_enemy[2] <= 0:
                        self.score += 50
                        self.big_enemies.remove(big_enemy)
                        self.enemy_destroy_sound.play()
                    break

    def show_game_over(self):
        pygame.mixer.music.stop()  # Stop background music
        self.game_over_sound.play()
        self.screen.fill(self.BLACK)
        self.game_over_text = self.font.render(f"Game Over! Final Score: {self.score}", True, self.WHITE)
        self.restart_text = self.font.render("Press R to Restart or Q to Quit", True, self.WHITE)
        self.screen.blit(self.game_over_text, (self.WIDTH//2 - self.game_over_text.get_width()//2, self.HEIGHT//2 - 50))
        self.screen.blit(self.restart_text, (self.WIDTH//2 - self.restart_text.get_width()//2, self.HEIGHT//2 + 50))
        pygame.display.flip()

        time.sleep(0.5)
        self.waiting_decision = True
        self.retry = False
        self.quit = False
        self.screen_param = "phase3"
        rospy.logwarn(f"You are at {self.screen_param}")
        rospy.set_param('screen', self.screen_param)
        while self.waiting_decision:
            if self.retry:
                pygame.mixer.music.load('background_music.mp3')  
                pygame.mixer.music.play(-1)  # Restart background music
                # Enemy setup
                self.enemy_speed = 1.5 * self.difficulty_multiplier  # Reduced from 2 to make the game easier
                self.ENEMY_SPAWN_RATE = 180
                # Big enemy setup
                self.big_enemy_speed = 1
                self.BIG_ENEMY_SPAWN_RATE = 600
                self.screen_param = "phase1"
                rospy.logwarn(f"You are at {self.screen_param}")
                rospy.set_param('screen', self.screen_param)
                self.choose_difficulty()
                return True
            if self.quit:
                return False

    def show_welcome_screen(self, player):
        # Start playing background music
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely
        
        self.screen.blit(self.background_image, (0, 0))
        # welcome_text = font.render("Welcome to Zombies Warrior", True, WHITE)
        self.start_text = self.font.render(f"Welcome {player.username}! Press any key to start", True, self.WHITE)
        # screen.blit(welcome_text, (WIDTH//2 - welcome_text.get_width()//2, HEIGHT//2 - 50))
        self.screen.blit(self.start_text, (self.WIDTH//2 - self.start_text.get_width()//2, self.HEIGHT//2 + 260))
        pygame.display.flip()

        time.sleep(0.5)
        self.waiting = True
        while self.waiting:
            pass
    
    def choose_difficulty(self):
        self.screen.fill(self.BLACK)
        self.difficulty_text = self.font.render("Choose Difficulty:", True, self.WHITE)
        self.options_text = self.font.render("  Easy   Medium   Hard  ", True, self.WHITE)

        self.screen.blit(self.difficulty_text, (self.WIDTH // 2 - self.difficulty_text.get_width() // 2, self.HEIGHT // 2 - 100))
        self.screen.blit(self.options_text, (self.WIDTH // 2 - self.options_text.get_width() // 2, self.HEIGHT // 2))


        pygame.display.flip()
        time.sleep(0.5)
        self.difficulty_multiplier = 0
        while self.difficulty_multiplier==0:
            pass

    def handle_setgamedifficulty(self,req):
        if self.screen_param == "phase1":
            difficulty = req.change_difficulty
            # Srv code
            if difficulty != "easy" and difficulty != "medium" and difficulty != "hard":
                rospy.loginfo("Not a difficulty, set to medium")
                difficulty = "medium"
                self.difficulty_multiplier = 1

            else:
                if difficulty == "easy":
                    self.difficulty_multiplier = 0.5
                elif difficulty == "medium":
                    self.difficulty_multiplier = 1
                else:
                    self.difficulty_multiplier = 2

            rospy.loginfo(" Difficulty is : %s" , str(difficulty) )
            response = True
            print(" Bool:" + str(True))
            return response
        else:
            return False

    def show_end_screen(self):
        self.screen_param = "phase3"
        rospy.logwarn(f"You are at {self.screen_param}")
        rospy.set_param('screen', self.screen_param)
        pygame.mixer.music.stop()
        pygame.mixer.music.load(os.path.join(self.current_dir, "end.mp3"))
        pygame.mixer.music.play(-1)
        self.end_image = pygame.image.load(os.path.join(self.current_dir, "end.png"))
        self.end_image = pygame.transform.scale(self.end_image, (self.WIDTH, self.HEIGHT))
        self.screen.blit(self.end_image, (0, 0))
        self.font = pygame.font.Font(None, 50)  # Use a system font, or provide a font file instead of 'None'
        self.text = self.font.render("You defeated the darkness, now you can rest.", True, (0, 0, 0))  # White text
        # Get the text's rect and center it on the screen
        self.text_rect = self.text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 8))
        # Blit the text onto the screen
        self.screen.blit(self.text, self.text_rect)

        pygame.display.flip()
        pygame.time.wait(10000)  # Show the end screen for 10 seconds before exiting
        self.final()
        pygame.quit()
        sys.exit()


    def game_loop(self):
        # global player_x, player_y, score, player_lives, enemies, big_enemies, bullets, enemy_speed
        # global power_up_timer, power_up_pos, last_shot_time, ENEMY_SPAWN_RATE, current_level

        self.player_x = self.WIDTH // 2 - self.player_size // 2
        self.player_y = self.HEIGHT // 2 - self.player_size // 2
        self.score = 0
        self.player_lives = 5
        self.enemies = []
        self.big_enemies = []
        self.bullets = []
        self.enemy_speed = 1.5 * self.difficulty_multiplier
        self.power_up_timer = 0
        self.power_up_pos = None
        self.last_shot_time = 0
        self.current_level = 1
        self.screen_param = "phase2"
        rospy.logwarn(f"You are at {self.screen_param}")
        rospy.set_param('screen', self.screen_param)
        self.running = True
        while self.running:
            for self.event in pygame.event.get():
                if self.event.type == pygame.QUIT:
                    self.running = False
            
            self.update_player_trail()

            # Spawn enemies
            if random.randint(1, self.ENEMY_SPAWN_RATE) == 1:
                self.side = random.choice(['top', 'bottom', 'left', 'right'])
                if self.side == 'top':
                    self.enemies.append([random.randint(0, self.WIDTH - self.enemy_size), -self.enemy_size])
                elif self.side == 'bottom':
                    self.enemies.append([random.randint(0, self.WIDTH - self.enemy_size), self.HEIGHT])
                elif self.side == 'left':
                    self.enemies.append([-self.enemy_size, random.randint(0, self.HEIGHT - self.enemy_size)])
                else:
                    self.enemies.append([self.WIDTH, random.randint(0, self.HEIGHT - self.enemy_size)])

            # Spawn big enemies
            if random.randint(1, self.BIG_ENEMY_SPAWN_RATE) == 1:
                self.side = random.choice(['top', 'bottom', 'left', 'right'])
                if self.side == 'top':
                    self.big_enemies.append([random.randint(0, self.WIDTH - self.big_enemy_size), -self.big_enemy_size, self.big_enemy_health])
                elif self.side == 'bottom':
                    self.big_enemies.append([random.randint(0, self.WIDTH - self.big_enemy_size), self.HEIGHT, self.big_enemy_health])
                elif self.side == 'left':
                    self.big_enemies.append([-self.big_enemy_size, random.randint(0, self.HEIGHT - self.big_enemy_size), self.big_enemy_health])
                else:
                    self.big_enemies.append([self.WIDTH, random.randint(0, self.HEIGHT - self.big_enemy_size), self.big_enemy_health])

            self.move_enemies()
            self.move_bullets()
            self.check_collisions()

            # Power-up logic
            self.power_up_timer += 1
            if self.power_up_timer >= self.POWER_UP_INTERVAL:
                self.power_up_timer = 0
                self.power_up_pos = (random.randint(0, self.WIDTH), random.randint(0, self.HEIGHT))

            if self.power_up_pos:
                if (self.player_x < self.power_up_pos[0] + 10 and
                    self.player_x + self.player_size > self.power_up_pos[0] - 10 and
                    self.player_y < self.power_up_pos[1] + 10 and
                    self.player_y + self.player_size > self.power_up_pos[1] - 10):
            
                    self.enemies = []  # Kill all enemies
                    self.big_enemies = []  # Kill all big enemies
                    self.power_up_pos = None
                    self.score += 50
                    self.power_up_sound.play()
            
                    # Show the jumpscare image
                    self.screen.blit(self.jumpscare_image, (0, 0))
                    pygame.display.flip()
                    pygame.time.delay(200)  # Display the jumpscare image for 0.2 seconds


            # Remove off-screen bullets
            self.bullets = [self.bullet for self.bullet in self.bullets if 0 <= self.bullet[0] <= self.WIDTH and 0 <= self.bullet[1] <= self.HEIGHT]

            self.screen.blit(self.title_screen, (0, 0))  # Draw title screen as background
            self.draw_player_trail()
            self.draw_player()
            self.draw_enemies()
            self.draw_bullets()
            self.draw_power_up()

            # Draw score, lives, and level
            self.score_text = self.font.render(f"Score: {self.score}", True, self.WHITE)
            self.lives_text = self.font.render(f"Lives: {self.player_lives}", True, self.WHITE)
            self.level_text = self.font.render(f"Level: {self.current_level}", True, self.WHITE)
            self.screen.blit(self.score_text, (10, 10))
            self.screen.blit(self.lives_text, (self.WIDTH - self.lives_text.get_width() - 10, 10))
            self.screen.blit(self.level_text, (self.WIDTH // 2 - self.level_text.get_width() // 2, 10))

            pygame.display.flip()
            self.clock.tick(60)

            # Check for level up
            if self.score >= self.current_level * self.POINTS_PER_LEVEL:
                self.current_level += 1
                
                if self.current_level == 6:
                    self.enemies = []  # Clear all existing enemies
                    self.big_enemies = []  # Clear all big enemies
                    self.show_level_screen()
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(os.path.join(self.current_dir, "final_boss.mp3"))
                    pygame.mixer.music.play(-1)
                    self.enemy_speed = 4 * self.difficulty_multiplier
 
                    
                elif self.current_level < 6:
                    self.enemies = []  # Clear all enemies on level up
                    self.big_enemies = []  # Clear all big enemies on level up
                    self.show_level_screen()
                    self.increase_difficulty()
                else:
                    self.show_end_screen()


            if self.player_lives <= 0:
                self.running = False

        return self.show_game_over()


if __name__ == '__main__':
    # Initialize pygame
    pygame.init()
    
    try:
        name_node = "game"
        rospy.init_node(name_node)
        rospy.loginfo("The node %s has started", name_node)

        #create and spin the node 
        node = Game()

        # Keep the node running until it is shut down
        rospy.spin()

    except rospy.ROSInterruptException:
        pass