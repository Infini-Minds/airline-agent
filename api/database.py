import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

# Fetch environment variables (using POSTGRES_* naming convention)
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
HOST = os.getenv("POSTGRES_HOST")
PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB")

# Ensure required env vars are present
if not all([USER, PASSWORD, HOST, DB_NAME]):
    raise EnvironmentError("Missing required PostgreSQL environment variables. Check .env file.")

# URL-encode the password to handle special characters like '@'
password_enc = quote_plus(PASSWORD)

# Construct the async connection URL (using asyncpg driver)
# Format: postgresql+asyncpg://user:password@host:port/dbname
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{USER}:{password_enc}@{HOST}:{PORT}/{DB_NAME}"

# Create async engine
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    echo=False
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
