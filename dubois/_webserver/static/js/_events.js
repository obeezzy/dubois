class Event {
    constructor(eventData, params={}) {
        this.action = eventData.action;
        this.type = eventData.type;
        this.params = params;
    }

    toString() {
        return JSON.stringify({
            'action': this.action,
            'type': this.type,
            'params': this.params
        });
    }
}

export class Ping extends Event {
    constructor() {
        super({ action: 'ping', type: 'pingEvent' });
    }
}

export class WheelEvent extends Event {
    constructor(action, params={ timeout: 100 }) {
        super({ action: action, type: 'wheelEvent' },
                params);
    }
}
