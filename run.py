#from app import app, ws
import app as pirouette

# app.run(host='localhost', port=8080, debug=True)
pirouette.ws.run(pirouette.app)
