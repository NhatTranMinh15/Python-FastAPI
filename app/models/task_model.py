from datetime import datetime
from typing import List, Optional, Set
from uuid import UUID
from models.user_model import UserResponseModel
from pydantic import BaseModel, Field
from schemas.task_schema import Priority, Status


class TaskModel(BaseModel):
    id: UUID
    summary: str
    description: str
    status: Status = Field(default=Status.OPEN)
    priority: Priority = Field(default=Priority.MEDIUM)


class TaskRequestModel(BaseModel):
    id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    summary: Optional[str] = ""
    description: Optional[str] = ""
    created_from: Optional[datetime] = datetime(1970, 1, 1, 0, 0, 1)
    created_to: Optional[datetime] = None


class CreateTaskRequestModel(BaseModel):
    summary: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[Priority] = None
    user_id: UUID = None
    status: Optional[Status] = None
    

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
