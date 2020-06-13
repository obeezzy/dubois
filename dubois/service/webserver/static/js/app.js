import { HeadlightSheet, ToggleSwitch } from './components/ui.js';
import { VirtualJoystick } from './vendor/virtualjoystick.js';
import { robot, Constants } from './robot.js';
import { DuboisClient } from './network.js';
import { BuzzerEvent, HeadlightEvent, IndicatorEvent, WheelEvent } from './_events.js';
import { BuzzerState, ErrorState, HeadlightState, IndicatorState } from './_states.js';

const duboisClient = new DuboisClient();
duboisClient.onrecv = (remoteState) => {
    if (remoteState.category == 'buzzer') {
        applyBuzzerState(new BuzzerState(remoteState));
    } else if (remoteState.category == 'headlight') {
        applyHeadlightState(new HeadlightState(remoteState));
    } else if (remoteState.category == 'indicator') {
        applyIndicatorState(new IndicatorState(remoteState));
    } else if (remoteState.category == 'error') {
        console.error('Error state received:', remoteState.message);
    }
};

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

customElements.define('headlight-sheet', HeadlightSheet);
customElements.define('toggle-switch', ToggleSwitch);

const applyBuzzerState = (state) => {
    robot.buzzerState = state;
}

const applyHeadlightState = (state) => {
    robot.headlightState = state;
//    const sheet = document.querySelector('headlight-sheet');
//    if (sheet)
//        sheet.state = state.toString();
};

const applyIndicatorState = (state) => {
    robot.indicatorState = state;
};

document.getElementById('buzzer').addEventListener('click', (event) => {
    event.preventDefault();
    duboisClient.send(new BuzzerEvent(robot.buzzerState.pinActive ? 'power_off' : 'power_on' ));
    navigator.vibrate(Constants.FEEDBACK_VIBRATION_DURATION);
});

document.getElementById('headlight').addEventListener('click', (event) => {
    event.preventDefault();
    navigator.vibrate(Constants.FEEDBACK_VIBRATION_DURATION);

    let sheet = document.querySelector('headlight-sheet');
    if (sheet) {
        document.getElementById('headlight').removeAttribute('panel__item--selected');
        sheet.open = false;
    } else {
        sheet = new HeadlightSheet();
        sheet.state = robot.headlightState.toString();
        document.querySelector('.panel').before(sheet);
        document.getElementById('headlight').setAttribute('panel__item--selected', '');
        sheet.powerSwitch.addEventListener('click', (e) => {
            duboisClient.send(new HeadlightEvent(robot.headlightState.pinActive ? 'power_off' : 'power_on' ));
        });
    }
});

document.getElementById('indicator').addEventListener('click', (event) => {
    event.preventDefault();
    duboisClient.send(new IndicatorEvent(robot.indicatorState.anyPinActive ? 'power_off' : 'power_on' ));
    navigator.vibrate(Constants.FEEDBACK_VIBRATION_DURATION);
});
