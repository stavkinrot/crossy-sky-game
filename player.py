import pygame

pygame.init()


class Player(pygame.sprite.Sprite):
    def __init__(self, bird):
        super().__init__()
        self.up_list = []
        self.down_list = []
        self.right_list = []
        self.left_list = []
        self.left_up_list = []
        self.left_down_list = []
        self.right_up_list = []
        self.right_down_list = []
        self.stand_list = []
        self.bird = bird
        self.intro = True
        self.player = False
        self.chosen = False

        # Upload image files:

        for i in range(0, 3):
            up = pygame.image.load(f'graphics/Birds/{bird}/tile00{+ (i + 3)}.png').convert_alpha()
            up_scale = pygame.transform.rotozoom(up, 0, 2)
            self.up_list.append(up_scale)

            down = pygame.transform.rotozoom(up, 180, 2)
            self.down_list.append(down)

            stand = pygame.image.load(f'graphics/Birds/{bird}/tile00{+ (i + 6)}.png').convert_alpha()
            stand = pygame.transform.rotozoom(stand, 0, 2)
            self.stand_list.append(stand)

            if i == 0:
                right = pygame.image.load(f'graphics/Birds/{bird}/tile00{+ (i + 9)}.png').convert_alpha()
            else:
                right = pygame.image.load(f'graphics/Birds/{bird}/tile0{+ (i + 9)}.png').convert_alpha()
            right_scale = pygame.transform.rotozoom(right, 0, 2)
            self.right_list.append(right_scale)

            right_up_scale = pygame.transform.rotozoom(right, 45, 2)
            self.right_up_list.append(right_up_scale)

            right_down_scale = pygame.transform.rotozoom(right, -45, 2)
            self.right_down_list.append(right_down_scale)

            left = pygame.image.load(f'graphics/Birds/{bird}/tile00{+ i}.png').convert_alpha()
            left_scale = pygame.transform.rotozoom(left, 0, 2)
            self.left_list.append(left_scale)

            left_up_scale = pygame.transform.rotozoom(left, -45, 2)
            self.left_up_list.append(left_up_scale)

            left_down_scale = pygame.transform.rotozoom(left, 45, 2)
            self.left_down_list.append(left_down_scale)

        # Initizalize bird's location

        self.animation_index = 0
        self.image = self.up_list[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(400, 780)).inflate(-25, -25)

    def animation_state(self, direction):
        self.animation_index += 0.3
        direction_lists = {'up': self.up_list,
                           'down': self.down_list,
                           'right': self.right_list,
                           'left': self.left_list,
                           'right_up': self.right_up_list,
                           'right_down': self.right_down_list,
                           'left_up': self.left_up_list,
                           'left_down': self.left_down_list,
                           'stand_list': self.stand_list
                           }
        if self.intro: direction = 'stand_list'
        elif direction is None: direction = 'up'
        image_list = direction_lists[direction]
        if self.animation_index >= len(image_list): self.animation_index = 0
        self.image = image_list[int(self.animation_index)]

    def player_input(self):
        if self.intro and not self.player:
            return 'intro'
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                if keys[pygame.K_RIGHT]:
                    self.rect.y -= 3.535
                    self.rect.x += 3.535
                    return 'right_up'
                elif keys[pygame.K_LEFT]:
                    self.rect.y -= 3.535
                    self.rect.x -= 3.535
                    return 'left_up'
                else:
                    self.rect.y -= 5
                return 'up'
            if keys[pygame.K_DOWN]:
                if keys[pygame.K_RIGHT]:
                    self.rect.y += 3.535
                    self.rect.x += 3.535
                    return 'right_down'
                elif keys[pygame.K_LEFT]:
                    self.rect.y += 3.535
                    self.rect.x -= 3.535
                    return 'left_down'
                else:
                    self.rect.y += 5
                return 'down'
            if keys[pygame.K_RIGHT]:
                self.rect.x += 5
                return 'right'
            if keys[pygame.K_LEFT]:
                self.rect.x -= 5
                return 'left'

    def update(self):
        if self.player and self.chosen:
            dir = self.player_input()
            self.animation_state(direction=dir)
        elif self.player:
            self.animation_state(direction='stand_list')
        elif self.intro:
            self.image = self.stand_list[0]

