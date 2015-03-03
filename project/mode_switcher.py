import pygame


class Mode_switcher:

    def __init__(self):
        self._leap_mode = False
        self._font = pygame.font.SysFont('Arial', 18)
        self.POSITION_X = 10
        self.POSITION_Y = 10
        self.WIDTH = 50
        self.HEIGHT = 25
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)

    def on_render(self, surface):
        button = pygame.Rect(self.POSITION_X, self.POSITION_Y,
                             self.WIDTH, self.HEIGHT)
        color = self.RED
        if self._leap_mode:
            color = self.GREEN
        pygame.draw.rect(surface, color, button)
        text_surface = self._font.render('Leap', True, (0, 0, 0))
        surface.blit(text_surface, (self.POSITION_X + 5, self.POSITION_Y))

    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            self.on_click_event(pos)

    def on_click_event(self, pos):
        (x, y) = pos
        on_button_x = x < self.POSITION_X + self.WIDTH and x > self.POSITION_X
        on_button_y = y < self.POSITION_Y + self.HEIGHT and y > self.POSITION_Y
        if on_button_x and on_button_y:
            self._leap_mode = not self._leap_mode
