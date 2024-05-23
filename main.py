import pygame
from sys import exit
from random import randint, choice
import math

from player import Player

from obstacles import Obstacles

pygame.init()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Crossing game')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
start_score = 0
difficulty_level = 0
birds = ['White Bird', 'Blue Jay', 'Cardinal']
birds_index = 0

sky_surface = pygame.image.load('graphics/Sky.jpg').convert_alpha()
sky_surface = pygame.transform.rotozoom(sky_surface, 0, 0.4)

obstacle_group = pygame.sprite.Group()

def display_score():
    score_surf = test_font.render(f'Score: {score}', False, (225, 245, 255))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)


def level_up(score, difficulty):
    if player.sprite.rect.bottom < 0:
        player.sprite.rect.top = 780
        score += 1
        if 1300 - difficulty > 250:
            difficulty += 150
        pygame.time.set_timer(obstacle_timer, int(1300 - difficulty))
    return score, difficulty


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        pygame.time.set_timer(obstacle_timer, 1300)
        return False
    else:
        return True

# Intro screen
def intro_screen(birds, birds_index):
    player_stand = pygame.image.load(f'graphics/{birds[birds_index]}/left2.png').convert_alpha()
    player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
    player_stand_rect = player_stand.get_rect(center=(400, 400))
    return player_stand, player_stand_rect

intro_screen(birds, birds_index)
game_name = test_font.render('Crossy Sky', False, (225, 245, 255))
game_name = pygame.transform.rotozoom(game_name, 0, 1.75)
game_name_rect = game_name.get_rect(center=(400, 260))

game_message = test_font.render('Press UP to fly', False, (225, 245, 255))
game_message_rect = game_message.get_rect(center=(400, 540))

right_arrow = test_font.render('>', False, (225, 245, 255))
right_arrow = pygame.transform.rotozoom(right_arrow, 0, 1.5)
right_arrow_rect = right_arrow.get_rect(center=(500,400))

left_arrow = test_font.render('<', False, (225, 245, 255))
left_arrow = pygame.transform.rotozoom(left_arrow, 0, 1.5)
left_arrow_rect = right_arrow.get_rect(center=(300, 400))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1300)

# The Game Loop:
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacles(choice(['eagle'])))

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game_active = True
                    score = 0
                    difficulty_level = 0
                    player.sprite.rect.bottom = 780
                if event.key == pygame.K_RIGHT:
                    if birds_index == len(birds) - 1:
                        birds_index = 0
                    else:
                        birds_index += 1
                if event.key == pygame.K_LEFT:
                    if birds_index == 0:
                        birds_index = len(birds) - 1
                    else:
                        birds_index -= 1
                intro_screen(birds, birds_index)
            player = pygame.sprite.GroupSingle()
            player.add(Player(birds[birds_index]))


    if game_active:
        screen.blit(sky_surface, (0, 0))
        display_score()

        player.draw(screen)
        player.update()
        score, difficulty_level = level_up(score, difficulty_level)


        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()


    else:
        screen.fill((44, 141, 222))
        bird, bird_rect = intro_screen(birds, birds_index)
        screen.blit(bird, bird_rect)

        score_message = test_font.render(f'Your score: {score}', False, (225, 245, 255))
        score_message_rect = score_message.get_rect(center=(400, 330))

        screen.blit(game_name, game_name_rect)
        screen.blit(right_arrow, right_arrow_rect)
        screen.blit(left_arrow, left_arrow_rect)
        obstacle_group.empty()

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)




    pygame.display.update()
    clock.tick(60)
