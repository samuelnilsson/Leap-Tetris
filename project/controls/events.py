import pygame
import tetris


Events = tetris.enum(
    DOWN_FASTER     = pygame.USEREVENT + 0,
    DOWN_NORMAL     = pygame.USEREVENT + 1,
    MOVE_LEFT       = pygame.USEREVENT + 2,
    MOVE_RIGHT      = pygame.USEREVENT + 3,
    PAUSE    		= pygame.USEREVENT + 4,
    PAUSE_TOGGLE    = pygame.USEREVENT + 5,
    PLAY    		= pygame.USEREVENT + 6,
    ROTATE_RIGHT    = pygame.USEREVENT + 7,
    ROTATE_LEFT     = pygame.USEREVENT + 8,
)
