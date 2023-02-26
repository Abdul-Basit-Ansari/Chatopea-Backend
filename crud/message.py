from sqlalchemy.orm import Session
from sqlalchemy import or_ , and_
from fastapi import HTTPException

from config.api import settings
import db.models as models
import Schemas.schemas as schemas



def new_message(
        db: Session,
        current_user,
        message: schemas.MessageCreate,
        ):
    try:
        if current_user.id == message.receiver_id:
            raise HTTPException(400 , detail="You Cant Sent Message To You.")    
        db_message = models.Message(
            message = message.message,
            seen = message.seen,
            is_delete = message.is_delete,
            sender_id = current_user.id,
            receiver_id = message.receiver_id
            )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message
    except Exception as err:
        raise err

def delete_message(
        db: Session,
        message_id: int,
        user_sender: int,
        ):
    msg = db.query(models.Message).filter(models.Message.id == message_id , models.Message.sender_id == user_sender).first()
    try:
        if msg :
            db.query(models.Message).filter(models.Message.id == message_id , models.Message.sender_id == user_sender).delete()
        else :
            raise HTTPException(403 , "You Can Only Delete Your Messages")    
        db.commit()
        return "Message Deleted."
    except Exception as err:
        raise err

def get_all_messages_by_user_id(db: Session, user_id: str):
    try:       
        msgs = db.query(models.Message).filter(or_(models.Message.sender_id == user_id , models.Message.receiver_id == user_id)).all()
        return msgs
    except Exception as err:
        raise err


        
def get_chat_messages_by_user_id(db: Session, sender_id: str , receiver_id: str):
    try:       
        msgs = db.query(models.Message).filter(and_(or_(models.Message.sender_id == sender_id ,models.Message.sender_id == receiver_id) , or_(models.Message.receiver_id == sender_id,models.Message.receiver_id == receiver_id))).order_by(models.Message.id).all()
        return msgs
    except Exception as err:
        raise err


        
def get_send_messages_by_user_id(db: Session, user_id: str):
    try:       
        msgs = db.query(models.Message).filter(models.Message.sender_id == user_id).all()
        return msgs
    except Exception as err:
        raise err


        
def get_receive_messages_by_user_id(db: Session, user_id: str):
    try:       
        msgs = db.query(models.Message).filter(models.Message.receiver_id == user_id).all()
        return msgs
    except Exception as err:
        raise err


