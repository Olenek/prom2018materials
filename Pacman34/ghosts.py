import pygame
from settings import part
from random import randint


class Ghost(pygame.sprite.Sprite):
    image_path = "images/ghost.png"

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(self.image_path), (part, part))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1
        self.speed = 2
        self.mode = "chase"
        self.frightened_image_path = "images/frightened"
        self.frightened_counter = 0
        self.aim = 0, 0
        self.scatter_aim = 0, 0
        self.center = -1, -1
        self.out_going = False
        self.go_out_score = 0
        self.went_out = False

    def draw(self, surf):
        surf.blit(self.image, self.rect)

    def choose_turn(self, pos_turns, pacman):
        if self.mode == "frightenned":
            self.direction = self.choice_by_fear(pos_turns)
        elif self.mode == "scatter":
            self.aim = self.scatter_aim
            self.sane_decision(pos_turns)
        else:
            self.aim_choice(pacman)
            self.sane_decision(pos_turns)

    def move(self, map_pos):
        if self.direction == 0:
            self.rect.y -= self.speed
        elif self.direction == 1:
            self.rect.x += self.speed
        elif self.direction == 2:
            self.rect.y += self.speed
        elif self.direction == 3:
            self.rect.x -= self.speed
        self.center = (self.rect.x + part // 2 - map_pos[0], self.rect.y + part // 2 - map_pos[1])

    def sane_decision(self, pos_turns):
        s_cell = self.get_cell()
        min_dist = [1000, -1]
        if pos_turns[0] and self.direction != 2:
            n_cell = s_cell[0], s_cell[1] - 1
            dist = (n_cell[0] - self.aim[0]) ** 2 + (n_cell[1] - self.aim[1]) ** 2
            if min_dist[0] >= dist:
                min_dist[0] = dist
                min_dist[1] = 0
        if pos_turns[1] and self.direction != 3:
            n_cell = s_cell[0] + 1, s_cell[1]
            dist = (n_cell[0] - self.aim[0]) ** 2 + (n_cell[1] - self.aim[1]) ** 2
            if min_dist[0] >= dist:
                min_dist[0] = dist
                min_dist[1] = 1
        if pos_turns[2] and self.direction != 0:
            n_cell = s_cell[0], s_cell[1] + 1
            dist = (n_cell[0] - self.aim[0]) ** 2 + (n_cell[1] - self.aim[1]) ** 2
            if min_dist[0] >= dist:
                min_dist[0] = dist
                min_dist[1] = 2
        if pos_turns[3] and self.direction != 1:
            n_cell = s_cell[0] - 1, s_cell[1]
            dist = (n_cell[0] - self.aim[0]) ** 2 + (n_cell[1] - self.aim[1]) ** 2
            if min_dist[0] >= dist:
                min_dist[0] = dist
                min_dist[1] = 3
        self.direction = min_dist[1]

    def choice_by_fear(self, possible_turns):
        ans = randint(0, 3)
        while possible_turns[ans] and ans != self.direction:
            ans = randint(0, 3)
        return ans

    def change_direction(self):  # используется при переключении режимов (в game)
        self.direction = (self.direction + 2) % 4

    def change_frightened_image(self):
        self.frightened_counter = (self.frightened_counter + 1) % 2
        self.image = pygame.transform.scale(pygame.image.load(self.frightened_image_path +
                                                                   str(self.frightened_counter) + ".png"), (part, part))

    def aim_choice(self, pacman):  # оставить pass, будет переопределенно в наследуемых классах
        pass

    def get_cell(self):
        return [self.center[0] // part, self.center[1] // part]

    def teleportation(self, map_pos, map_size):
        if self.get_cell()[0] == 0 and self.direction == 3:
            self.rect.x = map_size[0] + map_pos[0] - part
            pass
        elif self.get_cell()[0] == map_size[0] // part - 1 and self.direction == 1:
            self.rect.x = map_pos[0]
        self.center = (self.rect.x + part // 2 - map_pos[0], self.rect.y + part // 2 - map_pos[1])

    def change_mode(self, mode):
        if mode != self.mode:
            self.change_direction()
            if mode == "frightened":
                self.speed = 1
                self.image = pygame.transform.scale(pygame.image.load(self.frightened_image_path +
                                                                      str(self.frightened_counter) + ".png"),
                                                    (part, part))
            else:
                self.image = pygame.transform.scale(pygame.image.load(self.image_path), (part, part))
                self.speed = 2
            self.mode = mode

    def go_out(self, X, Y):
        if self.rect.x <= X - 1:
            self.direction = 1
        elif self.rect.x >= X + 1:
            self.direction = 3
        elif self.rect.y > Y:
            self.direction = 0
        else:
            self.direction = 1


class Blinky(Ghost):
    def __init__(self, x, y):
        self.image_path = "images/ghost1.png"
        super().__init__(x, y)
        self.name = "Blinky"
        self.scatter_aim = 25, -2
        self.start_pos = x, y
        self.go_out_score = 0

    def aim_choice(self, pacman):
        self.aim = pacman.get_cell()


class Pinky(Ghost):
    def __init__(self, x, y):
        self.image_path = "images/ghost2.png"
        super().__init__(x, y)
        self.name = "Pinky"
        self.scatter_aim = 2, -2
        self.start_pos = x, y
        self.go_out_score = 80

    def aim_choice(self, pacman):
        cell = pacman.get_cell()
        if pacman.direction == 0:
            cell[1] -= 4
        elif pacman.direction == 1:
            cell[0] += 4
        elif pacman.direction == 2:
            cell[1] += 4
        elif pacman.direction == 3:
            cell[0] -= 4
        self.aim = cell


class Inky(Ghost):
    def __init__(self, x, y):
        self.image_path = "images/ghost3.png"
        super().__init__(x, y)
        self.name = "Inky"
        self.scatter_aim = 27, 32
        self.start_pos = x, y
        self.go_out_score = 130

    def choose_turn(self, pos_turns, pacman, blinky):
        if self.mode == "frightenned":
            self.direction = self.choice_by_fear(pos_turns)
        elif self.mode == "scatter":
            self.aim = self.scatter_aim
            self.sane_decision(pos_turns)
        else:
            self.aim_choice(pacman, blinky)
            self.sane_decision(pos_turns)

    def aim_choice(self, pacman, blinky):
        p_cell = pacman.get_cell()
        b_cell = blinky.get_cell()
        s_cell = self.get_cell()
        if pacman.direction == 0:
            p_cell[1] -= 2;
        elif pacman.direction == 1:
            p_cell[0] += 2
        elif pacman.direction == 2:
            p_cell[1] += 2
        elif pacman.direction == 3:
            p_cell[0] -= 2
        s_cell[0] += (p_cell[0] - b_cell[0])
        s_cell[1] += (p_cell[1] - b_cell[1])
        self.aim = s_cell


class Clyde(Ghost):
    def __init__(self, x, y):
        self.image_path = "images/ghost4.png"
        super().__init__(x, y)
        self.name = "Clyde"
        self.scatter_aim = 0, 32
        self.start_pos = x, y
        self.go_out_score = 180

    def aim_choice(self, pacman):
        p_cell = pacman.get_cell()
        s_cell = self.get_cell()
        dist = (s_cell[0] - p_cell[0])**2 + (s_cell[1] - p_cell[1])**2
        if dist > 64:
            self.aim = p_cell
        else:
            self.aim = self.scatter_aim
