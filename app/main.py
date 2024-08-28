from contextlib import asynccontextmanager
import random
from typing import List

from config.database import get_db_context
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from routers import company_router, task_router, user_router
from schemas.company_schema import CompanySchema
from schemas.task_schema import TaskSchema
from schemas.user_schema import UserSchema
from sqlalchemy import func, select
from sqlalchemy.orm import Session


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    db: Session = next(get_db_context())
    count = (
        db.query(func.count(getattr(UserSchema, "company_id")))
        .filter(getattr(UserSchema, "company_id").isnot(None))
        .scalar()
    )
    if count == 0:
        users = db.scalars(select(UserSchema)).all()
        tasks = db.scalars(select(TaskSchema)).all()
        companies = db.scalars(select(CompanySchema)).all()
        users_length = users.__len__()
        companies_length = companies.__len__()
        for t in tasks:
            if random.random() > 0.3:
                t.user = users[random.randrange(users_length)]
        for u in users:
            if random.random() > 0.2:
                u.company = companies[random.randrange(companies_length)]
        db.commit()
    db.close()

    yield

    # Code to run on shutdown
    db.close()


app = FastAPI(lifespan=lifespan)

add_pagination(app)
app.include_router(user_router.router)
app.include_router(company_router.router)
app.include_router(task_router.router)


@app.get("/")
async def main():
    return "Hello"
