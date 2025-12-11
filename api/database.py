import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Fetch environment variables
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
HOST = os.getenv("POSTGRES_HOST")
PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB")

# Construct the connection URL (including SSL mode for Azure)
# Format: postgresql://user:password@host:port/dbname?sslmode=require
from urllib.parse import quote_plus

# Ensure required env vars are present
if not all([USER, PASSWORD, HOST, DB_NAME]):
    raise EnvironmentError("Missing required PostgreSQL environment variables. Check .env file.")

# URL‑encode the password to handle special characters like '@'
password_enc = quote_plus(PASSWORD)

# Construct the connection URL (including SSL mode for Azure)
# Format: postgresql://user:password@host:port/dbname?sslmode=require
sslmode = os.getenv("POSTGRES_SSLMODE", "require")
SQLALCHEMY_DATABASE_URL = f"postgresql://{USER}:{password_enc}@{HOST}:{PORT}/{DB_NAME}?sslmode={sslmode}"

# Azure Postgres often requires SSL mode
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
