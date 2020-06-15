import { BuzzerState, HeadlightState, IndicatorState } from './_states.js';

class Robot {
    constructor() {
        this.buzzerState = new BuzzerState();
        this.headlightState = new HeadlightState();
        this.indicatorState = new IndicatorState();
    }
}

export default new Robot();
export const Color = Object.freeze({'RED': 0, 'GREEN': 1, 'BLUE': 2});
export const Constants = {
    FEEDBACK_VIBRATION_DURATION: 50,
};
