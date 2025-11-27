from src.core.domain.document import CoreDocument
from src.infra.adapters.llm.interface import LLMInterface
from src.infra.adapters.preprocessing.interface import Preprocessor
from src.infra.adapters.promts.jinjaPrompter import JinjaPrompter
from src.infra.adapters.validation.interface import ValidatorInterface


class LLMPreprocessor(Preprocessor):
    def __init__(self, client: LLMInterface, prompter: JinjaPrompter, validator: ValidatorInterface):
        self._client = client
        self._prompter = prompter
        self._validator = validator

    async def preprocess(self, document: CoreDocument, **kwargs) -> CoreDocument:
        prompt = await self._prompter.get_prompt(case=kwargs['case'], document=document)
        response = await self._client.get_answer(model=kwargs['model'], query=prompt)
        return await self._validator.validate(response=response, document=document)
