var imgContainer = document.getElementById("images");
var imgs = [
	'imgs/dj.jpeg',
	'imgs/earphones.jpeg',
	'imgs/flower.jpeg',
	'imgs/ipad.jpeg',
	'imgs/wine.jpeg',
	'imgs/ants.jpeg',
	'imgs/city.jpeg',
	'imgs/abstract.jpeg',
	'imgs/couple.jpeg',
];

for(var imgKey in imgs) {
	var imgSrc = imgs[imgKey];
	var img = document.createElement('img');
	img.src = imgSrc;
	imgContainer.appendChild(img);
}

window.onload = function() {
	var center = (imgs.length * 400 - document.body.offsetWidth) / 2;
	window.scroll(center, 0);
};


function stepRight() {
	step(400, 500);
}

function stepLeft() {
	step(-400, 500);
}

function step(amount, time) {
	var amount 		= amount || 400,
		time 		= time || 500,
		numSteps 	= time / 10,
		amountStep 	= amount / numSteps;

	console.log('amountStep', amountStep);
	console.log('numSteps', numSteps);

	var interval = setInterval(function() {
		var  nextScrollPosition = window.pageXOffset + amountStep;
		console.log(nextScrollPosition);
		window.scroll(nextScrollPosition, 0);

		if(--numSteps == 0)
			clearInterval(interval);
	}, 10);
}