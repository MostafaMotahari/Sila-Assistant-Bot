from sqlalchemy.orm import Session

from base.sql.models import UserModel
from base.sql.session import TEMP_DATA

# Get Users List
def get_users_list(db: Session):
    users_list_tuple = db.query(UserModel.user_id).filter(UserModel.is_banned == False).all()
    users_list = []
    for user in users_list_tuple:
        users_list.append(user[0])
    return users_list


# Get a user
def get_user(db: Session, user_id, get_fisrt=True):
    if get_fisrt:
        user = db.query(UserModel).filter(UserModel.user_id == user_id).first()
        return user

    user = db.query(UserModel).filter(UserModel.user_id == user_id)
    return user

# Change a user
def change_user(db: Session, new_user: UserModel):
    old_user = get_user(db, new_user.user_id, False).first()
    
    if old_user:
        old_user = new_user
        db.commit()
        return new_user
    
    return False


# Signup new User
def sign_up(db: Session, user_id: int, first_search=False):
    if first_search:
        user = UserModel(
            user_id = user_id,
            total_searches = 1
        )

    else:
        user = UserModel(
            user_id = user_id,
            total_searches = 0
        )

    # Add user in temporary database
    global TEMP_DATA
    TEMP_DATA.append(user_id)

    db.add(user)
    db.commit()
    db.refresh(user)


# Controling details of searching
def search_details_control(db: Session, user_id, count=1):
    user = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    
    if user:
        user.total_searches += count
        user.search_credit -= count
        #user.update(user)
        db.commit()
        return user
    
    return False
