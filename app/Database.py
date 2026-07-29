# ORM( Object relational Model ): > Instead of manually defining tables in postgres, we can define our tables as python models.
#                                 > Queries can be made exclusively through python code. No SQL is necessary.
# SQLALCHEMY : most popular python ORMs


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor #RealDictCursor: makes PostgreSQL return data as a dictionary instead of a tuple.
import time
from .config import settings
from urllib.parse import quote_plus

# SQLALCHEMY_DATABASE_URL = 'postgresql:// <username> : <password> @ <ip-address/hostname> / <database_name>'
# SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'  
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.database_username}:"
    f"{quote_plus(settings.database_password)}@"
    f"{settings.database_hostname}:"
    f"{settings.database_port}/"
    f"{settings.database_name}"
)
 # ***Password contain @ which sepeartes the string so use %40 instead of @ {@ -> %40}***
''' password is very case sensitive 💀'''

#engine: responsible for establsihing the connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# For talking to database default values
SessionLocal = sessionmaker( autocommit=False , autoflush=False, bind=engine)# ( does not automatically save changes , does not automatically push pending changes to the database.)

Base = declarative_base()

# Open a database connection when a request comes and close it automatically when the request finishes
def get_db():
    db = SessionLocal() # session is responsile for talking with the database
    try:
        yield db
    finally:
        db.close()


# psycopg2: is a Python library that allows Python to talk to PostgreSQL. (python -> psycopg2 -> postgres sql)
# while True:
#     try: 
#         conn = psycopg2.connect(host='localhost', database='postgres',user='postgres',
#                                 password='Pass@123',cursor_factory=RealDictCursor) 
#         cursor= conn.cursor() # Cursor is the thing that executes the sql queries  (python -> cursor -> postgres sql)
#         print("Database connection was succesfull!")
#         break
#     except Exception as error:
#         print("Connecting to database Failed !!!")
#         print("Error:",error)
#         time.sleep(2)

