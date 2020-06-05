class Event {
    constructor(eventData, params={}) {
        this.action = eventData.action;
        this.category = eventData.category;
        this.params = params;
    }

    toString() {
        return JSON.stringify({
            'action': this.action,
            'category': this.category,
            'params': this.params
        });
    }
}

export class PingEvent extends Event {
    constructor() {
        super({ action: 'ping', category: 'ping' });
    }
}

export class WheelEvent extends Event {
    constructor(action, params={ timeout: 100 }) {
        super({ action: action, category: 'wheel' },
                params);
    }
}
