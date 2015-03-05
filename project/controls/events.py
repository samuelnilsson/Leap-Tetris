import pygame
import tetris


Events = tetris.enum(
	DOWN_FASTER		= pygame.USEREVENT + 1,
	DOWN_NORMAL		= pygame.USEREVENT + 2,
	MOVE_LEFT 		= pygame.USEREVENT + 3,
	MOVE_RIGHT		= pygame.USEREVENT + 4,
	PAUSE_TOGGLE 	= pygame.USEREVENT + 5,
	ROTATE_LEFT		= pygame.USEREVENT + 6,
	ROTATE_RIGHT	= pygame.USEREVENT + 7
)