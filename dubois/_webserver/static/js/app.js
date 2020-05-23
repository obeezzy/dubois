class Message {
    constructor(action, params=null) {
        this.action = action;
        this.params = params === null ? {} : params;
    }

    toString() {
        return JSON.stringify({
            'action': this.action,
            'params': this.params
        });
    }
}

serverAddress = document.domain;
port = 4201;
const connection = new WebSocket('ws://' + serverAddress + ':' + port);
connection.onopen = () => connection.send(new Message('ping'));
connection.onerror = (error) => console.log('WebSocket error:', error);
connection.onmessage = (event) => console.log('Server:', event.data);

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
            connection.send(new Message('move_forward'), { activated: true });
        } else if (joystick.down()) {
            pressedDown = true;
            console.log('Backward');
            connection.send(new Message('move_backward'), { activated: true });
        } else if (joystick.left()) {
            pressedDown = true;
            console.log('Left');
            socket.emit('counterclockwise', { activated: true });
            connection.send(new Message('move_counterclockwise'), { activated: true });
        } else if (joystick.right()) {
            pressedDown = true;
            console.log('Right');
            socket.emit('clockwise', { activated: true });
            connection.send(new Message('move_clockwise'), { activated: true });
        } else if (pressedDown) {
            connection.send(new Message('move_forward'), { activated: false });
            connection.send(new Message('move_backward'), { activated: false });
            connection.send(new Message('move_counterclockwise'), { activated: false });
            connection.send(new Message('move_clockwise'), { activated: false });
            pressedDown = false;
        }
    }, 100);

    const forwardButton = document.getElementById('forward-button');
    forwardButton.addEventListener('mousedown', () => {
        console.log('Forward down!');
        connection.send(new Message('move_forward'), { activated: true });
    });

    forwardButton.addEventListener('mouseup', () => {
        console.log('Forward up!');
        connection.send(new Message('move_forward'), { activated: false });
    });

    const backwardButton = document.getElementById('backward-button');
    backwardButton.addEventListener('mousedown', () => {
        console.log('Backward down!');
        connection.send(new Message('move_backward'), { activated: true });
    });
    backwardButton.addEventListener('mouseup', () => {
        console.log('Backward up!');
        connection.send(new Message('move_backward'), { activated: false });
    });

    const leftButton = document.getElementById('left-button');
    leftButton.addEventListener('mousedown', () => {
        console.log('Left down!');
        connection.send(new Message('move_counterclockwise'), { activated: true });
    });
    leftButton.addEventListener('mouseup', () => {
        console.log('Left up!');
        connection.send(new Message('move_counterclockwise'), { activated: false });
    });

    const rightButton = document.getElementById('right-button');
    rightButton.addEventListener('mousedown', () => {
        console.log('Right down!');
        connection.send(new Message('move_clockwise'), { activated: true });
    });
    rightButton.addEventListener('mouseup', () => {
        console.log('Right up!');
        connection.send(new Message('move_clockwise'), { activated: false });
    });

    // Virtual joystick code
    console.log("touchscreen is", VirtualJoystick.touchScreenAvailable() ? "available" : "not available");
});
