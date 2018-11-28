import pygame
from settings import SIZE, main_font_filename, BLACK, WHITE, logo_path, FULLSCREEN_DEFAULT
from string import ascii_letters, digits


class GetName:
    def __init__(self):
        if FULLSCREEN_DEFAULT is not False:
            self.screen = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(SIZE)

        self.w_close = False
        self.is_enter = False

        self.main_image = pygame.image.load(logo_path)
        self.main_image_rect = self.main_image.get_rect()

        self.text_rect = None
        self.text_surface = None
        self.name_rect = None
        self.name_surface = None
        self.colon_rect = None
        self.colon_surface = None

        self.name = ""
        self.text_font = pygame.font.Font(main_font_filename, 75)
        self.name_font = pygame.font.Font(main_font_filename, 90)

        self.loop_counter = 0

        self.set_text_surface()
        self.set_image_parmaters()

    def main_loop(self):
        while not self.w_close and not self.is_enter:
            self.process_events()
            self.set_name_surface()
            self.draw()
            self.loop_counter = (self.loop_counter + 1) % 20
            pygame.time.wait(50)

        return self.name

    def process_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.w_close = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and self.name:
                    self.name = self.name[:-1]
                elif event.key == pygame.K_RETURN:
                    if not self.name:
                        self.name = "Unknown"
                    self.is_enter = True
                elif chr(event.key) in ascii_letters or chr(event.key) in digits:
                    mods = pygame.key.get_mods()
                    key = chr(event.key)
                    if mods & pygame.KMOD_SHIFT:
                        key = key.upper()
                    if len(self.name) < 14:
                        self.name += key

    def draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.main_image, self.main_image_rect)
        self.screen.blit(self.text_surface, self.text_rect)
        self.screen.blit(self.name_surface, self.name_rect)
        if 0 < self.loop_counter < 4:
            self.screen.blit(self.colon_surface, self.colon_rect)
        pygame.display.flip()

    def set_name_surface(self):
        self.name_surface = self.name_font.render(self.name, True, WHITE)
        self.name_rect = self.name_surface.get_rect()
        self.name_rect.center = ((SIZE[0] / 2), (SIZE[1] * 7 / 9) - self.name_rect.height)

    def set_text_surface(self):
        self.text_surface = self.text_font.render("Enter your name", True, WHITE)
        self.colon_surface = self.text_font.render(":", True, WHITE)
        self.colon_rect = self.colon_surface.get_rect()
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = ((SIZE[0] / 2), (SIZE[1] * 5 / 9) - self.text_rect.height)
        self.colon_rect.center = (self.text_rect.x + self.text_rect.width + self.colon_rect.width / 2,
                                  (SIZE[1] * 5 / 9) - self.text_rect.height + 10)

    def set_image_parmaters(self):
        self.main_image_rect.center = (SIZE[0] / 2, self.main_image_rect.height * 3 / 4)
