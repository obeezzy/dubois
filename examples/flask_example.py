from flask import Flask, render_template, make_response
    
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def hello_world():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)
