import { VirtualJoystick } from './vendor/virtualjoystick.js';
import { WheelEvent } from './_events.js';

class DuboisClient {
    constructor(serverAddress=document.domain, serverPort=4201) {
        this.ws = new WebSocket('ws://' + serverAddress + ':' + serverPort);
        this.ws.onopen = () => console.log("Socket opened.");
        this.ws.onerror = (error) => console.log('WebSocket error:', error);
        this.ws.onmessage = (event) => console.log('Server:', event.data);
        this.ws.onclose = (event) => console.log('WebSocket closed. Reason:', event.code);
    }

    send(remoteEvent) {
        if (Object(remoteEvent).hasOwnProperty('action'))
            console.log('Action sent:', remoteEvent.action);
        else
            console.error('Malformed message object.');

        this.ws.send(remoteEvent);
    }
}

class JoystickArea extends HTMLElement {
    constructor() {
        super();
        this.duboisClient = new DuboisClient();

        const joystick = new VirtualJoystick({
            container: this,
            mouseSupport: true,
            strokeStyle: '#fff',
            limitStickTravel: true,
        });

        setInterval(() => {
            if (joystick.up()) {
                this.duboisClient.send(new WheelEvent('move_forward'));
            } else if (joystick.down()) {
                this.duboisClient.send(new WheelEvent('move_backward'));
            } else if (joystick.left()) {
                this.duboisClient.send(new WheelEvent('move_counterclockwise'));
            } else if (joystick.right()) {
                this.duboisClient.send(new WheelEvent('move_clockwise'));
            }
        }, 300);
    }
}

customElements.define('joystick-area', JoystickArea);
