from typing import List

from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from retry import retry

from src.core.application.generation.schemas.answer import Message, LLMResponse
from src.infra.adapters.llm.interface import LLMInterface
from src.shared.config import config


class GigaChatClient(LLMInterface):
    def __init__(self):
        self.credentials = config.GIGACHAT_CREDENTIALS
        self.scope = getattr(config, "GIGACHAT_SCOPE", "GIGACHAT_API_PERS")
        self.verify_ssl = False

    def generate(self, model: str, history: List[Message]) -> LLMResponse:
        pass

    @retry(tries=3, delay=30)
    async def get_answer(self, model: str, query: str) -> LLMResponse:
        try:
            async with GigaChat(
                    credentials=self.credentials,
                    verify_ssl_certs=self.verify_ssl,
                    scope=self.scope
            ) as giga:

                response = await giga.achat(Chat(
                    model=model,
                    messages=[Messages(role=MessagesRole.USER, content=query)],
                    temperature=0.5,
                    max_tokens=100,
                )
                )

                response = response.choices[0].message.content.strip()
                return LLMResponse(model=model, response=response)

        except Exception as e:
            print(f"Error: {e}")
            raise e