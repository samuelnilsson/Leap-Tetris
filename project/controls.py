import sys, inspect, thread, time
sys.path.insert(0, "lib")
import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture


class Controls (Leap.Listener):

	def __init__(self):
		self._controller = Leap.Controller()
		self._controller.add_listener(self)

		# Keep this process running until Enter is pressed.
		print "Press Enter to quit..."
		try:
			sys.stdin.readline()
		except KeyboardInterrupt:
			pass
		finally:
			controller.remove_listener(self)

	def on_connect():
		# Do stuff when connection established.
		print "on_connect()"

	def on_frame():
		# Do stuff in each frame.
		print "on_frame()"

if __name__ == "__controls__":
	controls = Controls()