# https://medium.com/@swaroopkml96/deploying-your-p5-js-sketch-using-flask-on-heroku-8702492047f5
# https://gabrieltanner.org/blog/realtime-drawing-app/

from flask import Flask, render_template, url_for, send_from_directory
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 's3cr3t'
bootstrap = Bootstrap(app)
socketio = SocketIO(app)

currentState = {}

### Sockets
@socketio.on("message")
def handle_message(data):
    print("Message received: {0}".format(data))

@socketio.on("connected")
def handle_connection(data):
    global currentState
    print("User connected: {0}".format(data))

    if currentState != {}:
        socketio.emit('set initial data', {'bgColor': currentState})

@socketio.on("bgColor")
def handle_connection(data):
    global currentState

    currentState = data
    print("Color received: {0}".format(data))
    socketio.emit('new bgColor', {'bgColor': data}, include_self=False)#, broadcast=True)

### Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == "__main__":
    socketio.run(app, port=8081)
    # app.run(debug=True)