from flask import Flask, render_template
from threading import Thread
import _logging as logging

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.env = 'development'

PORT = 4200

@app.route('/')
def index():
    return render_template('index.html',
                            title='Dubois',
                            greeting="Hi, I'm Dubois 🤖",
                            instructions='Drag your thumb across the screen to move me around.',
                            debug=True)

def start():
    Thread(target=app.run,
            args=('0.0.0.0', PORT),
            kwargs=dict(debug=True, use_reloader=False)) \
            .start()
    logger.info("Web server started.")
