import sys, thread, time, os, inspect
import events

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
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				self.rotate_right(grid)
			if event.key == pygame.K_RIGHT:
				self.move_right(grid)
			if event.key == pygame.K_LEFT:
				self.move_left(grid)
			if event.key == pygame.K_DOWN:
				self._timer = 5
				self._current_speed = 5
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_DOWN:
				self._current_speed = self.SPEED
			if event.key == pygame.K_p:
				self._paused = not self._paused


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

		# Get gestures
		for gesture in frame.gestures():
			if gesture.type == Leap.Gesture.TYPE_CIRCLE:
				circle = CircleGesture(gesture)

				# Determine clock direction using the angle between the pointable and the circle normal
				if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
					clockwiseness = "clockwise"
				else:
					clockwiseness = "counterclockwise"

				# Calculate the angle swept since the last frame
				swept_angle = 0
				if circle.state != Leap.Gesture.STATE_START:
					previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
					swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI

				print "  Circle id: %d, %s, progress: %f, radius: %f, angle: %f degrees, %s" % (
						gesture.id, self.state_names[gesture.state],
						circle.progress, circle.radius, swept_angle * Leap.RAD_TO_DEG, clockwiseness)

			if gesture.type == Leap.Gesture.TYPE_SWIPE:
				swipe = SwipeGesture(gesture)
				print "  Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (
						gesture.id, self.state_names[gesture.state],
						swipe.position, swipe.direction, swipe.speed)

			if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
				keytap = KeyTapGesture(gesture)
				print "  Key Tap id: %d, %s, position: %s, direction: %s" % (
						gesture.id, self.state_names[gesture.state],
						keytap.position, keytap.direction )

			if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
				screentap = ScreenTapGesture(gesture)
				print "  Screen Tap id: %d, %s, position: %s, direction: %s" % (
						gesture.id, self.state_names[gesture.state],
						screentap.position, screentap.direction )