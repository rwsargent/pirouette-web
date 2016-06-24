import socket
from threading import Thread, Lock
import time
from constants import PI_HOST, PI_PORT
from flask_socketio import emit


error_lock = Lock()
reconnect_lock = Lock()
socket_handle = None
socket_error = False


def valid_socket():
    if error_lock.locked():
        return not socket_error


def connect_to_pi(from_thread = True):
    host = PI_HOST
    port = PI_PORT
    global socket_handle
    with reconnect_lock:
        try:
            print("Trying to connect to pi...")
                socket_handle = socket.socket()
                socket_handle.connect((host, port))
                print("Connected to Pi")
                send("Web Server connected...")
                socket_error = False
                return True
        except socket.error, e:
            print(str(e))
            if not from_thread:
                retry_connection_thread()
            return False


def send(msg):
    global socket_error
    with reconnect_lock:
        try:
            bytes_sent = socket_handle.send(msg)
            if bytes_sent == 0:
                print("The send failed, sent zero bytes to pi.")
                with error_lock:
                    socket_error = True
                    return
        except IOError as err:
            if err.errno == 32:
                emit("pidisconnect", "Broken pipe to pi", namespace='/pir')
                print("Broken pipe, attempting to reconnect...")
                retry_connection_thread()


def retry_connection_thread():
    def try_connect_on_interval():
        global socket_handle
        with reconnect_lock:
            socket_handle.close()
            while not connect_to_pi():
                print("Attempting to reconnect")
                time.sleep(4)
            emit("pireconnect", "Pi reconnected", namespace='/pir')
    Thread(target=try_connect_on_interval).start()
