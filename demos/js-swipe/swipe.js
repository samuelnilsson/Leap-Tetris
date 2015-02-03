var output = document.getElementById("output");
var controller = Leap.loop({ enableGestures: true }, function(frame) {});
var activeSwipeHand = -1;

controller.on('gesture', function(gesture) {
	if(gesture.type == 'swipe') {
		if(gesture.state == 'start') {
			// console.log('Swipe started!', 'Swipe id:', gesture.id, gesture);

			if(gesture.direction[0] < 0)
				stepLeft();
			else
				stepRight();

		} else if(gesture.state == 'stop') {
			console.log('Swipe stopped!', 'Swipe id:', gesture.id, gesture);
		}
	}
});