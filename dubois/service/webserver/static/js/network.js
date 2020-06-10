export class DuboisClient {
    constructor(serverAddress=document.domain, serverPort=4201) {
        this.ws = new WebSocket('ws://' + serverAddress + ':' + serverPort);
        this.ws.onopen = () => console.log("Socket opened.");
        this.ws.onerror = (error) => console.log('WebSocket error:', error);
        this.ws.onmessage = (event) => this._recv(event.data);
        this.ws.onclose = (event) => console.log('WebSocket closed. Reason:', event.code);
        this.onrecv = (remoteState) => { };
    }

    send(remoteEvent) {
        if (Object(remoteEvent).hasOwnProperty('action')) {
            console.log('Event sent:', remoteEvent.toString());
            this.ws.send(remoteEvent);
        } else {
            console.error('No action specified.');
        }
    }

    _recv(remoteState) {
        remoteState = JSON.parse(remoteState)
        console.log('State received:', remoteState);
        this.onrecv(remoteState);
    }
}
