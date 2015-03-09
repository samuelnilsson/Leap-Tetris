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


class BaseControls(object):     # TODO: Make this abstract?
    def __init__(self):
        self.active = False

    def on_event(self, event):
        pass

    def _post_event(self, event):
        if event is not None:
            pygame.event.post(pygame.event.Event(event))


class KeyboardControls(BaseControls):
    def __init__(self):
        BaseControls.__init__(self)

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
        if self.active:
            self._post_event(self._generate_event(event))

    def _generate_event(self, pygame_event):
        try:
            eventlist = self._eventMap.get(pygame_event.type)
            event = eventlist.get(pygame_event.key)
            return event
        except:
            return None


class LeapControls(Leap.Listener, BaseControls):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def __init__(self):
        BaseControls.__init__(self)
        Leap.Listener.__init__(self)

        self._controller = Leap.Controller()
        self._controller.add_listener(self)
        self._safezone_width = 100
        self._safezone_angle = 0.3
        self._hasHands = False
        self.previous_frame = None
        self.move_timestamp = 0
        self.rotate_timestamp = 0

    def on_frame(self, controller):
        if not self.active: return

        frame = controller.frame()

        if frame.hands.is_empty:
            self._hasHands = False
            self._hand = None
            self._post_event(Events.PAUSE)
        else:
            self._hasHands = True
            self._hand = frame.hands[0]
            self._frame = frame
            self._movesideways()
            self._rotate()
            self._post_event(Events.PLAY)

        self.previous_frame = frame

    def _moveinterval(self, x):
    	y1 = 400000 # 0.4s
    	y2 = 50000 # 0.05s
    	x1 = self._safezone_width / 2
    	x2 = 200

    	k = (y2 - y1) / (x2 - x1)
    	m = y1 - (k * x1)
    	calculated_inteval = k * abs(x) + m

        return calculated_inteval

    def _rotateinterval(self, palm_direction):
        x_angle = abs(palm_direction.x)
        millis_base = 500   # 0.5s
        interval = millis_base * 1000 * (2 - x_angle ** 2)

        print str(x_angle)+"\r"

        return interval

    def _movesideways(self):
        x = self._hand.palm_position.x

        if self._frame.timestamp - self.move_timestamp > self._moveinterval(x):
			self.move_timestamp = self._frame.timestamp
			if x < -(self._safezone_width / 2):
				self._post_event(Events.MOVE_LEFT)
			elif x > self._safezone_width / 2:
				self._post_event(Events.MOVE_RIGHT)

    def _should_rotate(self, palm_direction):
        since_rotate = self._frame.timestamp - self.rotate_timestamp
        not_too_fast = since_rotate > self._rotateinterval(palm_direction)
        enough_angle = self._safezone_angle <= abs(palm_direction.normalized.x)

        return not_too_fast and enough_angle

    def _rotate(self):
        palm_direction = self._hand.palm_normal.normalized

        if self._should_rotate(palm_direction):
            self._post_event(Events.ROTATE_RIGHT)
            self.rotate_timestamp = self._frame.timestamp