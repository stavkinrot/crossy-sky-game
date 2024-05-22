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
difficulty_level = 0

sky_surface = pygame.image.load('graphics/Sky.jpg').convert_alpha()
sky_surface = pygame.transform.rotozoom(sky_surface, 0, 0.4)


def display_score():
    score_surf = test_font.render(f'Score: {score}', False, (225, 245, 255))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return score

def level_up(score, difficulty):
    if player.sprite.rect.bottom < 0:
        score += 1
        if 1300 - difficulty > 250:
            difficulty += 150
        pygame.time.set_timer(obstacle_timer, int(1300 - difficulty))
    return score, difficulty

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

endpoint_group = pygame.sprite.GroupSingle()

# Intro screen
player_stand = pygame.image.load('graphics/White Bird/left2.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 400))

game_name = test_font.render('Crossy Sky', False, (225, 245, 255))
game_name = pygame.transform.rotozoom(game_name, 0, 2)
game_name_rect = game_name.get_rect(center=(400, 200))

game_message = test_font.render('Press UP to fly', False, (225, 245, 255))
game_message_rect = game_message.get_rect(center=(400, 600))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, int(1300*math.exp(-difficulty_level)))

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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                game_active = True

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
        screen.blit(player_stand, player_stand_rect)

        score_message = test_font.render(f'Your score: {score}', False, (225, 245, 255))
        score_message_rect = score_message.get_rect(center=(400, 330))

        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

        score = 0
        difficulty_level = 0
        player.sprite.rect.bottom = 780

    pygame.display.update()
    clock.tick(60)
