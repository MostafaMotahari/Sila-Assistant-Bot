"""Session of postgresql"""

# Imports
from typing import Generator
from decouple import config

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(config("DB_URL"))
local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator:
    try:
        db = local_session()
        yield db
    finally:
        db.close()


# Temporary databsae
TEMP_DATA = []
