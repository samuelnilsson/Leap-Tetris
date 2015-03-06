def enum(**enums):
    return type('Enum', (), enums)


import pygame
import grid
import menu


class Tetris:

    def __init__(self):
        self._running = True
        self._display_surface = None
        self._size = self.width, self.height = 360, 720
        self._grid = grid.Grid()
        self._menu = menu.Menu(self, self._running)
        self._state = self._menu
        self.FPS = 50
        self.BLACK = (0, 0, 0)
        self._switch_to_game = False

    def switch_state_to_game(self):
        self._switch_to_game = True

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
        self._state.on_event(event)

    def on_loop(self):
        """The update function which computes changes in the game world"""
        self._state.on_loop()

    def on_render(self):
        """Renders the screen graphics"""
        self._display_surface.fill((self.BLACK))
        self._state.on_render(self._display_surface)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() is False:
            self._running = False

        while self._running:
            if self._switch_to_game:
                self._state = self._grid
                self._switch_to_game = False
            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop()
            self.on_render()
            pygame.time.delay(1000 / self.FPS)

        self.on_cleanup()


if __name__ == "__main__":
    tetris = Tetris()
    tetris.on_execute()