class State {
    constructor(stateData) {
        this.category = stateData.category;
    }
}

export class ErrorState extends State {
    constructor(stateData) {
        this.message = stateData;
    }
}

export class HeadlightState extends State {
    constructor(stateData) {
        this.pinActive = stateData.pinActive;
        this.oscillator = stateData.oscillator;
    }
}
