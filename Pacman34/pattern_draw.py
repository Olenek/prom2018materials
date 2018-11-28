import pygame
from math import pi
from settings import part, BLUE, WOODEN

'''
vertical |
horizontal -
corner1 |_       _
        corner2 |
corner3 _|      _
        corner4  |
'''


def draw_gate(surf, x, y):
    pygame.draw.line(surf, WOODEN, (x - 1, y + part // 2), (x + part + 1, y + part // 2))


def draw_vertical(surf, x, y):
    pygame.draw.line(surf, BLUE, (x + part // 2, y - 1), (x + part // 2, y + part + 1))


def draw_horizontal(surf, x, y):
    pygame.draw.line(surf, BLUE, (x - 1, y + part // 2), (x + part + 1, y + part // 2))


def draw_corner1(surf, x, y):
    pygame.draw.arc(surf, BLUE, [x + part // 2, y - part // 2, part, part], pi, 1.5 * pi)


def draw_corner2(surf, x, y):
    pygame.draw.arc(surf, BLUE, [x + part // 2, y + part // 2, part, part], 0.5 * pi, pi)


def draw_corner3(surf, x, y):
    pygame.draw.arc(surf, BLUE, [x - part // 2, y - part // 2, part, part], 1.5 * pi, 2 * pi)


def draw_corner4(surf, x, y):
    pygame.draw.arc(surf, BLUE, [x - part // 2, y + part // 2, part, part], 0, 0.5 * pi)


def draw_wall(field, screen, map_pos, x, y):
    if field[x][y].draw_pattern == "vertical":
        draw_vertical(screen, map_pos[0] + x * part, map_pos[1] + y * part)
    elif field[x][y].draw_pattern == "horizontal":
        draw_horizontal(screen, map_pos[0] + x * part, map_pos[1] + y * part)
    elif field[x][y].draw_pattern == "corner1":
        draw_corner1(screen, map_pos[0] + x * part, map_pos[1] + y * part)
    elif field[x][y].draw_pattern == "corner2":
        draw_corner2(screen, map_pos[0] + x * part, map_pos[1] + y * part)
    elif field[x][y].draw_pattern == "corner3":
        draw_corner3(screen, map_pos[0] + x * part, map_pos[1] + y * part)
    elif field[x][y].draw_pattern == "corner4":
        draw_corner4(screen, map_pos[0] + x * part, map_pos[1] + y * part)
    elif field[x][y].draw_pattern == "@":
        draw_gate(screen, map_pos[0] + x * part, map_pos[1] + y * part)
