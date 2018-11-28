SIZE = (WIDTH, HEIGHT) = (1280, 720)  # Размеры экрана
FULLSCREEN_DEFAULT = False
part = 20  # размер ячейки экрана
level_hard = 1  # начальный уровень сложности, от него зависит скорость привидения, увеличивается с прохождением
# каждого следующего уровня (это надо написать)
pacman_lives = 3
pacman_images_total = 3
frightened_mode_duration = 7

maze_map_filename = "map/maze.txt"
pattern_map_filename = "map/maze_pattern.txt"
lives_image = "images/pacman0.png"
main_font_filename = "fonts/PressStart2P-Regular.ttf"
logo_path = "images/logo.png"
records_path = "records.txt"
developers_file_path = "developers.txt"

RED = (255, 0, 0)  # цвета
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 180, 0)
PINK = (255, 185, 175)
WOODEN = (255, 128, 0)

BUTTON_STYLE = {  # стиль кнопки
    "hover_color": BLACK,
    "hover_font_color": RED,
}
