import pygame

pygame.init()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_fly_1 = pygame.image.load('graphics/White Bird/tile006.png').convert_alpha()
        player_fly_1 = pygame.transform.rotozoom(player_fly_1, 180, 2)
        player_fly_2 = pygame.image.load('graphics/White Bird/tile007.png').convert_alpha()
        player_fly_2 = pygame.transform.rotozoom(player_fly_2, 180, 2)
        player_fly_3 = pygame.image.load('graphics/White Bird/tile008.png').convert_alpha()
        player_fly_3 = pygame.transform.rotozoom(player_fly_3, 180, 2)
        self.player_fly = [player_fly_1, player_fly_2, player_fly_3]
        self.player_index = 0

        self.image = self.player_fly[self.player_index]
        self.rect = self.image.get_rect(midbottom=(400, 780))

    def animation_state(self):
        self.player_index += 0.3
        if self.player_index >= len(self.player_fly): self.player_index = 0
        self.image = self.player_fly[int(self.player_index)]

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            if self.rect.bottom >= 0:
                self.rect.top -= 4
            else:
                self.rect.top = 780

    def update(self):
        self.player_input()
        self.animation_state()
