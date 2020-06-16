from api.User import user_routes
from flask import Flask, request
from flask_socketio import SocketIO, join_room, emit, send
from flask_cors import CORS
import eventlet
from classes.ChatNamespace import ChatNamespace

eventlet.monkey_patch()

app = Flask(__name__)
CORS(app)
# socket_io = SocketIO(message_queue='redis://message_queue='redis://')  # when we have multiply workers or behind the
# proxy servers

socket_io = SocketIO(app)
socket_io.init_app(app, cors_allowed_origins="*"
                   # ,
                   # message_queue='redis://'
                   )


@socket_io.on_error(namespace="/")  # Handles the default namespace
def error_handler(e):
    print('error', e)
    # emit("my_response", {"code": 406, "message": e})



socket_io.on_namespace(ChatNamespace('/'))

app.register_blueprint(user_routes, url_prefix='/user')

if __name__ == '__main__':
    socket_io.run(app, host='0.0.0.0', port=3000, debug=True)
