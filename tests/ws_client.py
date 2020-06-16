import socketio
from models.Packets import *


amin_jamal_token = ''

includeamin_token = ''

sio = socketio.Client()
sio.connect(
    f'http://localhost:3000?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZS'
    'I6ImFtaW5qYW1hbCIsImNhIjoxNTkyMjI1Mj'
    'EyLjI2NjEyMywiZXgiOjE1OTI4MzAwMTIuMjY2MTQ2fQ.oylQVWwJRna29Xj9rAz4RskEwm8bUlI8wdUs2CCmAy4')


@sio.on('my_response')
def on_message(data):
    print(data)
    print('I received a message!')


@sio.on('direct_message')
def on_message(data):
    print(data)
    message = MessagePacket(**data)
    print('I received a direct message!')
    sio.emit("seen", {"id": message.id})


# packet = DirectMessageDataModel()
packet = {
    'token': includeamin_token, 'receiver': 'aminjamal', 'content_type': "text",
    'content': "salam chetori"
}
# for item in range(10):
#     sio.emit('message', {'foo': 'bar'})
sio.emit('message', packet)
