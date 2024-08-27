from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field
from models.user_model import UserResponseModel
from schemas.task_schema import Priority, Status


class TaskModel(BaseModel):
    id: UUID
    summary: str
    description: str
    status: Status = Field(default=Status.OPEN)
    priority: Priority = Field(default=Priority.MEDIUM)


class TaskRequestModel(BaseModel):
    id: Optional[UUID] = None
    summary: Optional[str] = ""
    description: Optional[str] = ""
    status: Optional[List[Status]] = None
    priority: Optional[List[Priority]] = None
    created_from: Optional[datetime] = datetime(1970, 1, 1, 0, 0, 1)
    created_to: Optional[datetime] = None


class CreateTaskRequestModel(BaseModel):
    summary: Optional[str] = ""
    description: Optional[str] = ""
    priority: Optional[Priority] = Priority.MEDIUM
    user_id: UUID

class TaskResponseModel(BaseModel):
    id: UUID
    summary: str
    description: str
    status: Status
    priority: Priority
    created_at: datetime
    user: Optional[UserResponseModel] = None

    class Config:
        from_attributes = True
