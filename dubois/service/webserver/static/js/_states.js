class State {
    constructor(stateData) {
        this.category = stateData.category;
    }
}

export class ErrorState extends State {
    constructor(stateData={category: 'error'}) {
        super(stateData);
        this.message = stateData;
    }
}

export class BuzzerState extends State {
    constructor(stateData={category: 'buzzer'}) {
        super(stateData);
        this.pinActive = stateData.pinActive || false;
        this.oscillator = stateData.oscillator || null;
    }

    toString() {
        return JSON.stringify({
            pinActive: this.pinActive,
            oscillator: this.oscillator,
        });
    }
}

export class HeadlightState extends State {
    constructor(stateData={category: 'headlight'}) {
        super(stateData);
        this.pinActive = stateData.pinActive || false;
        this.oscillator = stateData.oscillator || null;
    }

    toString() {
        return JSON.stringify({
            pinActive: this.pinActive,
            oscillator: this.oscillator,
        });
    }
}

export class IndicatorState extends State {
    constructor(stateData={category: 'indicator'}) {
        super(stateData);
        this.pinsActive = stateData.pinsActive || null;
        this.oscillators = stateData.oscillators || null;
    }

    get anyPinActive() {
        if (this.pinsActive === null)
            return false;

        return this.pinsActive.filter(pinActive => pinActive).length > 0;
    }

    toString() {
        return JSON.stringify({
            pinActive: this.pinActive,
            oscillators: this.oscillators,
        });
    }
}
