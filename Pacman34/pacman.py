import pygame
from cell import Cell
from settings import part, pacman_lives, pacman_images_total


class Pacman(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        """
        x - абсцисса пакмана, y - ордината пакмана, speed - скорость пакмана
        direction - направление движения пакмана: 0 - вверх, 1 - вправо, 2 - вниз, 3 - влево.
        """
        super().__init__()
        self.is_alive = True
        self.speed = speed
        self.direction = 1
        self.next_direction = -1
        self.images = []
        self.image_index = 0

        for i in range(pacman_images_total):
            self.images.append(pygame.image.load("images/pacman{count}.png".format(count=i)))

        self.update()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.center = (-1, -1)
        self.lives = pacman_lives

    def update(self):
        self.image = self.get_next_image()
        self.image = pygame.transform.scale(self.image, (part, part))

    def get_next_image(self):
        self.image_index = (self.image_index + 1) % pacman_images_total
        return self.images[self.image_index]

    def move(self, map_pos, cell=Cell(), key=42):
        key = chr(key)
        if key == 'w':
            self.next_direction = 0
        elif key == 's':
            self.next_direction = 2
        elif key == 'a':
            self.next_direction = 3
        elif key == 'd':
            self.next_direction = 1
        if self.next_direction == (self.direction + 2) % 4:
            self.direction = self.next_direction
            self.next_direction = -1
        if cell.is_turn and self.next_direction != -1 and \
                cell.possible_turns[self.next_direction]:  # and self.rect == cell.rect:
            self.direction = self.next_direction
            self.next_direction = -1
        if key == "*":  # * = 42
            if self.direction == 0:
                self.rect.y -= self.speed
            elif self.direction == 1:
                self.rect.x += self.speed
            elif self.direction == 2:
                self.rect.y += self.speed
            elif self.direction == 3:
                self.rect.x -= self.speed
        self.center = (self.rect.x + part // 2 - map_pos[0], self.rect.y + part // 2 - map_pos[1])

    def draw(self, surface):
        if self.direction == 0:
            surface.blit(pygame.transform.rotate(self.image, 90), self.rect)
        elif self.direction == 1:
            surface.blit(self.image, self.rect)
        elif self.direction == 2:
            surface.blit(pygame.transform.rotate(self.image, -90), self.rect)
        else:
            surface.blit(pygame.transform.flip(self.image, True, False), self.rect)

    def get_cell(self):
        return [self.center[0] // part, self.center[1] // part]

    def teleportation(self, map_pos, map_size):
        if self.get_cell()[0] == 0 and self.direction == 3:
            self.rect.x = map_size[0] + map_pos[0] - part
            pass
        elif self.get_cell()[0] == map_size[0] // part - 1 and self.direction == 1:
            self.rect.x = map_pos[0]
        self.center = (self.rect.x + part // 2 - map_pos[0], self.rect.y + part // 2 - map_pos[1])
