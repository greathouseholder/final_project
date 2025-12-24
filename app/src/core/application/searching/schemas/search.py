from pydantic import BaseModel
from uuid import UUID


class SearchRequest(BaseModel):
    query: str
    model: str
    collection_id: UUID
    top_k: int = 5
