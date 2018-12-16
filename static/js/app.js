namespace = '/test';
var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

socket.on('connect', function() {
    console.log("I'm connected bitches!");
    socket.emit('parcel', {data: 'I\'m connected!'});
});

document.addEventListener("DOMContentLoaded", function() {
    let pressedDown = false;
    const joystick = new VirtualJoystick({
        container: document.getElementById('joystick-area'),
        mouseSupport: true
    });

    setInterval(() => {
        if (joystick.up()) {
            pressedDown = true;
            console.log('Forward');
            socket.emit('forward', { activated: true });
        } else if (joystick.down()) {
            pressedDown = true;
            console.log('Backward');
            socket.emit('backward', { activated: true });
        } else if (joystick.left()) {
            pressedDown = true;
            console.log('Left');
            socket.emit('counterclockwise', { activated: true });
        } else if (joystick.right()) {
            pressedDown = true;
            console.log('Right');
            socket.emit('clockwise', { activated: true });
        } else if (pressedDown) {
            socket.emit('forward', { activated: false });
            socket.emit('backward', { activated: false });
            socket.emit('counterclockwise', { activated: false });
            socket.emit('clockwise', { activated: false });
            pressedDown = false;
        }
    }, 100);

    const forwardButton = document.getElementById('forward-button');
    forwardButton.addEventListener('mousedown', () => {
        console.log('Forward down!');
        socket.emit('forward', { activated: true });
    });

    forwardButton.addEventListener('mouseup', () => {
        console.log('Forward up!');
        socket.emit('forward', { activated: false });
    });

    const backwardButton = document.getElementById('backward-button');
    backwardButton.addEventListener('mousedown', () => {
        console.log('Backward down!');
        socket.emit('backward', { activated: true });
    });
    backwardButton.addEventListener('mouseup', () => {
        console.log('Backward up!');
        socket.emit('backward', { activated: false });
    });

    const leftButton = document.getElementById('left-button');
    leftButton.addEventListener('mousedown', () => {
        console.log('Left down!');
        socket.emit('counterclockwise', { activated: true });
    });
    leftButton.addEventListener('mouseup', () => {
        console.log('Left up!');
        socket.emit('counterclockwise', { activated: false });
    });

    const rightButton = document.getElementById('right-button');
    rightButton.addEventListener('mousedown', () => {
        console.log('Right down!');
        socket.emit('clockwise', { activated: true });
    });
    rightButton.addEventListener('mouseup', () => {
        console.log('Right up!');
        socket.emit('counterclockwise', { activated: false });
    });

    // Virtual joystick code
    console.log("touchscreen is", VirtualJoystick.touchScreenAvailable() ? "available" : "not available");
});
