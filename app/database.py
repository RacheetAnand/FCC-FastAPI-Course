# Copied from -> https://fastapi.tiangolo.com/tutorial/sql-databases/

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:dipasha321@localhost/FastAPI"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(
    # SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} # Only for SQLite as it is running in Memory.
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Previously in the main.py file :
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



import psycopg2
from psycopg2.extras import RealDictCursor
import time


while True:
    # Hard Coding the Passwords and all are generally not advisable.
    try:
        # conn = psycopg2.connect(host = 'localhost', database = 'FastAPI', user = 'postgres', password = 'dipasha321', cursor_factory = RealDictCursor)
        conn = psycopg2.connect(host = settings.database_hostname, database = settings.database_name, user = settings.database_username, password = settings.database_password, cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection was Successfull !!")
        break
    except Exception as error:
        print("Database Connection was Failed !")
        print("Error : ", error)
        time.sleep(2)

