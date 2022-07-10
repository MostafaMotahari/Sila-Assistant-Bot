from sqlalchemy.orm import Session
from sqlalchemy import exists

from base.sql.models import UserModel
from base.sql.session import get_db

# Get Users List
def get_users_list(db: Session):
    users_list_tuple = db.query(UserModel.user_id).filter(UserModel.is_banned == False).all()
    users_list = []
    for user in users_list_tuple:
        users_list.append(user[0])
    return users_list


# Check user exist
def check_user_exist(user_id):
    db_session = get_db().__next__()
    return True if db_session.query(exists().where(UserModel.user_id == user_id)).scalar() else False


# Get a user
def get_user(db: Session, user_id, get_fisrt=True):
    if get_fisrt:
        user = db.query(UserModel).filter(UserModel.user_id == user_id).first()
        return user

    user = db.query(UserModel).filter(UserModel.user_id == user_id)
    return user


# Controling details of searching
def search_details_control(user_id, count=1):
    db_session = get_db().__next__()
    user = db_session.query(UserModel).filter(UserModel.user_id == user_id).first()
    
    if user:
        user.total_searches += count
        user.search_credit -= count
        db_session.commit()
        return user
    
    return False
