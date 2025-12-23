from dishka import Provider, Scope, provide

from src.infra.adapters.llm.gigachatGenerator import GigaChatClient
from src.infra.adapters.llm.interface import LLMInterface


class GigachatProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_gigachat(self) -> LLMInterface:
        return GigaChatClient()
