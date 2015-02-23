from tetriminos import (i_tetrimino, j_tetrimino, l_tetrimino, o_tetrimino,
                        s_tetrimino, t_tetrimino, z_tetrimino)
from random import randint


class Grid:

    def __init__(self):
        self.HEIGHT = 24
        self.WIDTH = 12
        self._grid_structure = self.init_grid_structure()
        self._current_tetrimino = self.new_tetrimino()

    def init_grid_structure(self):
        """Returns a grid structure without blocks"""
        grid = []
        for column in range(0, self.WIDTH):
            col = []
            for row in range(0, self.HEIGHT):
                col.append(None)
            grid.append(col)
        return grid

    def on_render(self, surface):
        for column in range(0, self.WIDTH):
            for row in range(0, self.HEIGHT):
                if self._grid_structure[column][row] is not None:
                    x_pos = column * self._grid_structure[column][row].SIZE
                    y_pos = row * self._grid_structure[column][row].SIZE
                    surface.blit(self._grid_structure[column][row].get_image(),
                                 (x_pos, y_pos))
        self._current_tetrimino.on_render(surface)

    def on_loop(self):
        if self._current_tetrimino.is_termino_down(self._grid_structure):
            self._current_tetrimino.attach_current_tetrimino_to_grid(
                self._grid_structure)
            self._current_tetrimino = self.new_tetrimino()
            self.remove_full_rows()
        else:
            self._current_tetrimino.on_loop()

    def on_event(self, event):
        self._current_tetrimino.on_event(event, self._grid_structure)

    def new_tetrimino(self):
        """Returns a randomly generated tetrimino"""
        random_brick = randint(0, 6)
        if random_brick is 0:
            return i_tetrimino.I_tetrimino(self)
        if random_brick is 1:
            return j_tetrimino.J_tetrimino(self)
        if random_brick is 2:
            return l_tetrimino.L_tetrimino(self)
        if random_brick is 3:
            return o_tetrimino.O_tetrimino(self)
        if random_brick is 4:
            return s_tetrimino.S_tetrimino(self)
        if random_brick is 5:
            return t_tetrimino.T_tetrimino(self)
        if random_brick is 6:
            return z_tetrimino.Z_tetrimino(self)

    def remove_full_rows(self):
        for y in range(0, self.HEIGHT):
            row_full = True
            for x in range(0, self.WIDTH):
                if self._grid_structure[x][y] is None:
                    row_full = False
            if row_full:
                self.remove_row(y)

    def remove_row(self, row):
        print(row)
        for x in range(0, self.WIDTH):
            self._grid_structure[x][row] = None
        for tmp in range(0, row - 1):
            'It iterates from the bottom to the top'
            y = row - 1 - tmp
            for x in range(0, self.WIDTH):
                self._grid_structure[x][y + 1] = self._grid_structure[x][y]
                self._grid_structure[x][y] = None
