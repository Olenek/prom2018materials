#!/usr/bin/env python3
import pygame
from sys import exit
from game import Game
from startmenu import StartMenu

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    if StartMenu().main_loop():
        g = Game()
        g.main_loop()
    exit()
