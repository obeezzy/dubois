import { VirtualJoystick } from './vendor/virtualjoystick.js';
import { robot } from './robot.js';
import { BuzzerEvent, HeadlightEvent, IndicatorEvent, WheelEvent } from './_events.js';
import { BuzzerState, ErrorState, HeadlightState, IndicatorState } from './_states.js';

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
        remoteState = JSON.parse(remoteState)
        console.log('State received:', remoteState);
        if (remoteState.category == 'buzzer') {
            applyBuzzerState(new BuzzerState(remoteState));
        } else if (remoteState.category == 'headlight') {
            applyHeadlightState(new HeadlightState(remoteState));
        } else if (remoteState.category == 'indicator') {
            applyIndicatorState(new IndicatorState(remoteState));
        } else if (remoteState.category == 'error') {
            console.log('Error state received:', remoteState.message);
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

const applyBuzzerState = (state) => {
    robot.buzzerState = state;
}

const applyHeadlightState = (state) => {
    robot.headlightState = state;
};

const applyIndicatorState = (state) => {
    robot.indicatorState = state;
};

document.getElementById('buzzer').addEventListener('click', (event) => {
    duboisClient.send(new BuzzerEvent(robot.buzzerState.pinActive ? 'power_off' : 'power_on' ));
});

document.getElementById('headlight').addEventListener('click', (event) => {
    duboisClient.send(new HeadlightEvent(robot.headlightState.pinActive ? 'power_off' : 'power_on' ));
});

document.getElementById('indicator').addEventListener('click', (event) => {
    duboisClient.send(new IndicatorEvent(robot.indicatorState.anyPinActive ? 'power_off' : 'power_on' ));
});
