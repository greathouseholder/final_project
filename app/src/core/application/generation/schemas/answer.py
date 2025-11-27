from pydantic import BaseModel
from enum import Enum

class MessageRole(Enum):
    user = "user"
    model = "model"


class Message(BaseModel):
    role: MessageRole
    text: str


class LLMResponse(BaseModel):
    model: str
    response: str