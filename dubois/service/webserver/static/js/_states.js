class State {
    constructor(stateData) {
        this.category = stateData.category;
    }
}

export class ErrorState extends State {
    constructor(stateData) {
        super(stateData);
        this.message = stateData;
    }
}

export class BuzzerState extends State {
    constructor(stateData) {
        super(stateData);
        this.pinActive = stateData.pinActive;
        this.oscillator = stateData.oscillator;
    }
}

export class HeadlightState extends State {
    constructor(stateData) {
        super(stateData);
        this.pinActive = stateData.pinActive;
        this.oscillator = stateData.oscillator;
    }
}
