import socket
from threading import Thread, Lock
from time import sleep
from constants import PI_HOST, PI_PORT
from flask_socketio import emit

#Locks for threading
error_lock = Lock()
reconnect_lock = Lock()
socket_handle = None
socket_error = False

#Unused?
def valid_socket():
    if error_lock.locked():
        return not socket_error

def send(msg):
    '''
    
    '''
    global socket_error
    if not socket_handle:
        print("The message " + msg + " wasn't sent because there isn't a socket to send it on.")
        return
    try:
        bytes_sent = socket_handle.send(msg)
        if bytes_sent == 0:
            print("The send failed, sent zero bytes to pi.")
            with error_lock:
                socket_error = True
                return
        else:
          emit("success", "Connected!")
    except IOError as err:
        errorMsg = ""
        if err.errno == 32:
            errorMsg = "Broken pipe, attempting to reconnect..."
        else:
            errorMsg = "Unknown error " + str(err.errno) + ", still attempting to reconnected..."
        print(errorMsg)
        emit("pidisconnect",errorMsg)
        
        #launch_connection_thread(cb = emit_callback)
        launch_listen_thread()

def launch_listen_thread(**kwarg):
    def pi_listen():
        global socket_handle
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind(("0.0.0.0", 5676))
        serversocket.listen(5)
        print("Accepting...")
        (connected_socket, address) = serversocket.accept()
        print("Accepted on address: " + str(address))
        socket_handle = connected_socket
        #close listening socket
#        emit("connect", "Connected!")
        serversocket.close()
    listening = Thread(target=pi_listen)
    listening.daemon = True
    listening.start()
        

def launch_connection_thread(**kwarg):
    def try_connect_on_interval(cb):
            global socket_handle
            if socket_handle:
                socket_handle.close()
            while not connect_to_pi():
                print("Attempting to reconnect")
                sleep(4)
            print("Reconnected to pi")
            
    if not reconnect_lock.locked():
        with reconnect_lock:
            Thread(target=try_connect_on_interval, args=(kwarg['cb'])).start()


def connect_to_pi():
    host = PI_HOST
    port = PI_PORT
    global socket_handle
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
        return False
