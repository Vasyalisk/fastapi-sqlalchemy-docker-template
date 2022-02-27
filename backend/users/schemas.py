from pydantic import BaseModel

from datetime import datetime


class UserDetailResponse(BaseModel):
    id: int
    username: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserUpdateRequest(BaseModel):
    username: str
