from flask import request
from flask_socketio import Namespace, emit, join_room
from classes.Authentication import Authentication
from models.Packets import *
from classes.ChatActions import ChatActions


class ChatNamespace(Namespace):
    def on_connect(self):
        data = Authentication.validate_jwt(request.args.get("token").encode('utf-8'))
        join_room(data, request.sid)
        emit("server_response", {"username": data, "sid": request.sid})
        print(f'{data} connected')

    def on_disconnect(self):
        print("disconnect")

    def on_message(self, data):
        packet = DirectMessageDataModel(**data)
        message_packet = ChatActions.add_message(packet)
        emit("direct_message", message_packet.dict(), room=packet.receiver)
        emit('server_response', data)

    def on_seen(self, data):
        packet = SeenModel(**data)
        ChatActions.seen_message(packet.id)

    def in_my_response(self, data):
        print(data)
        print('I received a message!')
