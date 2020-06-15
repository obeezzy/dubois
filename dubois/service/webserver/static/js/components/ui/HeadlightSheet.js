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
        <dbs-toggle-switch class='sheet__item__switch'></dbs-toggle-switch>
    </div>
</div>`;

let template = document.createElement('template');
template.innerHTML = html;

export default class HeadlightSheet extends Sheet {
    constructor() {
        super();
        const shadow = this.attachShadow({ mode: 'open' });
        shadow.appendChild(template.content.cloneNode(true));
        this.shadowRoot.querySelector('dbs-toggle-switch').addEventListener('toggle', (e) => {
            const event = new CustomEvent('pinActiveChange', {
                bubbles: true,
                cancelable: false,
            });
            this.pinActive = e.target.active;
            this.dispatchEvent(event);
        });
    }

    get pinActive() {
        return this.hasAttribute('pinActive');
    }

    set pinActive(val) {
        console.log('HeadlightSheet.pinActive', val);
        if (val)
            this.setAttribute('pinActive', '');
        else
            this.removeAttribute('pinActive');

        this.shadowRoot.querySelector('dbs-toggle-switch').active = val;
    }

    set state(val) {
        const newState = JSON.parse(val.toString());
        if ('pinActive' in newState) {
            this.pinActive = newState.pinActive;
        }
        if ('oscillator' in newState) {
            this.oscillator = newState.oscillator;
        }
    }
}
