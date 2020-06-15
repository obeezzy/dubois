const shadowCss = `
:host {
    --sheet-height: 120px;

    background-color: var(--primary-color-darker);
    display: block;
    width: 100%;
    height: var(--sheet-height);
    position: absolute;
    z-index: 2;
    transition: top .25s cubic-bezier(0.34, 1.56, 0.64, 1);
    top: 100%;
    padding: 8px 8px var(--panel-height) 8px
}

:host([open]) {
    top: calc(100vh - var(--sheet-height));
}

:host([hidden]) {
    display: none;
}`;

export const css = `
${shadowCss}
.sheet {
    display: flex;
    height: 100%;
    flex-direction: column;
    align-items: stretch;
}`;

export default class Sheet extends HTMLElement {
    constructor() {
        super();
        setTimeout(() => { this.open = true; }, 10);
    }

    get open() {
        return this.hasAttribute('open');
    }

    set open(val) {
        if (val) {
            this.setAttribute('open', '');
        } else {
            this.addEventListener('transitionend', () => this.remove());
            this.addEventListener('webkitTransitionEnd', () => this.remove());
            this.removeAttribute('open');
        }
    }
}
