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


def connect_to_pi():
    host = PI_HOST
    port = PI_PORT
    global socket_handle, socket_error
    try:
        with error_lock:
            socket_handle = socket.socket()
            socket_handle.connect((host, port))
            socket_error = False
        return True
    except socket.error, e:
        print(str(e))
        with error_lock:
            socket_error = True
        return False


def send(msg):
    global socket_error
    bytes_sent = 0
    with reconnect_lock:
        while bytes_sent < len(msg):
            sent = socket_handle.send(msg[bytes_sent:])
            if sent == 0:
                print("this failed for whatever reason")
                with error_lock:
                    socket_error = True
                return
            bytes_sent = bytes_sent + sent


def retry_connection_thread():
    def try_connect_on_interval():
        global socket_handle
        with reconnect_lock:
            socket_handle.close()
            while not connect_to_pi():
                time.sleep(4)
            emit("reconnected", "RECONNECTED", namespace='/pir')
    Thread(target=try_connect_on_interval).start()
