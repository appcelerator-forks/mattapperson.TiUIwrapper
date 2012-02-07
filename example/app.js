var TiUIwrapper = require('TiUIwrapper');

//extend before we use it…
TiUIwrapper.createLabel.prototype.laugh = function() {
    alert('HAHAHAHA!');
};

var test = new TiUIwrapper.createLabel({text: 'YAY!!!'});

// To directly edit a property of the element after creation… (fixing this soon)
test.proxy.backgroundColor = 'blue';

test.addEventListener('click', function() {
    alert('YAY!!!!');
});

test.addEventListener('click', function() {
    test.laugh();
});

// No custom properties in here (yet, but it will come...) 
var win = new TiUIwrapper.createWindow({
    title:'Test',
    backgroundColor:'#fff',
    barColor:'#000'
});

win.add(test);


win.open();