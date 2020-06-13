import Sheet, { css as parentCss } from './common/Sheet.js';

const css = `
.sheet__item {
    display: flex;
    align-items: stretch;
    justify-content: stretch;
    color: var(--text-color);
    padding: 2px 8px;
}

.sheet__item__label {
    flex: 1;
}`;

const html = `
<style>
${parentCss}
${css}
</style>
<div class='sheet'>
    <div class='sheet__item'>
        <label class='sheet__item__label' for='powerSwitch'>Power</label>
        <toggle-switch class='sheet__item__switch' id='powerSwitch'></toggle-switch>
    </div>
</div>`;

let template = document.createElement('template');
template.innerHTML = html;

export default class HeadlightSheet extends Sheet {
    constructor() {
        super();
        const shadow = this.attachShadow({ mode: 'open' });
        shadow.appendChild(template.content.cloneNode(true));
    }

    get pinActive() {
        return this.shadowRoot.querySelector('#powerSwitch').checked;
    }

    set pinActive(val) {
        this.shadowRoot.querySelector('#powerSwitch').checked = val;
    }

    set state(val) {
        const newState = JSON.parse(val);
        if ('pinActive' in newState)
            this.pinActive = newState.pinActive;
        if ('oscillator' in newState)
            this.oscillator = newState.oscillator;
    }

    connectedCallback() {
        super.connectedCallback();
        this.powerSwitch = this.shadowRoot.querySelector('#powerSwitch');
    }
}
