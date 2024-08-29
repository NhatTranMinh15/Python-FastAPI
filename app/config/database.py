"""Database Config"""

import logging

from fastapi import Depends
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings

# Configure logging
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


def get_db_context():
    """
    Provides a synchronous database session context.

    This function creates a new database session and yields it.
    The session is closed after the context is exited.

    Yields:
        SessionLocal: A database session.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def get_async_db_context():
    """
    Provides an asynchronous database session context.

    This function creates a new asynchronous database session and yields it.
    The session is closed after the context is exited.

    Yields:
        AsyncSessionLocal: An asynchronous database session.
    """
    async with AsyncSessionLocal() as async_db:
        yield async_db


engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)
async_engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URL_ASYNC)

MetaData().create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSessionLocal = async_sessionmaker(async_engine, autocommit=False, autoflush=False)

Base = declarative_base()
db_dependency = Depends(get_db_context)
