from src.core.domain.document import CoreDocument
from src.infra.adapters.validation.interface import ValidatorInterface


class ValidatorPreprocessing(ValidatorInterface):
    async def validate(self, response: str, document: CoreDocument):
        return CoreDocument(
            metadata=document.metadata,
            text=response,
        )
