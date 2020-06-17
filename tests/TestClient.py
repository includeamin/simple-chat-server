import socketio
import requests
import sys
from pydantic import BaseModel
from datetime import datetime
from typing import Any
import pprint

base_url = "http://localhost:3000/"


class MessagePacket(BaseModel):
    id: int = None
    sender_username: str
    receiver_username: str
    content_type: str
    content: Any
    create_at: datetime = datetime.now()


def login_get_token(user, password):
    result = requests.post(f"{base_url}user/{action}", json={
        "username": user,
        "password": password
    })
    if result.status_code != 200:
        print(result.content)
        exit(1)
    return result.json()["Authorization"]


def get_new_messages():
    result = requests.get(f"{base_url}user/messages/unread", headers={'Authorization': token})
    assert result.status_code == 200
    result = result.json()
    pprint.pprint(result)


if len(sys.argv) < 4:
    print("please enter username and password")
    exit(1)
action = sys.argv[1]
if action.lower() not in ['signup', 'login']:
    print("invalid action, valid actions are login and signup")
    exit(1)

u = sys.argv[2]
p = sys.argv[3]
token = login_get_token(u, p)

# token = login_get_token(u, p)
get_new_messages()
sio = socketio.Client()
sio.connect(
    f'{base_url}?token={token}')


@sio.on('my_response')
def on_message(data):
    print(data)
    print('I received a message!')


@sio.on('direct_message')
def on_message(data):
    message = MessagePacket(**data)
    print(f'\n{message.sender_username} says: {message.content}')
    sio.emit("seen", {"id": message.id})


while True:
    message = input("Enter the Message: ")
    receiver_username = input("Receiver username: ")
    packet = {
        'token': token, 'receiver': receiver_username, 'content_type': "text",
        'content': message
    }
    sio.emit('message', packet)
