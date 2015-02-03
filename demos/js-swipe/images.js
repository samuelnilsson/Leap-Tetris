var imgContainer = document.getElementById("images");
var animationStep = 20;
var animationStepTime = 100;
var imgs = [
	'imgs/dj.jpeg',
	'imgs/earphones.jpeg',
	'imgs/flower.jpeg',
	'imgs/ipad.jpeg',
	'imgs/wine.jpeg',
];

for(var imgKey in imgs) {
	var imgSrc = imgs[imgKey];
	var img = document.createElement('img');
	img.src = imgSrc;
	imgContainer.appendChild(img);
}

function stepRight() {
	window.scroll(window.pageXOffset + animationStep, 0);
	console.log(window.scrollX);
}

function stepLeft() {
	window.scroll(window.pageXOffset - animationStep, 0);
	console.log(window.scrollX);
}