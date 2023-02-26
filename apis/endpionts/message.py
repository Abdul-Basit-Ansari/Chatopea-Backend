from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Security import deps
from crud import message as crud_message
from crud import user as crud_user
from config.api import settings
from Schemas.schemas import MessageCreate , User
router = APIRouter()


@router.post("/", response_model=MessageCreate)
def new_message(
    message: MessageCreate, db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)):   
    try:
        result = crud_message.new_message(db=db, current_user=current_user,message=message)
        return result
    except Exception as err:
        raise err

@router.get("/{user_id}")
def get_chat_messages(user_id : int, current_user: User = Depends(deps.get_current_active_user) ,db: Session = Depends(deps.get_db)):   
    try:
        result = crud_message.get_chat_messages_by_user_id(db=db, sender_id=current_user.id , receiver_id=user_id)
        return result
    except Exception as err:
        err

@router.get("/allMessages/{user_id}")
def get_all_messages(user_id : int, current_user: User = Depends(deps.get_current_active_user) ,db: Session = Depends(deps.get_db)):   
    try:
        result = crud_message.get_all_messages_by_user_id(db=db, user_id=user_id)
        return result
    except Exception as err:
        err

@router.get("/sendMessages/{user_id}")
def get_send_messages(user_id : int, current_user: User = Depends(deps.get_current_active_user) ,db: Session = Depends(deps.get_db)):   
    try:
        result = crud_message.get_send_messages_by_user_id(db=db, user_id=user_id)
        return result
    except Exception as err:
        err

@router.get("/receiveMessages/{user_id}")
def get_receive_messages(user_id : int , current_user: User = Depends(deps.get_current_active_user),db: Session = Depends(deps.get_db)):   
    try:
        result = crud_message.get_receive_messages_by_user_id(db=db, user_id=user_id)
        return result
    except Exception as err:
        err


@router.delete("/{message_id}")
def delete_message(
    message_id : int,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)):   
    try:
        result = crud_message.delete_message(db=db, message_id=message_id , user_sender=current_user.id)
        return result
    except Exception as err:
        raise err
