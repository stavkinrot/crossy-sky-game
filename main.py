import pygame
from sys import exit
from random import randint, choice

def display_score():
    score_cnt = 0 # Add functionallity
    score_surf = test_font.render(f'Score: {score_cnt}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return score_cnt


pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Crossing game')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0


