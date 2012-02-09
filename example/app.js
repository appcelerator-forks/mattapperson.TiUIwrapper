var TiUIwrapper = require('TiUIwrapper');

// extend before we use it…
TiUIwrapper.createLabel.prototype.laugh = function() {
    alert('HAHAHAHA!');
};

var test = new TiUIwrapper.createLabel({text: 'YAY!!!'});

// Replace an existing method
test.addEventListener = function(event, callback) {
    // Do whatever custom code you want
    Ti.API.info('Event listener added :)');
    
    // forward back to the orig when done… if you want :)
    this.proxy.addEventListener(event, callback)
};

// Access native properties like this
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