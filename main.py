import pygame
from sys import exit

from player import Player
from obstacles import Obstacles

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Crossy Sky')
clock = pygame.time.Clock()

# Fonts
score_font = pygame.font.Font('font/NicoClean-Regular.otf', 40)
title_font = pygame.font.Font('font/NicoClean-Regular.otf', 80)
message_font = pygame.font.Font('font/NicoPups-Regular.otf', 40)

# Game state variables
game_active = False
start_time = 0
score = 0
start_score = 0
difficulty_level = 0
START_DIFFICULTY = 1300
MAX_DIFFICULTY = 250
birds = ['White', 'Blue', 'Cardinal', 'Robin', 'Sparrow']
birds_index = 0
bird_chosen = False
sky_surface = None
instruction_menu = True

# Groups
obstacle_group = pygame.sprite.Group()

# Set up the birds
def set_birds():
    x_pos = 240
    player_bird = None
    birds_group = pygame.sprite.Group()
    for i in range(5):
        bird = Player(birds[i])
        bird.rect.center = (x_pos, 345)
        if i == birds_index:
            bird.player = True
            player_bird = bird
        birds_group.add(bird)
        x_pos += 40
    return player_bird, birds_group

# Display the score
def display_score():
    score_surf = score_font.render(f'Score: {score}', False, (225, 245, 255))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)

# Level up and increase difficulty
def level_up(score, difficulty):
    if player.sprite.rect.bottom < 0:
        player.sprite.rect.top = 780
        score += 1
        if START_DIFFICULTY - difficulty > MAX_DIFFICULTY: # Smaller numbers means eagles summons faster
            difficulty += 80
        pygame.time.set_timer(obstacle_timer, int(START_DIFFICULTY - difficulty))
    return score, difficulty

# Keep the player within the screen boundaries
def boundaries():
    if player.sprite.rect.right < 0:
        player.sprite.rect.left = 800
    if player.sprite.rect.left > 800:
        player.sprite.rect.right = 0
    if player.sprite.rect.bottom >= 790:
        player.sprite.rect.bottom = 790
    if player.sprite.rect.bottom < 0:
        player.sprite.rect.top = 780

# Check for collisions with eagles
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        pygame.time.set_timer(obstacle_timer, START_DIFFICULTY)
        return False
    else:
        return True

# Set the difficulty and background based on the chosen cloud
def set_difficulty(cloud):
    global sky_surface, MAX_DIFFICULTY, START_DIFFICULTY
    sky_backgrounds = ['Sunny Sky', 'Rainy Sky', 'Stormy Sky']
    sky_surface = pygame.image.load(f'graphics/background/{sky_backgrounds[cloud]}.png').convert_alpha()
    sky_surface = pygame.transform.rotozoom(sky_surface, 0, 0.4)
    if cloud == 0:
        START_DIFFICULTY = 1300
        MAX_DIFFICULTY = 275
    elif cloud == 1:
        START_DIFFICULTY = 1200
        MAX_DIFFICULTY = 250
    else:
        START_DIFFICULTY = 700
        MAX_DIFFICULTY = 225

# Game title and message
game_name = title_font.render('Crossy Sky', False, (225, 245, 255))
game_name_rect = game_name.get_rect(center=(400, 400))
game_message = message_font.render('Press UP to fly', False, (225, 245, 255))
game_message_rect = game_message.get_rect(center=(400, 500))

# Clouds - Difficulty levels
clouds_list = []
sunny_cloud = pygame.image.load('graphics/Regular Cloud 2.png').convert_alpha()
sunny_cloud = pygame.transform.rotozoom(sunny_cloud, 0, 0.25)
clouds_list.append(sunny_cloud.get_rect(center=(160, 150)))
rainy_cloud = pygame.image.load('graphics/Rain Cloud.png').convert_alpha()
rainy_cloud = pygame.transform.rotozoom(rainy_cloud, 0, 0.25)
clouds_list.append(rainy_cloud.get_rect(center=(410, 160)))
stormy_cloud = pygame.image.load('graphics/Storm Cloud.png').convert_alpha()
stormy_cloud = pygame.transform.rotozoom(stormy_cloud, 0, 0.25)
clouds_list.append(stormy_cloud.get_rect(center=(650, 200)))

# Instructions cloud (commented out as it's not used)
# instructions_cloud = pygame.image.load('graphics/Instruction Cloud.png').convert_alpha()
# instructions_cloud = pygame.transform.rotozoom(instructions_cloud, 0, 0.6)
# instructions_cloud_rect = instructions_cloud.get_rect(center=(400,600))

# Timer for spawning obstacles
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, START_DIFFICULTY)

# The Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacles())
        elif bird_chosen:
            for i in range(3):
                if player.sprite.rect.colliderect(clouds_list[i]):
                    set_difficulty(i)
                    game_active = True
                    instruction_menu = False
                    score = 0
                    difficulty_level = 0
                    player.sprite.rect.bottom = 780
        else:
            bird, birds_group = set_birds()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    bird_chosen = True
                    bird.chosen = True
                    bird.intro = False
                    birds_group.remove(bird)
                    player = pygame.sprite.GroupSingle()
                    player.add(bird)
                elif event.key == pygame.K_RIGHT:
                    birds_index = (birds_index + 1) % len(birds)
                elif event.key == pygame.K_LEFT:
                    birds_index = (birds_index - 1) % len(birds)

    if game_active:
        screen.blit(sky_surface, (0, 0))
        display_score()
        player.draw(screen)
        player.update()
        score, difficulty_level = level_up(score, difficulty_level)
        boundaries()
        obstacle_group.draw(screen)
        obstacle_group.update()
        game_active = collision_sprite()
        if not game_active:
            bird_chosen = False
            player.intro = True
            player.chosen = False
    else:
        screen.fill((44, 141, 222))
        score_message = message_font.render(f'Your score: {score}', False, (225, 245, 255))
        score_message_rect = score_message.get_rect(center=(400, 500))
        screen.blit(sunny_cloud, clouds_list[0])
        screen.blit(rainy_cloud, clouds_list[1])
        screen.blit(stormy_cloud, clouds_list[2])
        screen.blit(game_name, game_name_rect)
        obstacle_group.empty()
        if instruction_menu:
            screen.blit(game_message, game_message_rect)
            # screen.blit(instructions_cloud, instructions_cloud_rect)  # Commented out as it's not used
        else:
            screen.blit(score_message, score_message_rect)
        birds_group.draw(screen)
        birds_group.update()
        if bird_chosen:
            player.draw(screen)
            player.update()
            boundaries()

    pygame.display.update()
    clock.tick(60)