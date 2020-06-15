const css = `
/* The switch - the box around the slider */
.switch {
    position: relative;
    display: inline-block;
    width: 60px;
    height: 34px;
}

/* Hide default HTML checkbox */
.switch input {
    opacity: 0;
    width: 0;
    height: 0;
}

/* The slider */
.slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    -webkit-transition: .4s;
    transition: .4s;
}

.slider:before {
    position: absolute;
    content: "";
    height: 26px;
    width: 26px;
    left: 4px;
    bottom: 4px;
    background-color: white;
    -webkit-transition: .4s;
    transition: .4s;
}

input:checked + .slider {
    background-color: var(--secondary-color-light);
}

input:focus + .slider {
    box-shadow: 0 0 1px var(--secondary-color-light);
}

input:checked + .slider:before {
    -webkit-transform: translateX(26px);
    -ms-transform: translateX(26px);
    transform: translateX(26px);
}

/* Rounded sliders */
.slider.round {
    border-radius: 34px;
}

.slider.round:before {
    border-radius: 50%;
}
`;

const html = `
<style>
${css}
</style>
<label class='switch'>
    <input type='checkbox'>
    <span class='slider round'></span>
</label>
`;

let template = document.createElement('template');
template.innerHTML = html;

export default class ToggleSwitch extends HTMLElement {
    constructor() {
        super();
        const shadow = this.attachShadow({ mode: 'open' });
        shadow.appendChild(template.content.cloneNode(true));
        this.shadowRoot.querySelector('input[type]').addEventListener('click', (e) => {
            const event = new CustomEvent('toggle', {
                bubbles: true,
                cancelable: false,
            });
            this.active = e.target.checked;
            this.dispatchEvent(event);
        });
    }

    get active() {
        return this.hasAttribute('active');
    }
    
    set active(val) {
        if (val)
            this.setAttribute('active', '');
        else
            this.removeAttribute('active');

        this.shadowRoot.querySelector('input[type]').checked = val;
    }

    connectedCallback() {
        this.shadowRoot.querySelector('input[type]').checked = this.active;
    }
}
