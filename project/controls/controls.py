import sys
import os
import inspect
import pygame
from events import Events

from sys import platform as _platform

if _platform == "linux" or _platform == "linux2":
    src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
    arch_dir = '../lib/x64/' if sys.maxsize > 2 ** 32 else '../lib/x86/'
    sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))
    import Leap
else:
    sys.path.insert(0, "lib")
    import Leap

# from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture


class BaseControls:     # TODO: Make this abstract?
    def _post_event(self, event):
        if event is not None:
            pygame.event.post(pygame.event.Event(event))

    def on_event(self, event):
        return


class KeyboardControls(BaseControls):
    def __init__(self):
        self._eventMap = {
            pygame.KEYDOWN: {
                pygame.K_UP: Events.ROTATE_RIGHT,
                pygame.K_RIGHT: Events.MOVE_RIGHT,
                pygame.K_LEFT: Events.MOVE_LEFT,
                pygame.K_DOWN: Events.DOWN_FASTER
            },
            pygame.KEYUP: {
                pygame.K_DOWN: Events.DOWN_NORMAL,
                pygame.K_p: Events.PAUSE_TOGGLE
            }
        }

    def on_event(self, event):
        self._post_event(self._generate_event(event))

    def _generate_event(self, pygame_event):
        try:
            eventlist = self._eventMap.get(pygame_event.type, None)
            event = eventlist.get(pygame_event.key, None)
            return event
        except:
            return None


class LeapControls(Leap.Listener, BaseControls):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def __init__(self):
        Leap.Listener.__init__(self)
        self._controller = Leap.Controller()
        self._controller.add_listener(self)
        self._safezone_width = 80
        self._hasHands = False
        self.previous_frame = None
        self.move_timestamp = 0
        self.rotate_timestamp = 0

    def _moveinterval(self, x):
        return 2000 * abs(x)

    def _rotateinterval(self, palm_direction):
        # print "%s\r" % palm_direction.normalized
        x_angle = abs(palm_direction.x)
        millis_base = 800   # Minimum rotation interval in millis
        interval = millis_base * 1000 * (2 - x_angle)
        return interval

    def _movesideways(self):
        x = self._hand.palm_position.x
        if x < -(self._safezone_width / 2):
            if self._frame.timestamp - self.move_timestamp > self._moveinterval(x):
                self._post_event(Events.MOVE_LEFT)
                self.move_timestamp = self._frame.timestamp
        elif x > self._safezone_width / 2:
            if self._frame.timestamp - self.move_timestamp > self._moveinterval(x):
                self._post_event(Events.MOVE_RIGHT)
                self.move_timestamp = self._frame.timestamp

    def _should_rotate(self, palm_direction):
        since_rotate = self._frame.timestamp - self.rotate_timestamp
        not_too_fast = since_rotate > self._rotateinterval(palm_direction)
        enough_angle = 0.75 <= abs(palm_direction.normalized.x)

        return not_too_fast and enough_angle

    def _rotate(self):
        palm_direction = self._hand.palm_normal.normalized

        if self._should_rotate(palm_direction):
            self._post_event(Events.ROTATE_RIGHT)
            self.rotate_timestamp = self._frame.timestamp

    def on_connect(self, controller):
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)

    def on_frame(self, controller):
        frame = controller.frame()

        if len(frame.hands) == 0:
            self._hasHands = False
            self._hand = None
        else:
            self._hasHands = True
            self._hand = frame.hands[0]

        if self._hasHands:
            self._frame = frame
            self._movesideways()
            self._rotate()

        self.previous_frame = frame
