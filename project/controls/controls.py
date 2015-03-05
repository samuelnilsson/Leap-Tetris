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


class KeyboardControls:
 	def on_event(self, event):
 		generated_event = self._generate_event(event)
		if generated_event is not None:
			pygame.event.post(pygame.event.Event(generated_event))

	def _generate_event(self, pygame_event):
		if pygame_event.type == pygame.KEYDOWN:
			return {
				pygame.K_UP: 	Events.ROTATE_RIGHT,
				pygame.K_RIGHT: Events.MOVE_RIGHT,
				pygame.K_LEFT: 	Events.MOVE_LEFT,
				pygame.K_DOWN:	Events.DOWN_FASTER
			}.get(pygame_event.key, None)
		if pygame_event.type == pygame.KEYUP:
			return {
				pygame.K_DOWN: 	Events.DOWN_NORMAL,
				pygame.K_p: 	Events.PAUSE_TOGGLE
			}.get(pygame_event.key, None)

		return None


class LeapControls(Leap.Listener):
	finger_names 	= ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
	bone_names 		= ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
	state_names 	= ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

	def __init__(self):
		Leap.Listener.__init__(self)
		self._controller = Leap.Controller()
		self._controller.add_listener(self)
		self._seesHands = False

	def on_event(self, event):
		print event

	def on_init(self, controller):
		print "Initialized"

	def on_connect(self, controller):
		print "Connected"

		controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
		controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

	def on_disconnect(self, controller):
		# Note: not dispatched when running in a debugger.
		print "Disconnected"

	def on_exit(self, controller):
		print "Exited"

	def on_frame(self, controller):
		frame = controller.frame()

		if len(frame.hands) == 0:
			self._hasHands = False
			print "Cant see hands :("
		else:
			self._hasHands = True
			print "Can see hands :)"
			for hand in frame.hands:
				handType = "Left hand" if hand.is_left else "Right hand"

				# Get the hand's normal vector and direction
				# normal = hand.palm_normal
				# direction = hand.direction

				# Calculate the hand's pitch, roll, and yaw angles
				# print "  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
				# 	direction.pitch * Leap.RAD_TO_DEG,
				# 	normal.roll * Leap.RAD_TO_DEG,
				# 	direction.yaw * Leap.RAD_TO_DEG)

		for gesture in frame.gestures():
			if gesture.type == Leap.Gesture.TYPE_CIRCLE:
				circle = CircleGesture(gesture)

				if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
					clockwiseness = "clockwise"
				else:
					clockwiseness = "counterclockwise"

				swept_angle = 0
				if circle.state != Leap.Gesture.STATE_START:
					previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
					swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI

				# print "  Circle id: %d, %s, progress: %f, radius: %f, angle: %f degrees, %s" % (
				# 		gesture.id, self.state_names[gesture.state],
				# 		circle.progress, circle.radius, swept_angle * Leap.RAD_TO_DEG, clockwiseness)

			if gesture.type == Leap.Gesture.TYPE_SWIPE:
				swipe = SwipeGesture(gesture)
				# print "  Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (
				# 		gesture.id, self.state_names[gesture.state],
				# 		swipe.position, swipe.direction, swipe.speed)

			if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
				keytap = KeyTapGesture(gesture)
				# print "  Key Tap id: %d, %s, position: %s, direction: %s" % (
				# 		gesture.id, self.state_names[gesture.state],
				# 		keytap.position, keytap.direction )

			if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
				screentap = ScreenTapGesture(gesture)
				# print "  Screen Tap id: %d, %s, position: %s, direction: %s" % (
				# 		gesture.id, self.state_names[gesture.state],
				# 		screentap.position, screentap.direction )