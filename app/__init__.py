# Import flask and template operators
from flask import Flask, render_template
from flask_socketio import SocketIO
import socket_layer as pi_socket

# Define the WSGI application object
app = Flask(__name__)
ws = SocketIO(app)

# Configurations
app.config.from_object('config')

# Sample HTTP error handling
# @app.errorhandler(404)
# def not_found(error):
#     return render_template('404.html'), 404

pi_socket.connect_to_pi()


@app.route("/")
def home():
    return render_template('home-page.html')


@ws.on('connect', namespace="/pir")
def on_connect():
    print("connected")


@ws.on('disconnect', namespace="/pir")
def on_disconnect():
    print("disconnected")


@ws.on_error()
def on_ws_error(message):
    print("error" + message)


@ws.on('stop', namespace='/pir')
def stop(message):
    pi_socket.send("STOP")


@ws.on('left', namespace="/pir")
def turn_left(message):
    pi_socket.send("LEFT")
    print("Turn left " + str(message))


@ws.on('right', namespace="/pir")
def turn_right(message):
    pi_socket.send("RIGHT")
    print("Turn right " + str(message))
