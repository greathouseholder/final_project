from typing import List, Any
import openai
from .interface import LLMInterface
from src.shared.config import config
from src.core.application.generation.schemas.answer import Message, LLMResponse

class LLMClient(LLMInterface):
    def __init__(self):
        self.api_key = config.LLM_API_KEY

    def generate(self, model: str, history: List[Message]) -> LLMResponse:
        adapted_history = self._create_adapted_history(history)
        return self._create_response(self.api_key, model, adapted_history)

    @staticmethod
    def _create_adapted_history(history: List[Message]) -> Any:
        # например как это для openai будет
        adapted_history = []
        for msg in history:
            adapted_history.append({
                "role": msg.role.value,
                "content": msg.content
            })
        return adapted_history

    @staticmethod
    def _create_response(api_key: str, model: str, history: Any) -> LLMResponse:
        #например как это будет для openai
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model=model,
            messages=history,
        )
        return LLMResponse(model=model, response=response.choices[0].message.content)