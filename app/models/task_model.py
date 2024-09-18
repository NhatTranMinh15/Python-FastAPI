"""Task Model"""

from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from models.user_model import UserResponseModel
from schemas.task_schema import Priority, Status


class TaskModel(BaseModel):
    """Task Model"""

    id: UUID
    summary: str
    description: str
    status: Status = Field(default=Status.OPEN)
    priority: Priority = Field(default=Priority.MEDIUM)


class OrderBy(str, Enum):
    """_summary_

    Args:
        str (_type_): _description_
        Enum (_type_): _description_
    """
    id = "id"
    summary = "summary"
    created_at = "created_at"


class TaskRequestModel(BaseModel):
    """
    Model for handling task request parameters.

    Attributes:
        id (Optional[UUID]): The unique identifier of the task.
        user_id (Optional[UUID]): The unique identifier of the user associated with the task.
        summary (Optional[str]): A part summary of the task.
        description (Optional[str]): A part description of the task.
        created_from (Optional[datetime]): The start datetime for filtering tasks. Default is January 1, 1970.
        created_to (Optional[datetime]): The end datetime for filtering tasks. Default is now, created at the time of request
        all (Optional[bool]): Get all other user tasks. Default is false. Only admin can use this feature
        page (int): The page number for pagination. Default is 1.
        size (int): The number of items per page for pagination. Default is 15.
    """

    id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    summary: Optional[str] = ""
    description: Optional[str] = ""
    created_from: Optional[datetime] = datetime(1970, 1, 1, 0, 0, 1)
    created_to: Optional[datetime] = None
    all: bool = False
    page: int = 1
    size: int = 15
    order_by: OrderBy = OrderBy.id
    order_dir: bool = False


class CreateTaskRequestModel(BaseModel):
    """
    Model for creating a new task.

    Attributes:
        summary (Optional[str]): A brief summary of the task.
        description (Optional[str]): A detailed description of the task.
        priority (Optional[Priority]): The priority level of the task.
        user_id (UUID): The unique identifier of the user associated with the task.
        status (Optional[Status]): The current status of the task.
    """

    summary: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[Priority] = None
    user_id: UUID = None
    status: Optional[Status] = None


class TaskResponseModel(BaseModel):
    """
    Model for task response data.

    Attributes:
        id (UUID): The unique identifier of the task.
        summary (str): A brief summary of the task.
        description (str): A detailed description of the task.
        status (Status): The current status of the task.
        priority (Priority): The priority level of the task.
        created_at (datetime): The creation timestamp of the task.
        user (Optional[UserResponseModel]): The user associated with the task.
    """

    id: UUID
    summary: str
    description: str
    status: Status
    priority: Priority
    created_at: datetime
    user: Optional[UserResponseModel] = None

    class Config:
        """Config"""

        from_attributes = True
