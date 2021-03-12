from config import config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

hostname = config.get("postgres.hostname")
database = config.get("postgres.database")
user = config.get("postgres.user")
password = config.get("postgres.password", "")

db_url = config.get("postgres.db_url").format(
    user=user, password=password, database=database, hostname=hostname
)
engine = create_engine(db_url, pool_size=2, max_overflow=1)

Session = sessionmaker(bind=engine)

Base = declarative_base()


def get_session():
    return Session()


def return_session(session):
    session.close()
