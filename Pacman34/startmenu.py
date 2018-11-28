import pygame
from settings import main_font_filename, logo_path, SIZE, BLACK, WHITE, BUTTON_STYLE, records_path, \
    developers_file_path, FULLSCREEN_DEFAULT
from button import Button
from math import floor
from random import shuffle


class StartMenu:
    def __init__(self):
        if FULLSCREEN_DEFAULT is not False:
            self.screen = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(SIZE)

        self.w_close = False
        self.new_game = False
        self.main_image = pygame.image.load(logo_path)
        self.main_image_rect = self.main_image.get_rect()
        self.button_font = pygame.font.Font(main_font_filename, 40)

        self.new_game_button = Button((SIZE[0] / 3, self.main_image_rect.height * 2,
                                       SIZE[0] / 3, self.main_image_rect.height / 2), BLACK,
                                      self.new_game_button_action, text='New Game', font=self.button_font,
                                      **BUTTON_STYLE)
        self.records_button = Button((SIZE[0] / 3, self.main_image_rect.height * 2.5,
                                      SIZE[0] / 3, self.main_image_rect.height / 2), BLACK,
                                     self.records_button_action, text='Records', font=self.button_font,
                                     **BUTTON_STYLE)
        self.developers_button = Button((SIZE[0] / 3, self.main_image_rect.height * 3,
                                         SIZE[0] / 3, self.main_image_rect.height / 2), BLACK,
                                        self.developers_button_action, text='Developers', font=self.button_font,
                                        **BUTTON_STYLE)
        self.exit_button = Button((SIZE[0] / 3, self.main_image_rect.height * 3.5,
                                   SIZE[0] / 3, self.main_image_rect.height / 2), BLACK,
                                  self.exit_button_action, text='Exit', font=self.button_font,
                                  **BUTTON_STYLE)

        self.set_image_parmaters()

    def main_loop(self):
        while not self.w_close and not self.new_game:
            self.process_events()
            self.draw()
        return self.new_game

    def process_events(self):
        events = pygame.event.get()
        for event in events:
            self.check_button_events(event)
            if event.type == pygame.QUIT:
                self.w_close = True

    def draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.main_image, self.main_image_rect)
        self.draw_buttons()
        pygame.display.flip()

    def set_image_parmaters(self):
        self.main_image_rect.center = (SIZE[0] / 2, self.main_image_rect.height)

    def check_button_events(self, event):
        self.new_game_button.check_event(event)
        self.records_button.check_event(event)
        self.developers_button.check_event(event)
        self.exit_button.check_event(event)

    def draw_buttons(self):
        self.new_game_button.update(self.screen)
        self.records_button.update(self.screen)
        self.developers_button.update(self.screen)
        self.exit_button.update(self.screen)

    def new_game_button_action(self):
        self.new_game = True

    def records_button_action(self):
        file = open(records_path)
        records = [(line.split()[0], line.split()[1]) for line in file]
        records.sort(key=lambda x: int(x[1]), reverse=True)
        DrawList(self.screen, records, "tuples").main_loop()
        file.close()

    def developers_button_action(self):
        file = open(developers_file_path)
        developers = [line[:-1] for line in file]
        shuffle(developers)
        DrawList(self.screen, developers, "strings").main_loop()
        file.close()

    def exit_button_action(self):
        self.w_close = True


class DrawList:
    def __init__(self, surf, list, type):
        self.type = type
        self.screen = surf
        self.end = False
        if self.type == "tuples":
            self.top = [i[0] + " " * (20 - len(i[0]) - len(i[1])) + i[1]
                        for i in (list[:10] if len(list) >= 10 else list)]
            self.rec_text = (pygame.font.Font(main_font_filename, 70)).render("Records", True, WHITE)
        if self.type == "strings":
            self.top = [" " * (len(name) // 2) + name + " " * ((int(floor(len(name) - 1.1)) // 2) + 1) for name in list]
            self.rec_text = (pygame.font.Font(main_font_filename, 70)).render("Developers", True, WHITE)
        self.back_button = Button((30, 30, 50, 50), BLACK, self.back_button_action, text='<',
                                  font=pygame.font.Font(main_font_filename, 60), **BUTTON_STYLE)
        self.list_font = pygame.font.Font(main_font_filename, 40)

    def main_loop(self):
        while not self.end:
            self.process_events()
            self.draw()

    def process_events(self):
        events = pygame.event.get()
        for event in events:
            self.back_button.check_event(event)
            if event.type == pygame.QUIT:
                exit()

    def draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.rec_text, ((SIZE[0] - self.rec_text.get_width()) // 2, 5))
        for i in range(len(self.top)):
            text = self.list_font.render(self.top[i], True, WHITE)
            self.screen.blit(text, ((SIZE[0] - text.get_width()) // 2, (i + 1) * SIZE[1] // (len(self.top) + 1)))
        self.back_button.update(self.screen)
        pygame.display.flip()

    def back_button_action(self):
        self.end = True
