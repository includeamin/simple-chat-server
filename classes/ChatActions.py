from classes.Authentication import Authentication
from models.Packets import *
from database.DB import Chat as ChatDb, session
from sqlalchemy import and_
from models.User import UserChatHistoryModel
from models.User import UserUnreadMessage, UserMessagesResponse


class ChatActions:
    @staticmethod
    def add_message(packet: DirectMessageDataModel):
        # get sender username from token
        sender_username = Authentication.validate_jwt(packet.token)
        # create full package to send and save in database
        data = MessagePacket(sender_username=sender_username, receiver_username=packet.receiver,
                             content_type=packet.content_type, content=packet.content)
        message_in_db = ChatDb(sender_username=data.sender_username,
                               receiver_username=data.receiver_username,
                               content=data.content,
                               content_type=data.content_type,
                               is_seen=False,
                               create_at=data.create_at)
        session.add(message_in_db)
        session.commit()
        data.id = message_in_db.id
        data.create_at = data.create_at.timestamp()
        return data

    @staticmethod
    def seen_message(message_id: int):
        session.query(ChatDb).filter(and_(ChatDb.id <= message_id, ChatDb.is_seen == False)).update(
            {ChatDb.is_seen: True},
            synchronize_session=False)
        session.commit()

    @staticmethod
    def get_user_un_saw_messages(username: str) -> dict:
        messages = session.query(ChatDb).filter(and_(ChatDb.sender_username == username, ChatDb.is_seen == False))
        response = UserMessagesResponse(messages=[])
        for message in messages:
            response.messages.append(UserUnreadMessage(**message.__dict__))
        if response.messages:
            last_message_id = response.messages[-1].id
            ChatActions.seen_message(last_message_id)
        return response.dict()

    @staticmethod
    def get_messages_with_other_user(username: str, other_username: str) -> dict:
        messages = session.query(ChatDb).filter(
            and_(ChatDb.sender_username == username, ChatDb.receiver_username == other_username))
        response = UserChatHistoryModel()
        for message in messages:
            response.messages.append(MessagePacket(**message.__dict__))
        return response.dict()
