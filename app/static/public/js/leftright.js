var socket = null;

function left() {
    socket.emit('left', "Going left!");
}

function right() {
    socket.emit('right', "Going right!");
}

function stop() {
    socket.emit('stop', "");
}

function onkeydown(event) {
    
}

function setupSockets() {
    var namespace = '/pir'; // change to an empty string to use the global namespace
    // socket = new WebSocket("ws://" + document.domain + ":" + location.port + "/pir");
    socket = io('http://' + document.domain + ':' + location.port + namespace);
    // event handler for server sent data
    // the data is displayed in the "Received" section of the page
    // event handler for new connections
    socket.on('connect', function() {
        console.log("connected");
    });
}

$(document).ready(function() {
    setupSockets();
    var $left = $(".circle.left");
    var $right = $(".circle.right");
    
    window.addEventListener('keydown', function(event) {
        var code = event.keyCode;
        if(code === 37) {
            left();
//            $left.addClass("hovered");
            $left.addClass("pulsate");
        } else if (code === 39) {
            right();
//            $right.addClass("hovered");
            $right.addClass("pulsate");
        }
    }, false);

    window.addEventListener('keyup', function(event) {
        var code = event.keyCode;
        if(code === 37) {
            stop();
        } else if (code === 39) {
            stop();
        }
        $left.removeClass("pulsate");
        $right.removeClass("pulsate");
    }, false);
});
