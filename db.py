import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SSL_CERT_PATH = os.path.join(BASE_DIR, "isrgrootx1.pem")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={
        "ssl": {
            "ca": SSL_CERT_PATH
        }
    }
)

sessionLocal = sessionmaker(bind=engine)
Base = declarative_base()