import pygame


class Tetris:

    def __init__(self):
        self._running = True
        self._display_surface = None
        self._size = self.weight, self.height = 400, 600
        self._tetris_image = pygame.image.load('assets/tetris.png')

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

    def on_loop(self):
        """The update function which computes changes in the game world"""
        pass

    def on_render(self):
        """Renders the screen graphics"""
        self._display_surface.blit(self._tetris_image, (0, 0))
        pygame.display.flip()
        pass

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
        self.on_cleanup()


if __name__ == "__main__":
    tetris = Tetris()
    tetris.on_execute()