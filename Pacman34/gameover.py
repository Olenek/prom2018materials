import pygame
from button import Button
from settings import SIZE, BLACK, WHITE, BUTTON_STYLE, main_font_filename


class GameOver:
    def __init__(self, surf, map_pos, map_size):

        self.is_chosen = False

        self.result = None
        self.map_pos = map_pos
        self.map_size = map_size
        self.button_font = pygame.font.Font(main_font_filename, 40)
        self.screen = surf
        self.text_surface = None
        self.text_rect = None
        self.set_text_surface()
        self.button_restart = Button((self.map_pos[0] * 3 / 4, SIZE[1] * 5 / 8, map_size[0] / 2, map_size[1] / 4),
                                     BLACK, self.button_restart_action, text='Restart', font=self.button_font,
                                     **BUTTON_STYLE)
        self.button_exit = Button((self.map_pos[0] * 5 / 4 + self.map_size[0] / 2, SIZE[1] * 5 / 8,
                                   map_size[0] / 2, map_size[1] / 4), BLACK, self.button_exit_action,
                                  text='Exit', font=self.button_font, **BUTTON_STYLE)

    def set_text_surface(self):
        large_text = pygame.font.Font(main_font_filename, 115)
        self.text_surface = large_text.render("Game Over", True, WHITE)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = ((SIZE[0] / 2), (SIZE[1] / 2) - self.text_rect.height)

    def main_loop(self):
        while not self.is_chosen:
            self.process_events()
            self.draw()
            pygame.time.wait(20)
        return self.result

    def process_events(self):
        events = pygame.event.get()
        for event in events:
            self.button_exit.check_event(event)
            self.button_restart.check_event(event)
            if event.type == pygame.QUIT:
                self.is_chosen = True
                self.result = "exit"

    def draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.text_surface, self.text_rect)
        self.button_restart.update(self.screen)
        self.button_exit.update(self.screen)
        pygame.display.flip()

    def button_exit_action(self):
        self.result = "exit"
        self.is_chosen = True

    def button_restart_action(self):
        self.result = "restart"
        self.is_chosen = True
