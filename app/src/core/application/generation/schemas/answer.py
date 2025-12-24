from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class MessageRole(Enum):
    user = "user"
    model = "model"


class Message(BaseModel):
    role: MessageRole
    text: str


class LLMResponse(BaseModel):
    model: str
    response_text: str


class LLMRequest(BaseModel):
    query: str
    model: str
    collection_id: UUID
