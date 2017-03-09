# Import flask and template operators
from flask import Flask, render_template
from flask_socketio import SocketIO
import socket_layer as pi_socket

# Define the WSGI application object
app = Flask(__name__)
ws = SocketIO(app)

# Configurations
app.config.from_object('config')

pi_socket.launch_listen_thread()

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route("/")
def home():
    return render_template('home-page.html')


@ws.on('connect', namespace="/pir")
def on_connect():
    print("Web socket connected.")


@ws.on('disconnect', namespace="/pir")
def on_disconnect():
    print("Web socket disconnected")


@ws.on_error()
def on_ws_error(message):
    print("error" + message)


@ws.on('stop', namespace='/pir')
def stop(message):
    pi_socket.send("STOP\n")


@ws.on('left', namespace="/pir")
def turn_left(message):
    pi_socket.send("LEFT\n")
    print("Turn left " + str(message))


@ws.on('right', namespace="/pir")
def turn_right(message):
    pi_socket.send("RIGHT\n")
    print("Turn right " + str(message))
