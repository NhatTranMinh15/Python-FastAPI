"""task Router"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from fastapi_pagination import Page
from sqlalchemy.orm import Session
from starlette import status

from config.database import db_dependency
from models.task_model import (
    CreateTaskRequestModel,
    TaskRequestModel,
    TaskResponseModel,
)
from schemas.task_schema import Priority, Status
from schemas.user_schema import UserSchema
from services import auth_service as AuthService
from services import task_service as TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("", status_code=status.HTTP_200_OK, response_model=Page[TaskResponseModel])
async def get_all_tasks(
    task_request: TaskRequestModel = Depends(),
    junction_type: str = Query(default="AND"),
    statuses: Optional[List[Status]] = Query(None),
    priorities: Optional[List[Priority]] = Query(None),
    db: Session = db_dependency,
    user_token: UserSchema = Depends(
        AuthService.get_token_interceptor(allow_user=True)
    ),
):
    """
    Retrieves a paginated list of tasks based on the provided filters.

    Args:
        task_request (TaskRequestModel): The request model containing task filters.
        junction_type (str): The type of junction for combining filters. Default is "AND".
        statuses (Optional[List[Status]]): A list of statuses to filter tasks.
        priorities (Optional[List[Priority]]): A list of priorities to filter tasks.
        db (Session): The database session dependency.
        user_token (UserSchema): The user token for authentication.

    Returns:
        Page[TaskResponseModel]: A paginated list of tasks.
    """
    tasks = TaskService.get_all_tasks(
        db,
        task_request,
        junction_type,
        user_token,
        statuses,
        priorities,
    )
    return tasks


@router.get(
    "/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskResponseModel
)
async def get_one_task(
    task_id: UUID,
    db: Session = db_dependency,
    user_token: UserSchema = Depends(
        AuthService.get_token_interceptor(allow_user=True)
    ),
):
    """
    Retrieves details of a specific task by its ID.

    Args:
        task_id (UUID): The unique identifier of the task.
        db (Session): The database session dependency.
        user_token (UserSchema): The user token for authentication.

    Returns:
        TaskResponseModel: The details of the task.
    """
    return TaskService.get_one_task(db, task_id)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TaskResponseModel)
async def create_task(
    task_request: CreateTaskRequestModel,
    db: Session = db_dependency,
    user_token: UserSchema = Depends(
        AuthService.get_token_interceptor(allow_user=True)
    ),
):
    """
    Retrieves details of a specific task by its ID.

    Args:
        task_id (UUID): The unique identifier of the task.
        db (Session): The database session dependency.
        user_token (UserSchema): The user token for authentication.

    Returns:
        TaskResponseModel: The details of the task.
    """
    return TaskService.create_task(db, task_request)


@router.put(
    "/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskResponseModel
)
async def update_task(
    task_id: UUID,
    task_request: CreateTaskRequestModel,
    r: bool = False,
    db: Session = db_dependency,
    user_token: UserSchema = Depends(
        AuthService.get_token_interceptor(allow_user=True)
    ),
):
    """
    Updates details of a specific task.

    Args:
        task_id (UUID): The unique identifier of the task.
        task_request (CreateTaskRequestModel): The request model containing updated task details.
        r (bool): Flag to indicate if the user should be removed. Default is False.
        db (Session): The database session dependency.
        user_token (UserSchema): The user token for authentication.

    Returns:
        TaskResponseModel: The updated details of the task.
    """
    return TaskService.update_task(db, task_id, task_request, remove_user=r)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    db: Session = db_dependency,
    user_token: UserSchema = Depends(
        AuthService.get_token_interceptor(allow_user=True)
    ),
):
    """
    Deletes a specific task by its ID.

    Args:
        task_id (UUID): The unique identifier of the task.
        db (Session): The database session dependency.
        user_token (UserSchema): The user token for authentication.

    Returns:
        None
    """
    return TaskService.delete_task(db, task_id)
