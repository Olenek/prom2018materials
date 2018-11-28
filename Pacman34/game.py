from button import Button
from ghosts import *
from pacman import *
import time
from name_recording import GetName
import pattern_draw as pattern
from settings import BLACK, WHITE, RED, PINK, SIZE, BUTTON_STYLE, records_path, frightened_mode_duration, \
    part, maze_map_filename, pattern_map_filename, lives_image, main_font_filename, FULLSCREEN_DEFAULT
from gameover import GameOver
from cell import Cell


class Game:
    def __init__(self, level=1, player_name=""):
        if FULLSCREEN_DEFAULT is not False:
            self.screen = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(SIZE)
        # state
        self.w_close = False
        self.w_pause = False
        self.fullscreen = FULLSCREEN_DEFAULT
        self.image_counter = 0  # отвечает за изображение пакмана

        # objects
        self.field = []
        self.MAP_POS = []  # self.MAP_POS and self.MAP_SIZE is needed to center the GUI elements
        self.MAP_SIZE = []

        self.score = 0
        self.current_score = 0
        self.corn_counter = 0
        self.pacman = None
        self.ghosts = pygame.sprite.Group()

        self.fill_fields()
        self.__calculate_screen_size()
        self.spawn_entities()

        self.main_font = pygame.font.Font(main_font_filename, 20)
        self.minor_font = pygame.font.Font(main_font_filename, 16)
        self.lives_img = pygame.transform.scale(pygame.image.load(lives_image), (part, part))

        self.level = level
        self.player_name = player_name
        if self.level == 1 and not player_name:
            self.player_name = GetName().main_loop()

        self.start_time = time.time()
        self.next_mode = [int(time.time()), "scatter"]
        self.mode_turning_counter = 8
        self.start_pause_time = 0
        self.frightened_start_time = -1000
        self.frightened_points = 200

        self.button_exit = Button(
            (self.MAP_POS[0] + self.MAP_SIZE[0] - 100, 5, 100, 50), BLACK, self.button_action_exit,
            font=self.minor_font, text='Exit', **BUTTON_STYLE
        )  # кнопка выхода

        self.button_pause = Button(
            (self.MAP_POS[0] + self.MAP_SIZE[0] - 220, 5, 100, 50), BLACK, self.button_action_pause,
            font=self.minor_font, text='Pause', **BUTTON_STYLE
        )  # кнопка паузы

    def spawn_entities(self):
        # FIXME: spawn points is relative to the map structure
        self.pacman = Pacman(self.MAP_POS[0] + 13.5 * part, self.MAP_POS[1] + 23 * part, 2)
        self.ghosts.add(
            Blinky(self.MAP_POS[0] + 14 * part, self.MAP_POS[1] + 11 * part),
            Pinky(self.MAP_POS[0] + 12 * part, self.MAP_POS[1] + 13 * part),
            Inky(self.MAP_POS[0] + 14 * part, self.MAP_POS[1] + 13 * part),
            Clyde(self.MAP_POS[0] + 16 * part, self.MAP_POS[1] + 13 * part)
        )

    def kill_all_entities(self):
        for ghost in self.ghosts:
            ghost.kill()
        self.pacman.kill()

    def __calculate_screen_size(self):
        self.MAP_SIZE = [len(self.field) * part, len(self.field[0]) * part]
        self.MAP_POS = [(SIZE[0] - self.MAP_SIZE[0]) // 2, (SIZE[1] - self.MAP_SIZE[1]) // 2]

    def fill_fields(self):

        # Meaning of characters in map file:
        # '#' a wall
        # '.' a dot
        # '_' a void

        maze_map_file = open(maze_map_filename, "r")
        pattern_map_file = open(pattern_map_filename, "r")

        maze_map = [line.split() for line in maze_map_file]
        pattern_map = [line.split() for line in pattern_map_file]
        self.field = [[j for j in i] for i in maze_map]

        for i in range(len(self.field)):
            for j in range(len(self.field[0])):
                self.field[i][j] = Cell()
                self.field[i][j].type = maze_map[i][j]
                self.field[i][j].draw_pattern = pattern_map[i][j]

        self.field = [[self.field[j][i] for j in range(len(self.field))] for i in range(len(self.field[0]))]

        for i in range(len(self.field)):
            for j in range(len(self.field[0])):
                self.field[i][j].rect = pygame.Rect(i * part + (SIZE[0] - (len(maze_map) - 3) * part) // 2,
                                                    j * part + (SIZE[1] - (len(maze_map[0]) + 3) * part) // 2,
                                                    part, part)
                self.field[i][j].is_turn, self.field[i][j].possible_turns = self.turns(i, j)

        maze_map_file.close()
        pattern_map_file.close()

    def main_loop(self):
        while not self.w_close:
            self.process_events()
            if not self.w_close:
                self.game_logic()
            if not self.w_close:
                self.draw()
            pygame.time.wait(10)

    def process_events(self):
        if not self.w_pause:
            self.check_time_events()
        events = pygame.event.get()
        for event in events:
            self.button_pause.check_event(event)  # обновляем кнопки
            self.button_exit.check_event(event)
            if event.type == pygame.QUIT:
                self.record_score()
                self.w_close = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.fullscreen_toggle()
                elif event.key == pygame.K_p:
                    self.button_action_pause()
                elif not self.w_pause:
                    cell = self.pacman.get_cell()
                    self.pacman.move(self.MAP_POS, self.field[cell[0]][cell[1]], event.key)

    def game_logic(self):
        if not self.w_pause:
            self.pacman_shift()
            self.change_pacman_image()
            collides = pygame.sprite.spritecollide(self.pacman, self.ghosts, dokill=False)
            if collides:
                self.pacman_collides(collides)
            else:
                for ghost in self.ghosts:
                    self.ghost_shift(ghost)
            if self.corn_counter == 244:
                self.new_level()

    def frightened_mode_on(self):
        for ghost in self.ghosts:
            ghost.change_mode("frightened")
        self.next_mode[0] += frightened_mode_duration
        self.frightened_start_time = int(time.time())

    def frightened_mode_off(self):
        for ghost in self.ghosts:
            if self.next_mode[1] == "scatter":
                ghost.change_mode("chase")
            elif self.next_mode[1] == "chase":
                ghost.change_mode("scatter")
        self.frightened_start_time = -1000

    def check_time_events(self):
        now = int(time.time())
        if now == self.next_mode[0] and self.mode_turning_counter:
            for ghost in self.ghosts:
                ghost.change_mode(self.next_mode[1])
            if self.next_mode[1] == "scatter":
                self.next_mode[0] = now + 6
                self.next_mode[1] = "chase"
            elif self.next_mode[1] == "chase":
                self.next_mode[0] = now + 20
                self.next_mode[1] = "scatter"
            self.mode_turning_counter -= 1

        if now == int(self.frightened_start_time + frightened_mode_duration):
            self.frightened_mode_off()
        if now == int(self.frightened_start_time + frightened_mode_duration) - 1:
            self.change_ghosts_image()


    def game_over(self):
        gameover = GameOver(self.screen, self.MAP_POS, self.MAP_SIZE)
        return gameover.main_loop()

    def new_level(self):
        score = self.score
        pacman_lives = self.pacman.lives
        self.__init__(self.level + 1)
        self.score = score
        self.pacman.lives = pacman_lives

    def record_score(self):
        file = open(records_path, "a")
        file.write("\n" + self.player_name + " " + str(self.score))
        file.close()

    def pacman_collides(self, ghosts):
        for ghost in ghosts:
            if ghost.mode != "frightened":
                if self.pacman.lives == 0:
                    if self.game_over() == 'restart':
                        self.record_score()
                        self.__init__(player_name=self.player_name)
                    else:
                        self.record_score()
                        self.button_action_exit()

                else:
                    lives = self.pacman.lives - 1
                    self.kill_all_entities()
                    self.spawn_entities()
                    self.pacman.lives = lives
                    self.current_score = 0
                    self.next_mode = [int(time.time()) + 1, "scatter"]
                    self.mode_turning_counter = 8
                    for ghost in ghosts:
                        ghost.went_out = False
                pygame.time.delay(500)
                return
            else:
                ghost.rect.x, ghost.rect.y = ghost.start_pos
                ghost.direction = 1
                if self.next_mode[1] == "scatter":
                    ghost.change_mode("chase")
                elif self.next_mode[1] == "chase":
                    ghost.change_mode("scatter")
                ghost.went_out = False
                self.score += self.frightened_points
                if self.frightened_points != (2 ** len(self.ghosts)) * 100:
                    self.frightened_points *= 2
                else:
                    self.frightened_points = 200

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_field()
        self.pacman.draw(self.screen)
        for ghost in self.ghosts:
            ghost.draw(self.screen)

        self.draw_score()

        self.draw_lives()
        self.draw_buttons()

        pygame.display.flip()

    def draw_lives(self):
        for i in range(self.pacman.lives):
            self.screen.blit(self.lives_img, (self.MAP_POS[0] + i * part, self.MAP_POS[1] + self.MAP_SIZE[1]))

    def draw_buttons(self):
        self.button_exit.update(self.screen)  # обновляем кнопки
        self.button_pause.update(self.screen)

    def draw_field(self):
        for x in range(len(self.field)):
            for y in range(len(self.field[0])):
                if self.field[x][y].type == '#':
                    pattern.draw_wall(self.field, self.screen, self.MAP_POS, x, y)
                elif self.field[x][y].type == '.':
                    pygame.draw.circle(self.screen, WHITE, (self.MAP_POS[0] + x * part + part // 2,
                                                            self.MAP_POS[1] + y * part + part // 2), part // 8)
                elif self.field[x][y].type == 'o':
                    pygame.draw.circle(self.screen, PINK, (self.MAP_POS[0] + x * part + part // 2,
                                                           self.MAP_POS[1] + y * part + part // 2), part // 3)

    def draw_score(self):
        score = self.main_font.render(str(self.score), True, WHITE)
        player_one_text = self.main_font.render("1UP", True, WHITE)
        height = player_one_text.get_height()

        self.screen.blit(player_one_text, (self.MAP_POS[0], self.MAP_POS[1] - height * 2))
        self.screen.blit(score, (self.MAP_POS[0], self.MAP_POS[1] - height))

    def pacman_shift(self):
        cell = self.pacman.get_cell()
        self.pacman.move(self.MAP_POS, self.field[cell[0]][cell[1]])
        cell = self.pacman.get_cell()

        if self.field[cell[0]][cell[1]].type == '#':
            self.pacman.direction = (self.pacman.direction - 2) % 4
            self.pacman.move(self.MAP_POS)
            self.pacman.direction = (self.pacman.direction - 2) % 4
        if self.field[cell[0]][cell[1]].type == '.':
            self.corn_counter += 1
            self.score += 10
            self.current_score += 10
            self.field[cell[0]][cell[1]].type = '_'
        if self.field[cell[0]][cell[1]].type == 'o':
            self.corn_counter += 1
            self.score += 50
            self.current_score += 50
            self.field[cell[0]][cell[1]].type = '_'
            self.frightened_mode_on()
        if self.field[cell[0]][cell[1]].type == '8':
            self.pacman.teleportation(self.MAP_POS, self.MAP_SIZE)

    def ghost_shift(self, ghost):
        ghost.move(self.MAP_POS)
        cell = ghost.get_cell()

        if not ghost.went_out and self.current_score >= ghost.go_out_score:
            ghost.go_out(self.MAP_POS[0] + 14 * part, self.MAP_POS[1] + 11 * part)
            if (ghost.rect.x == self.MAP_POS[0] + 14 * part) and (ghost.rect.y == self.MAP_POS[1] + 11 * part):
                ghost.went_out = True
        else:
            if self.field[cell[0]][cell[1]].type == '#':
                ghost.change_direction()
                ghost.move(self.MAP_POS)
                ghost.change_direction()
            if self.field[cell[0]][cell[1]].type == '8':
                ghost.teleportation(self.MAP_POS, self.MAP_SIZE)
            if self.field[cell[0]][cell[1]].is_turn and ghost.rect == self.field[cell[0]][cell[1]].rect:
                if ghost.name != "Inky":
                    ghost.choose_turn(self.field[cell[0]][cell[1]].possible_turns, self.pacman)
                else:
                    ghost.choose_turn(self.field[cell[0]][cell[1]].possible_turns, self.pacman, list(self.ghosts)[0])

    def change_pacman_image(self):
        if self.image_counter == 4:
            self.image_counter = 0
            self.pacman.update()
        self.image_counter += 1

    def change_ghosts_image(self):
        if self.image_counter == 4:
            for ghost in self.ghosts:
                if ghost.mode == "frightened":
                    ghost.change_frightened_image()

    def button_action_pause(self):  # функция кнопки паузы
        if self.w_pause:
            delay = int(time.time()) - self.start_pause_time
            self.next_mode[0] += delay
            self.frightened_start_time += delay
            self.w_pause = False
            self.button_pause.text = self.button_pause.font.render("Pause", True, WHITE)
            self.button_pause.hover_text = self.button_pause.font.render("Pause", True, RED)
        else:
            self.start_pause_time = int(time.time())
            self.w_pause = True
            self.button_pause.text = self.button_pause.font.render("Paused", True, RED)
            self.button_pause.hover_text = self.button_pause.font.render("Paused", True, RED)

    def button_action_exit(self):  # функция кнопки выхода
        self.w_close = True

    def turns(self, x, y):
        if x == 0 or y == 0 or x == len(self.field) - 1 or y == len(self.field[0]) - 1:
            return False, [False] * 4

        pos_turns = [self.field[x][y - 1].type != '#', self.field[x + 1][y].type != '#',
                     self.field[x][y + 1].type != '#', self.field[x - 1][y].type != '#']

        if (pos_turns[1] and pos_turns[3] and not pos_turns[0] and not pos_turns[2]) or \
                (not pos_turns[1] and not pos_turns[3] and pos_turns[0] and pos_turns[2]) or self.field[x][
            y].type == '#':
            return False, pos_turns
        return True, pos_turns

    def get_collides(self):
        ans = []
        for ghost in self.ghosts:
            if ghost.center == self.pacman.center:
                ans.append(ghost)
        return ans

    def fullscreen_toggle(self):
        if self.fullscreen:
            self.screen = pygame.display.set_mode(SIZE)
        else:
            self.screen = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
        self.fullscreen = not self.fullscreen
