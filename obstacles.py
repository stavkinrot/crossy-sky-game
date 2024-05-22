import pygame
from random import randint, choice

numbers_in_increments_of_32 = list(range(64, 737, 32))

class Obstacles(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        y_pos = choice(numbers_in_increments_of_32)
        if type == 'eagle':
            fly_1 = pygame.image.load('graphics/Eagle/left1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/Eagle/left2.png').convert_alpha()
            fly_3 = pygame.image.load('graphics/Eagle/left3.png').convert_alpha()
            self.frames = [fly_1, fly_2, fly_3]
        # else:
        #     snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
        #     snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
        #     self.frames = [snail_1, snail_2]
        #     y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.3
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
