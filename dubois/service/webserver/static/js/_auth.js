export class Authenticator {
    constructor() {
        const password = window.prompt('Password:');
        if (password != "***") {
            document.querySelector('body').style = 'color: #fff; text-align: center; margin: 0 auto;';
            document.querySelector('body').innerHTML = '<h4>Wrong password</h4>';
        } else {
            console.log('Password correct!');
        }
    }
}

