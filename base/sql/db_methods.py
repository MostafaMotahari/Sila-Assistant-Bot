from sqlalchemy.orm import Session
from sqlalchemy import exists
from pyrogram.types import User

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
def get_user(user_id: int = None, username: str = None):
    db_session = get_db().__next__()
    if user_id:
        user = db_session.query(UserModel).filter(UserModel.user_id == user_id).first()
    else:
        user = db_session.query(UserModel).filter(UserModel.username == username).first()

    return user if user else None

# Update a user
def update_user(user: UserModel):
    db_session = get_db().__next__()
    user_obj = db_session.query(UserModel).filter(UserModel.user_id == user.user_id).first()
    user_obj = user
    db_session.commit()
    # db_session.refresh(user_obj)
    

# Add user
def add_user(user: User, is_admin: bool, is_superuser: bool):
    db_session = get_db().__next__()
    user_obj = UserModel(
        user_id=user.id,
        username=user.username,
        is_admin=is_admin,
        is_superuser=is_superuser
    )
    print(user_obj.__dict__)
    db_session.add(user_obj)
    db_session.commit()
    db_session.refresh(user_obj)

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

# First run migrations
def migrations():
    db_session = get_db().__next__()
    user = UserModel(
        user_id=3234234,
        username="slkdfjlsdkfj",
        is_admin=True
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)