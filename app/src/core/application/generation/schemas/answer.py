from enum import Enum

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
    collection_name: str
