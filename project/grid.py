import pygame


def enum(**enums):
    return type('Enum', (), enums)


Color = enum(GREEN=1, RED=2, YELLOW=3, PINK=4,
                          DARK_BLUE=5, LIGHT_BLUE=6, ORANGE=7)


class Block:

    def __init__(self, color):
        self.SIZE = 30
        self._image = pygame
        self._color = color

    def get_image(self):
        if self._color == Color.GREEN:
            return pygame.image.load('assets/tetris_green.png')
        elif self._color == Color.RED:
            return pygame.image.load('assets/tetris_red.png')
        elif self._color == Color.YELLOW:
            return pygame.image.load('assets/tetris_yellow.png')
        elif self._color == Color.PINK:
            return pygame.image.load('assets/tetris_pink.png')
        elif self._color == Color.DARK_BLUE:
            return pygame.image.load('assets/tetris_dark_blue.png')
        elif self._color == Color.LIGHT_BLUE:
            return pygame.image.load('assets/tetris_red.png')
        else:
            return pygame.image.load('assets/tetris_orange.png')


class Grid:

    def __init__(self):
        self._grid_structure = self.init_grid_structure()

    def init_grid_structure(self):
        """Returns a grid structure without blocks"""
        grid = []
        for column in range(0, 11):
            col = []
            for row in range(0, 23):
                col.append(None)
            grid.append(col)
        grid[5][5] = Block(Color.GREEN)
        return grid

    def on_render(self, surface):
        for column in range(0, 11):
            for row in range(0, 23):
                if self._grid_structure[column][row] is not None:
                    x_pos = column * self._grid_structure[column][row].SIZE
                    y_pos = row * self._grid_structure[column][row].SIZE
                    surface.blit(self._grid_structure[column][row].get_image(),
                                 (x_pos, y_pos))
