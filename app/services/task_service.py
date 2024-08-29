"""User Services"""
from datetime import datetime
from typing import List
from uuid import UUID

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session

from models.task_model import CreateTaskRequestModel, TaskRequestModel
from schemas.task_schema import Priority, Status, TaskSchema
# from schemas.user_schema import UserSchema
from services import user_service as UserService
from services.exceptions import ResourceNotFoundException


def get_all_tasks(
    db: Session,
    task_request: TaskRequestModel,
    junction_type: str,
    # user_token:UserSchema,
    status=List[Status],
    priority=List[Priority],
) -> Page[TaskSchema]:
    """Get All Tasks

    Args:
        db (Session): Database Session
        task_request (TaskRequestModel): Filter Parameter
        junction_type (str): Parameters join type. Either "AND" or "OR". Default to "AND"
        # user_token (UserSchema): _description_
        status (_type_, optional): status filter
        priority (_type_, optional): priority filter

    Returns:
        Page[TaskSchema]: One Page of Tasks
    """
    query = select(TaskSchema)
    conditions = []
    if task_request.id:
        conditions.append(TaskSchema.id == task_request.id)
    if task_request.user_id:
        conditions.append(TaskSchema.user_id == task_request.user_id)
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
    """Get One Task

    Args:
        db (Session): Database Session
        task_id (UUID): Task ID

    Raises:
        ResourceNotFoundException

    Returns:
        TaskSchema: Task information
    """
    task = db.scalars(select(TaskSchema).filter(TaskSchema.id == task_id)).first()
    if not task:
        raise ResourceNotFoundException()
    return task


def create_task(db: Session, task_request: CreateTaskRequestModel) -> TaskSchema:
    """Create one task

    Args:
        db (Session): Database Session
        task_request (CreateTaskRequestModel): Task infomation

    Returns:
        TaskSchema: Newly created task
    """
    if task_request.user_id:
        UserService.get_one_user(db, "id", task_request.user_id)
    task_request.status = Status.OPEN
    if not task_request.priority:
        task_request.priority = Priority.MEDIUM
    task_schema = TaskSchema(**task_request.model_dump())
    db.add(task_schema)
    db.commit()
    db.refresh(task_schema)
    return task_schema


def update_task(
    db: Session, task_id: UUID, task_request: CreateTaskRequestModel, remove_user: bool
)-> TaskSchema:
    """Update one task

    Args:
        db (Session): Database Sesion
        task_id (UUID): Task ID to be updated
        task_request (CreateTaskRequestModel): Task update information
        remove_user (bool): Remove user from task

    Returns:
        TaskSchema: Updated Task
    """
    task = get_one_task(db, task_id)
    if remove_user:
        task.user = None
    elif task_request.user_id:
        user = UserService.get_one_user(db, "id", task_request.user_id)
        task.user = user
    if task_request.summary:
        task.summary = task_request.summary
    if task_request.description:
        task.description = task_request.description
    if task_request.status:
        task.status = task_request.status
    if task_request.priority:
        task.priority = task_request.priority

    db.commit()
    db.refresh(task)

    return task


def delete_task(db: Session, task_id: UUID):
    """Delete one task

    Args:
        db (Session): Database Sesion
        task_id (UUID): Task ID to be deleted
    """
    task = get_one_task(db, task_id)
    db.delete(task)
    db.commit()
