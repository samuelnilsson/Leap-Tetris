import sys, thread, time, os, inspect
import pygame
from events import Events

from sys import platform as _platform

if _platform == "linux" or _platform == "linux2":
	src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
	arch_dir = './lib/x64/' if sys.maxsize > 2**32 else './lib/x86/'
	sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))
	import Leap
else:
	sys.path.insert(0, "lib")
	import Leap

from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture


class BaseControls: # TODO: Make this abstract?
	def _post_event(self, event):
		pygame.event.post(pygame.event.Event(event))

	def on_event(self, event):
		return


class KeyboardControls(BaseControls):
	def __init__(self):
		self._keyup_events = {
			pygame.K_UP: 	Events.ROTATE_RIGHT,
			pygame.K_RIGHT: Events.MOVE_RIGHT,
			pygame.K_LEFT: 	Events.MOVE_LEFT,
			pygame.K_DOWN:	Events.DOWN_FASTER
		}
		self._keydown_events = {
			pygame.K_DOWN: 	Events.DOWN_NORMAL,
			pygame.K_p: 	Events.PAUSE_TOGGLE
		}

 	def on_event(self, event):
 		generated_event = self._generate_event(event)
		if generated_event is not None:
			self._post_event(generated_event)

	def _generate_event(self, pygame_event):
		if pygame_event.type == pygame.KEYDOWN:
			return self._keyup_events.get(pygame_event.key, None)
		if pygame_event.type == pygame.KEYUP:
			return self._keydown_events.get(pygame_event.key, None)

		return None


class LeapControls(Leap.Listener, BaseControls):
	finger_names 	= ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
	bone_names 		= ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
	state_names 	= ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

	def __init__(self):
		Leap.Listener.__init__(self)
		self._controller = Leap.Controller()
		self._controller.add_listener(self)
		self._hasHands = False
		self.previous_frame = None

	def on_init(self, controller):
		print "Initialized"

	def on_connect(self, controller):
		print "Connected"

		controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
		controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

	def on_disconnect(self, controller):
		print "Disconnected"

	def on_exit(self, controller):
		print "Exited"

	def on_frame(self, controller):
		frame = controller.frame()

		# if self._hasHands:
		# 	self._post_event(Events.ROTATE_RIGHT)

		if len(frame.hands) == 0:
			self._hasHands = False
			self._hand = None
		else:
			self._hasHands = True
			self._hand = frame.hands[0]

		if self._hand is not None:


		self.previous_frame = frame