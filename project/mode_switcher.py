import pygame


class ModeSwitcher:

    def __init__(self, click_handler):
        self._click_handler = click_handler
        self._leap_mode = False
        self._font = pygame.font.SysFont('Arial', 18)
        self._is_mouse_over_button = False
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
        if self._is_mouse_over_button:
            color = (255, 100, 100)
        if self._leap_mode:
            color = self.GREEN
            if self._is_mouse_over_button:
                color = (150, 255, 150)
        pygame.draw.rect(surface, color, button)
        text_surface = self._font.render('Leap', True, (0, 0, 0))
        surface.blit(text_surface, (self.POSITION_X + 5, self.POSITION_Y))

    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            self.on_click_event(pos)
        elif event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            self.on_mouse_movement(pos)

    def on_click_event(self, pos):
        if self.is_position_on_button(pos):
            self._leap_mode = not self._leap_mode
            self._click_handler()

    def on_mouse_movement(self, pos):
        self._is_mouse_over_button = self.is_position_on_button(pos)

    def is_position_on_button(self, pos):
        (x, y) = pos
        on_button_x = x < self.POSITION_X + self.WIDTH and x > self.POSITION_X
        on_button_y = y < self.POSITION_Y + self.HEIGHT and y > self.POSITION_Y
        return on_button_x and on_button_y
