import { VirtualJoystick } from './vendor/virtualjoystick.js';
import { WheelEvent, HeadlightEvent } from './_events.js';
import { ErrorState, HeadlightState } from './_states.js';

class DuboisClient {
    constructor(serverAddress=document.domain, serverPort=4201) {
        this.ws = new WebSocket('ws://' + serverAddress + ':' + serverPort);
        this.ws.onopen = () => console.log("Socket opened.");
        this.ws.onerror = (error) => console.log('WebSocket error:', error);
        this.ws.onmessage = (event) => this.recv(event.data);
        this.ws.onclose = (event) => console.log('WebSocket closed. Reason:', event.code);
    }

    send(remoteEvent) {
        if (Object(remoteEvent).hasOwnProperty('action')) {
            console.log('Event sent:', remoteEvent.toString());
            this.ws.send(remoteEvent);
        } else {
            console.error('No action specified.');
        }
    }

    recv(remoteState) {
        console.log('State received:', remoteState);
        if (remoteState.category == 'error') {
            console.log('Error state received:', remoteState.message);
        } else if (remoteState.category == 'headlight') {
            applyHeadlightState(new HeadlightState(remoteState));
        }
    }
}

const duboisClient = new DuboisClient();

customElements.define('joystick-area',
    class extends HTMLElement {
        constructor() {
            super();

            const joystick = new VirtualJoystick({
                container: this,
                mouseSupport: true,
                strokeStyle: '#fff',
                limitStickTravel: true,
            });

            setInterval(() => {
                if (joystick.up()) {
                    duboisClient.send(new WheelEvent('move_forward'));
                } else if (joystick.down()) {
                    duboisClient.send(new WheelEvent('move_backward'));
                } else if (joystick.left()) {
                    duboisClient.send(new WheelEvent('move_counterclockwise'));
                } else if (joystick.right()) {
                    duboisClient.send(new WheelEvent('move_clockwise'));
                }
            }, 100);
        }
    }
);

let powerOn = false;
document.getElementById('headlight').addEventListener('click', (event) => {
    powerOn = !powerOn;
    duboisClient.send(new HeadlightEvent(powerOn ? 'power_on' : 'power_off'));
});

const applyHeadlightState = (state) => {
    console.log('Headlights state received:', state.pinActive);
};
