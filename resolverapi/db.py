import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session

def db_session():
    engine = create_engine(
        os.getenv('DATABASE_URL'),
        echo=os.getenv('DATABASE_ECHO', '').lower() == 'true'
    )

    session = scoped_session(sessionmaker(bind=engine))  