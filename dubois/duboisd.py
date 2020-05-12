#!/usr/bin/python3

from flask import Flask, render_template
from flask_socketio import SocketIO, emit, disconnect
from transducers.output import Wheels

app = Flask(__name__, template_dir='public_html')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=None)

wheels = Wheels()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('parcel', namespace='/test')
def test_message(message):
    print("Message received:", message['data'])

@socketio.on('forward', namespace='/test')
def move_forward(message):
    print('Move forward', message)
    if message['activated']:
        wheels.move_forward()
    else:
        wheels.stop()

@socketio.on('backward', namespace='/test')
def move_backward(message):
    print('Move backward', message)
    if message['activated']:
        wheels.move_backward()
    else:
        wheels.stop()

@socketio.on('clockwise', namespace='/test')
def move_clockwise(message):
    print('Move clockwise', message)
    if message['activated']:
        pass
        wheels.move_clockwise()
    else:
        wheels.stop()

@socketio.on('counterclockwise', namespace='/test')
def move_counterclockwise(message):
    print('Move counterclockwise', message)
    if message['activated']:
        pass
        wheels.move_counterclockwise()
    else:
        wheels.stop()

if __name__ == '__main__':
    try:
        socketio.run(app, debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        wheels.shutdown()
