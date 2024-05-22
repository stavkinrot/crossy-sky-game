import pygame
pygame.init()


class Player(pygame.sprite.Sprite):
    def __init__(self, bird):
        super().__init__()
        rotate = 0
        if bird == 'Blue Jay': rotate = 180
        player_fly_up_1 = pygame.image.load(f'graphics/{bird}/tile006.png').convert_alpha()
        player_fly_up_1 = pygame.transform.rotozoom(player_fly_up_1, rotate, 2)
        player_fly_up_2 = pygame.image.load(f'graphics/{bird}/tile007.png').convert_alpha()
        player_fly_up_2 = pygame.transform.rotozoom(player_fly_up_2, rotate, 2)
        player_fly_up_3 = pygame.image.load(f'graphics/{bird}/tile008.png').convert_alpha()
        player_fly_up_3 = pygame.transform.rotozoom(player_fly_up_3, rotate, 2)
        player_fly_down_1 = pygame.image.load(f'graphics/{bird}/tile006.png').convert_alpha()
        player_fly_down_1 = pygame.transform.rotozoom(player_fly_down_1, rotate + 180, 2)
        player_fly_down_2 = pygame.image.load(f'graphics/{bird}/tile006.png').convert_alpha()
        player_fly_down_2 = pygame.transform.rotozoom(player_fly_down_2, rotate + 180, 2)
        player_fly_down_3 = pygame.image.load(f'graphics/{bird}/tile006.png').convert_alpha()
        player_fly_down_3 = pygame.transform.rotozoom(player_fly_down_3, rotate + 180, 2)
        player_fly_right_1 = pygame.image.load(f'graphics/{bird}/tile006.png').convert_alpha()
        player_fly_right_1 = pygame.transform.rotozoom(player_fly_right_1, rotate, 2)
        player_fly_right_2 = pygame.image.load(f'graphics/{bird}/tile006.png').convert_alpha()
        player_fly_right_2 = pygame.transform.rotozoom(player_fly_right_2, rotate, 2)
        player_fly_right_3 = pygame.image.load(f'graphics/{bird}/tile006.png').convert_alpha()
        player_fly_right_3 = pygame.transform.rotozoom(player_fly_right_3, rotate, 2)
        player_fly_left_1 = pygame.image.load(f'graphics/{bird}/tile006.png').convert_alpha()
        player_fly_left_1 = pygame.transform.rotozoom(player_fly_left_1, rotate, 2)
        player_fly_left_2 = pygame.image.load(f'graphics/{bird}/tile006.png').convert_alpha()
        player_fly_left_2 = pygame.transform.rotozoom(player_fly_left_2, rotate, 2)
        player_fly_left_3 = pygame.image.load(f'graphics/{bird}/tile006.png').convert_alpha()
        player_fly_left_3 = pygame.transform.rotozoom(player_fly_left_3, rotate, 2)

        self.player_fly_up = [player_fly_up_1, player_fly_up_2, player_fly_up_3]
        self.player_fly_down = [player_fly_down_1, player_fly_down_2, player_fly_down_3]
        self.player_fly_right = [player_fly_right_1, player_fly_right_2, player_fly_right_3]
        self.player_fly_left = [player_fly_left_1, player_fly_left_2, player_fly_left_3]
        self.player_index = 0
        self.image = self.player_fly_up[self.player_index]
        self.rect = self.image.get_rect(midbottom=(400, 780)).inflate(-25, -25)

    def animation_state(self):
        self.player_index += 0.3
        if self.player_index >= len(self.player_fly_up): self.player_index = 0
        self.image = self.player_fly_up[int(self.player_index)]

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            if self.rect.bottom >= 0:
                self.rect.top -= 5
                return False
            else:
                self.rect.top = 780

    def update(self):
        res = self.player_input()
        self.animation_state()
        return res


