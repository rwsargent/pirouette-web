#from app import app, ws
import app as pirouette
import app.socket_layer as pi_socket

# app.run(host='localhost', port=8080, debug=True)
pirouette.ws.run(pirouette.app)


