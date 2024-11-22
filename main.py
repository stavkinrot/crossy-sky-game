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

# Music
easy_music = pygame.mixer.Sound('audio/[MapleStory BGM] Ludibrium_ Flying in a Blue Dream.mp3')
easy_music.set_volume(0.15)
normal_music = pygame.mixer.Sound('audio/[MapleStory BGM] Orbis_ Upon the Sky.mp3')
normal_music.set_volume(0.15)
hard_music = pygame.mixer.Sound('audio/[MapleStory BGM] The Final War (KMST 1.2.445).mp3')
hard_music.set_volume(0.15)
bg_music = [easy_music, normal_music, hard_music]


# Game state variables
game_active = False
start_time = 0
score = 0
screen_colors = [(44, 141, 222),(163, 175, 189),(0, 8, 44)]
color_index = 0
start_score = 0
difficulty_level = 0
START_DIFFICULTY = 1300
MAX_DIFFICULTY = 250
eagle_speed = 0
birds = ['White', 'Blue', 'Cardinal', 'Robin', 'Sparrow']
current_music = normal_music
birds_index = 0
bird_chosen = False
sky_surface = None
instruction_menu = True

current_music.play(loops=-1, fade_ms=2000)


# Groups
obstacle_group = pygame.sprite.Group()

def instruction_bird():
    screen.blit(branch, branch_rect)
    screen.blit(eagle_instructor, eagle_instructor_rect)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if eagle_instructor_rect.left <= mouse_x <= eagle_instructor_rect.right and eagle_instructor_rect.top <= mouse_y <= eagle_instructor_rect.bottom:
        screen.blit(instructions_cloud, instructions_cloud_rect)
    else: screen.blit(question_mark, question_mark_rect)

def change_music(music):
    global current_music
    if current_music is not music:
        current_music.fadeout(750)
        current_music = music
        current_music.play(loops=-1, fade_ms= 500)

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
    global sky_surface, MAX_DIFFICULTY, START_DIFFICULTY, color_index, eagle_speed
    sky_backgrounds = ['Sunny Sky', 'Rainy Sky', 'Stormy Sky']
    sky_surface = pygame.image.load(f'graphics/background/{sky_backgrounds[cloud]}.png').convert_alpha()
    sky_surface = pygame.transform.rotozoom(sky_surface, 0, 0.4)
    if cloud == 0:
        START_DIFFICULTY = 1300
        MAX_DIFFICULTY = 275
        eagle_speed = 6
    elif cloud == 1:
        START_DIFFICULTY = 1200
        MAX_DIFFICULTY = 250
        eagle_speed = 6.5
    else:
        START_DIFFICULTY = 700
        MAX_DIFFICULTY = 225
        eagle_speed = 7
    color_index = cloud
    return bg_music[cloud]

# Game title and message
game_name = title_font.render('Crossy Sky', False, (225, 245, 255))
game_name_rect = game_name.get_rect(center=(400, 400))
game_message = message_font.render('Press UP to fly', False, (225, 245, 255))
game_message_rect = game_message.get_rect(center=(400, 500))

# Clouds - Difficulty levels
clouds_list = []
sunny_cloud = pygame.image.load('graphics/Regular Cloud.png').convert_alpha()
sunny_cloud = pygame.transform.rotozoom(sunny_cloud, 0, 0.25)
clouds_list.append(sunny_cloud.get_rect(center=(160, 150)))
rainy_cloud = pygame.image.load('graphics/Rain Cloud.png').convert_alpha()
rainy_cloud = pygame.transform.rotozoom(rainy_cloud, 0, 0.25)
clouds_list.append(rainy_cloud.get_rect(center=(410, 160)))
stormy_cloud = pygame.image.load('graphics/Storm Cloud.png').convert_alpha()
stormy_cloud = pygame.transform.rotozoom(stormy_cloud, 0, 0.25)
clouds_list.append(stormy_cloud.get_rect(center=(650, 200)))

# Instructions graphics
eagle_instructor = pygame.image.load('graphics/Eagle/stand.png')
eagle_instructor = pygame.transform.rotozoom(eagle_instructor,0,2)
eagle_instructor_rect = eagle_instructor.get_rect(left=120, bottom=750)
branch = pygame.image.load('graphics/branch.png')
branch = pygame.transform.rotozoom(branch, 0, 0.35)
branch_rect = branch.get_rect(left=-10, bottom=850)
instructions_cloud = pygame.image.load('graphics/pixel-speech-bubble.png').convert_alpha()
instructions_cloud = pygame.transform.rotozoom(instructions_cloud, 0, 0.35)
question_mark = pygame.image.load('graphics/question_mark.png')
question_mark = pygame.transform.rotozoom(question_mark,0,0.05)
question_mark_rect = question_mark.get_rect(left=167, bottom=705)
instructions_cloud_rect = instructions_cloud.get_rect(left=30,bottom=700)

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
                obstacle_group.add(Obstacles(eagle_speed))
        elif bird_chosen:
            for i in range(3):
                if player.sprite.rect.colliderect(clouds_list[i]):
                    music = set_difficulty(i)
                    change_music(music)
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
        screen.fill(screen_colors[color_index])
        if instruction_menu:
            # screen.blit(game_message, game_message_rect)
            instruction_bird()
        else:
            screen.blit(score_message, score_message_rect)
        score_message = message_font.render(f'Your score: {score}', False, (225, 245, 255))
        score_message_rect = score_message.get_rect(center=(400, 500))
        screen.blit(sunny_cloud, clouds_list[0])
        screen.blit(rainy_cloud, clouds_list[1])
        screen.blit(stormy_cloud, clouds_list[2])
        screen.blit(game_name, game_name_rect)
        obstacle_group.empty()
        birds_group.draw(screen)
        birds_group.update()
        if bird_chosen:
            player.draw(screen)
            player.update()
            boundaries()

    pygame.display.update()
    clock.tick(60)