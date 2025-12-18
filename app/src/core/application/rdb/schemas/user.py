from pydantic import BaseModel
from uuid import UUID


class UserResponse(BaseModel):
    user_id: UUID
    telegram_id: int
    role: str


class CreateUserRequest(BaseModel):
    telegram_id: int
    role: str = "user"