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
    } else if (remoteState.category == 'aggregate') {
        applyBuzzerState(new BuzzerState(remoteState.states.buzzer));
        applyHeadlightState(new HeadlightState(remoteState.states.headlight));
        applyIndicatorState(new IndicatorState(remoteState.states.indicator));
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
    const sheet = document.querySelector('headlight-sheet');
    if (sheet)
        sheet.state = state;
};

const applyIndicatorState = (state) => {
    robot.indicatorState = state;
};

document.getElementById('buzzerButton').addEventListener('click', (e) => {
    e.preventDefault();
    duboisClient.send(new BuzzerEvent(robot.buzzerState.pinActive ? 'power_off' : 'power_on' ));
    navigator.vibrate(Constants.FEEDBACK_VIBRATION_DURATION);
});

document.getElementById('headlightButton').addEventListener('click', (e) => {
    e.preventDefault();
    navigator.vibrate(Constants.FEEDBACK_VIBRATION_DURATION);

    let sheet = document.querySelector('headlight-sheet');
    if (sheet) {
        e.target.removeAttribute('panel__item--selected');
        sheet.open = false;
    } else {
        sheet = new HeadlightSheet();
        sheet.state = robot.headlightState;
        document.querySelector('.panel').before(sheet);
        e.target.setAttribute('panel__item--selected', '');
        sheet.addEventListener('pinActiveChange', (e) => {
            duboisClient.send(new HeadlightEvent(e.target.pinActive ? 'power_on' : 'power_off' ));
        });
    }
});

document.getElementById('indicatorButton').addEventListener('click', (e) => {
    e.preventDefault();
    duboisClient.send(new IndicatorEvent(robot.indicatorState.anyPinActive ? 'power_off' : 'power_on' ));
    navigator.vibrate(Constants.FEEDBACK_VIBRATION_DURATION);
});
