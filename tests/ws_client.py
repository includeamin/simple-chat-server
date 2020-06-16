import socketio
from models.Packets import *


amin_jamal_token = ''

includeamin_token = ''

sio = socketio.Client()
sio.connect(
    f'http://localhost:3000?token={includeamin_token}')


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
