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
    font-size: 20px;
    padding-top: 2px;
}`;

const html = `
<style>
${parentCss}
${css}
</style>
<div class='sheet'>
    <div class='sheet__item'>
        <label class='sheet__item__label' for='powerSwitch'>
            Power
        </label>
        <dbs-toggle-switch class='sheet__item__switch' id='powerSwitch'></dbs-toggle-switch>
    </div>
</div>`;

let template = document.createElement('template');
template.innerHTML = html;

export default class IndicatorSheet extends Sheet {
    constructor() {
        super();
        const shadow = this.attachShadow({ mode: 'open' });
        shadow.appendChild(template.content.cloneNode(true));
        this.shadowRoot.querySelector('#powerSwitch').addEventListener('toggle', (e) => {
            const event = new CustomEvent('pinActiveChange', {
                bubbles: true,
                cancelable: false,
            });
            this.anyPinActive = e.currentTarget.active;
            this.dispatchEvent(event);
        });
    }

    get anyPinActive() {
        return this.hasAttribute('anyPinActive');
    }

    set anyPinActive(val) {
        if (val)
            this.setAttribute('anyPinActive', '');
        else
            this.removeAttribute('anyPinActive');

        this.shadowRoot.querySelector('#powerSwitch').active = val;
    }

    set state(val) {
        const newState = JSON.parse(val.toString());
        if ('pinsActive' in newState) {
            this.pinsActive = newState.pinsActive;
            this.anyPinActive = val.anyPinActive;
        }
        if ('oscillators' in newState) {
            this.oscillators = newState.oscillators;
        }
    }
}
