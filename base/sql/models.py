from enum import unique
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean
)

from base.sql.base_class import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    total_searches = Column(Integer, unique=False, nullable=False, default=0)
    search_credit = Column(Integer, unique=False, nullable=False, default=5)
    is_admin = Column(Boolean, unique=False, nullable=False, default=False)
    is_superuser = Column(Boolean, unique=False, nullable=False, default=False)
    is_banned = Column(Boolean, unique=False, nullable=False, default=False)