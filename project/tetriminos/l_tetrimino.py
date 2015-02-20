import tetrimino


class L_tetrimino(tetrimino.Tetrimino):

    def load_image(self):
        return tetrimino.pygame.image.load('assets/tetris_light_blue.png')

    def get_up_shape(self):
        return [[0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0],
                [0, 1, 2, 1, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]]

    def get_right_shape(self):
        return [[0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 2, 0, 0],
                [0, 0, 1, 1, 0],
                [0, 0, 0, 0, 0]]

    def get_down_shape(self):
        return [[0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 1, 2, 1, 0],
                [0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0]]

    def get_left_shape(self):
        return [[0, 0, 0, 0, 0],
                [0, 1, 1, 0, 0],
                [0, 0, 2, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0]]
