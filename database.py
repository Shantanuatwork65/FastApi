from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_url='mysql+pymysql://root:54321@localhost/fastapi_db'

engine=create_engine(db_url)
session=sessionmaker(autoflush=False,autocommit=False,bind=engine)

