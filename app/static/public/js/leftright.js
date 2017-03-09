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
        console.log("Socket IO connected to web server.");
    });
    
    socket.on('success', function() {
        $(".container").removeClass("error");
    });

    socket.on('pireconnect', function(msg) {
        console.log("We're back, baby. (Message: " + str(msg) + ")");
        $(".container").removeClass("error");
    });

    socket.on('pidisconnect', function(msg) {
        console.log("Pi is down.");
        $(".container").addClass("error");
    });

}

$(document).ready(function() {
    setupSockets();
    var $left = $(".circle.left");
    var $right = $(".circle.right");

    var keydown = false;

    $left.on('mousedown', function(event) {
        left();
        $left.addClass("pulsate");
    });

    $right.on('mousedown', function(event) {
        right();
        $right.addClass("pulsate");
    });
    
    window.addEventListener('keydown', function(event) {
        var code = event.keyCode;
        if(!keydown) {
            keydown = true;
            if(code === 37) {
                left();
                $left.addClass("pulsate");
            } else if (code === 39) {
                right();
                $right.addClass("pulsate");
            }
        }
    }, false);

    var done = function(event) {
        var code = event.keyCode;
        keydown = false;
        if(code === 37) {
            stop();
        } else if (code === 39) {
            stop();
        } else if (!code) {
            stop();
        }
        $left.removeClass("pulsate");
        $right.removeClass("pulsate");
    }

    window.addEventListener('keyup', done , false);
    window.addEventListener('mouseup', done, false);
});
