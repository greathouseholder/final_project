from typing import List

import openai
from retry import retry

from src.core.application.generation.schemas.answer import Message, LLMResponse
from src.infra.adapters.llm.interface import LLMInterface
from src.shared.config import config


class OpenAIClient(LLMInterface):
    def __init__(self):
        self.api_key = config.LLM_API_KEY
        self.client = openai.AsyncOpenAI(
            base_url="https://api.llm7.io/v1",
            api_key=self.api_key
        )

    def generate(self, model: str, history: List[Message]) -> LLMResponse:
        pass

    @retry(tries=3, delay=30)
    async def get_answer(self, model: str, query: str) -> str:
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": query}],
                temperature=0.5,
                max_tokens=100
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error: {e}")
            return query
