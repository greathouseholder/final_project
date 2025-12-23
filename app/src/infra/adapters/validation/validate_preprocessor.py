from src.core.application.generation.schemas.answer import LLMResponse
from src.core.domain.document import CoreDocument
from src.infra.adapters.validation.interface import ValidatorInterface


class ValidatorPreprocessing(ValidatorInterface):
    async def validate(
            self, response: LLMResponse, document: CoreDocument) -> CoreDocument:
        new_text = response.response

        if not new_text or not new_text.strip():
            return document

        return CoreDocument(
            metadata=document.metadata,
            text=new_text.strip(),
        )
