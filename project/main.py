import pygame
from tetriminos import l_tetrimino


class Tetris:

    def __init__(self):
        self._running = True
        self._display_surface = None
        self._size = self.weight, self.height = 360, 720
        self._currentblock = l_tetrimino.L_tetrimino()
        self.FPS = 50
        self.BLACK = (0, 0, 0)

    def on_init(self):
        pygame.init()
        self._display_surface = pygame.display.set_mode(
            self._size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("Leap Tetris!")
        self._running = True

    def on_event(self, event):
        """Proceeds events such as pressed keys, mouse movements
        (or Leap input)"""
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self._currentblock.rotate_right()
            if event.key == pygame.K_RIGHT:
                self._currentblock.move_right()
            if event.key == pygame.K_LEFT:
                self._currentblock.move_left()

    def on_loop(self):
        """The update function which computes changes in the game world"""
        self._currentblock.on_loop()

    def on_render(self):
        """Renders the screen graphics"""
        self._display_surface.fill((self.BLACK))
        self._currentblock.on_render(self._display_surface)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() is False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            pygame.time.delay(1000/self.FPS)
        self.on_cleanup()


if __name__ == "__main__":
    tetris = Tetris()
    tetris.on_execute()
