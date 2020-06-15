import { BuzzerSheet, HeadlightSheet, IndicatorSheet, ToggleSwitch } from './components/ui.js';
import { VirtualJoystick } from './vendor/virtualjoystick.js';
import robot, { Constants } from './robot.js';
import { DuboisClient } from './network.js';
import { BuzzerEvent, HeadlightEvent, IndicatorEvent, WheelEvent } from './_events.js';
import { BuzzerState, ErrorState, HeadlightState, IndicatorState } from './_states.js';

const duboisClient = new DuboisClient();
duboisClient.addEventListener('recv', (e) => {
    const remoteState = e.detail;
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
});

customElements.define('dbs-joystick-area',
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

customElements.define('dbs-buzzer-sheet', BuzzerSheet);
customElements.define('dbs-headlight-sheet', HeadlightSheet);
customElements.define('dbs-indicator-sheet', IndicatorSheet);
customElements.define('dbs-toggle-switch', ToggleSwitch);

const applyBuzzerState = (state) => {
    robot.buzzerState = state;
}

const applyHeadlightState = (state) => {
    robot.headlightState = state;
    const sheet = document.querySelector('dbs-headlight-sheet');
    if (sheet)
        sheet.state = state;
};

const applyIndicatorState = (state) => {
    robot.indicatorState = state;
};

const clearSheets = () => {
    let buzzerSheet = document.querySelector('dbs-buzzer-sheet');
    let headlightSheet = document.querySelector('dbs-headlight-sheet');
    let indicatorSheet = document.querySelector('dbs-indicator-sheet');

    if (buzzerSheet)
        buzzerSheet.open = false;
    if (headlightSheet)
        headlightSheet.open = false;
    if (indicatorSheet)
        indicatorSheet.open = false;

    let selectedPanelItem = document.querySelector('.panel__item.panel__item--selected');
    if (selectedPanelItem)
        selectedPanelItem.classList.remove('panel__item--selected');
}

document.getElementById('buzzerButton').addEventListener('click', (e) => {
    e.preventDefault();
    navigator.vibrate(Constants.FEEDBACK_VIBRATION_DURATION);

    let sheet = document.querySelector('dbs-buzzer-sheet');
    if (sheet) {
        e.currentTarget.classList.remove('panel__item--selected');
        sheet.open = false;
    } else {
        clearSheets();
        sheet = new BuzzerSheet();
        sheet.state = robot.buzzerState;
        document.querySelector('.panel').before(sheet);
        e.currentTarget.classList.add('panel__item--selected');
        sheet.addEventListener('pinActiveChange', (e) => {
            duboisClient.send(new BuzzerEvent(e.currentTarget.pinActive ? 'power_on' : 'power_off' ));
            navigator.vibrate(Constants.FEEDBACK_VIBRATION_DURATION);
        });
    }
});

document.getElementById('headlightButton').addEventListener('click', (e) => {
    e.preventDefault();
    navigator.vibrate(Constants.FEEDBACK_VIBRATION_DURATION);

    let sheet = document.querySelector('dbs-headlight-sheet');
    if (sheet) {
        e.currentTarget.classList.remove('panel__item--selected');
        sheet.open = false;
    } else {
        clearSheets();
        sheet = new HeadlightSheet();
        sheet.state = robot.headlightState;
        document.querySelector('.panel').before(sheet);
        e.currentTarget.classList.add('panel__item--selected');
        sheet.addEventListener('pinActiveChange', (e) => {
            duboisClient.send(new HeadlightEvent(e.currentTarget.pinActive ? 'power_on' : 'power_off' ));
            navigator.vibrate(Constants.FEEDBACK_VIBRATION_DURATION);
        });
    }
});

document.getElementById('indicatorButton').addEventListener('click', (e) => {
    e.preventDefault();
    navigator.vibrate(Constants.FEEDBACK_VIBRATION_DURATION);

    let sheet = document.querySelector('dbs-indicator-sheet');
    if (sheet) {
        e.currentTarget.classList.remove('panel__item--selected');
        sheet.open = false;
    } else {
        clearSheets();
        sheet = new IndicatorSheet();
        sheet.state = robot.indicatorState;
        document.querySelector('.panel').before(sheet);
        e.currentTarget.classList.add('panel__item--selected');
        sheet.addEventListener('pinActiveChange', (e) => {
            duboisClient.send(new IndicatorState(e.currentTarget.anyPinActive ? 'power_on' : 'power_off' ));
            navigator.vibrate(Constants.FEEDBACK_VIBRATION_DURATION);
        });
    }
});
