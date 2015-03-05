import pygame
import grid


class Tetris:

    def __init__(self):
        self._running = True
        self._display_surface = None
        self._size = self.weight, self.height = 360, 720
        self._grid = grid.Grid()
        self._game_finished = (False, 0)
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
        self._grid.on_event(event)

    def on_loop(self):
        """The update function which computes changes in the game world"""
        self._grid.on_loop(self._game_finished)

    def on_render(self):
        """Renders the screen graphics"""
        self._display_surface.fill((self.BLACK))
        self._grid.on_render(self._display_surface)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() is False:
            self._running = False

        while self._running:
            self.on_loop()
            self.on_render()
            pygame.time.delay(1000/self.FPS)
        self.on_cleanup()


if __name__ == "__main__":
    tetris = Tetris()
    tetris.on_execute()
