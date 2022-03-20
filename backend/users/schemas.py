from pydantic import BaseModel, Field

from uuid import UUID

from datetime import datetime


class UserDetailResponse(BaseModel):
    uid: UUID = Field(alias="user_uid")
    email: str
    created_at: datetime

    class Config:
        allow_population_by_field_name = True
        orm_mode = True
