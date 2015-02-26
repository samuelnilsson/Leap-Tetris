import sys, inspect, thread, time
sys.path.insert(0, "lib")
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))
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