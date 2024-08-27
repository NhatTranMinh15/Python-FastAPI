from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from models.task_model import CreateTaskRequestModel, TaskRequestModel
from schemas.task_schema import Priority, Status, TaskSchema
from services.exceptions import ResourceNotFoundException
from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session, joinedload
from services import user_service as UserService


def get_all_tasks(
    db: Session,
    task_request: TaskRequestModel,
    junction_type: str,
    status=List[Status],
    priority=List[Priority],
) -> Page[TaskSchema]:
    print(task_request.created_to)
    query = select(TaskSchema)
    conditions = []
    if task_request.id:
        conditions.append(TaskSchema.id == task_request.id)
    if status:
        conditions.append(TaskSchema.status.in_(status))
    if priority:
        conditions.append(TaskSchema.priority.in_(priority))
    if task_request.summary:
        conditions.append(TaskSchema.summary.like(f"%{task_request.summary}%"))
    if task_request.description:
        conditions.append(TaskSchema.description.like(f"%{task_request.description}%"))
    if not task_request.created_to:
        task_request.created_to = datetime.today()
    conditions.append(
        TaskSchema.created_at.between(
            task_request.created_from, task_request.created_to
        )
    )
    if junction_type == "OR":
        query = query.filter(or_(*conditions))
    elif junction_type == "AND":
        query = query.filter(and_(*conditions))
    return paginate(db, query)


def get_my_tasks(
    db: Session,
    user_id: UUID,
    task_request: TaskRequestModel,
    junction_type: str,
    status=List[Status],
    priority=List[Priority],
) -> Page[TaskSchema]:
    print(task_request.created_to)
    query = select(TaskSchema).filter(TaskSchema.user_id == user_id)
    conditions = []
    if task_request.id:
        conditions.append(TaskSchema.id == task_request.id)
    if status:
        conditions.append(TaskSchema.status.in_(status))
    if priority:
        conditions.append(TaskSchema.priority.in_(priority))
    if task_request.summary:
        conditions.append(TaskSchema.summary.like(f"%{task_request.summary}%"))
    if task_request.description:
        conditions.append(TaskSchema.description.like(f"%{task_request.description}%"))
    if not task_request.created_to:
        task_request.created_to = datetime.today()
    conditions.append(
        TaskSchema.created_at.between(
            task_request.created_from, task_request.created_to
        )
    )
    if junction_type == "OR":
        query = query.filter(or_(*conditions))
    elif junction_type == "AND":
        query = query.filter(and_(*conditions))
    return paginate(db, query)


def get_one_task(db: Session, task_id: UUID) -> TaskSchema:
    task = db.scalars(select(TaskSchema).filter(TaskSchema.id == task_id)).first()
    if not task:
        raise ResourceNotFoundException()
    return task


def create_task(db: Session, task_request: CreateTaskRequestModel):
    print(1)
    user = UserService.get_one_user_by_id(db, task_request.user_id)
    print(user)
    task_schema = TaskSchema(**task_request.model_dump())
    print(2, task_schema)
    # task_schema.user = user
    db.add(task_schema)
    print(3)
    db.commit()
    db.refresh(task_schema)
    return task_schema
