from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str
    model: str
    collection_name: str
