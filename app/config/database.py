from fastapi import Depends
from config import settings
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

# Configure logging
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


def get_db_context():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def get_async_db_context():
    async with AsyncSessionLocal() as async_db:
        yield async_db


engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)
async_engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URL_ASYNC)

metadata = MetaData().create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSessionLocal = async_sessionmaker(async_engine, autocommit=False, autoflush=False)

Base = declarative_base()
db_dependency = Depends(get_db_context)
