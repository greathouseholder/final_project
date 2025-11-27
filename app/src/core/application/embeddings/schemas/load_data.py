from pydantic import BaseModel

from src.core.domain.document import CoreDocument


class LoadDataRequest(BaseModel):
    data: CoreDocument
    chunk_size: int = 300
    chunk_overlap: int = 100
    collection_name: str = 'baseline'