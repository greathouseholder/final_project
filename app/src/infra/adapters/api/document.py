from src.api.v1.schemas import Document
from src.core.domain.document import ExtendedVectorisedDocument


def get_api_do_entity(doc: ExtendedVectorisedDocument) -> Document:
    return Document(
        title=doc.metadata.get('title', ''),
        revelance=doc.metadata['rerank_score'],
        url=doc.metadata.get('url')
    )
