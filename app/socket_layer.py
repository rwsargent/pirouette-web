import socket


SOCKET_PORT = 3490
SOCKET_HOST = "192.168.1.6"


def connect_to_pi():
    s = socket.socket()
    host = SOCKET_HOST
    port = SOCKET_PORT
    s.connect((host, port))
    return s