import pygame
import math


class MenuItem:

    def __init__(self, name, execute):
        self._name = name
        self.execute = execute
        self._button_color = (192, 192, 192)
        self._button_edge_color = (120, 120, 120)
        self._position = 0
        self._click = (False, (0, 0))
        self._mouse_movement = (False, (0, 0))

    def on_render(self, surface, position):
        self._position = position
        outer_radius = 120
        inner_radius = 100
        if self._click[0] is True and self.distance(position, self._mouse_movement[1]) < outer_radius:
            self.execute()
        elif self._mouse_movement[0] is True and self.distance(position, self._mouse_movement[1]) < outer_radius:
            inner_radius = 115
            outer_radius = 130
        pygame.draw.circle(surface, self._button_edge_color, position, outer_radius)
        pygame.draw.circle(surface, self._button_color, position, inner_radius)
        font = pygame.font.SysFont('Arial', 70)
        text_surface = font.render(self._name, True, (120, 120, 120))
        surface.blit(text_surface, (position[0] - text_surface.get_width() / 2, position[1] - 35))


    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            self._click = (True, pos)
        elif event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            self._mouse_movement = (True, pos)

    def distance(self, position1, position2):
        return math.sqrt(abs(position2[1] - position1[1])**2 + abs(position2[0] - position1[0])**2)


class Menu:

    def __init__(self, main, running):
        self._menu_items = self.initialize_menu()
        self._main = main

    def initialize_menu(self):
        def play_execute():
            self._main.switch_state_to_game()
        def quit_execute():
            self._main._running = False
        play = MenuItem('Play', play_execute)
        quit = MenuItem('Quit', quit_execute)
        return [play, quit]

    def on_render(self, surface):
        self.render_background(surface)
        pos = 150
        for menu_item in self._menu_items:
            menu_item.on_render(surface, (180, pos))
            pos += 400

    def on_loop(self):
        return (False, 0)

    def on_event(self, event):
        for menu_item in self._menu_items:
            menu_item.on_event(event)

    def render_background(self, surface):
        background_image = pygame.image.load('assets/background.png')
        surface.blit(background_image, (0, 0))
