from dishka import Provider, Scope, provide

from src.infra.adapters.llm.gigachatGenerator import GigaChatClient


class GigachatProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_gigachat(self) -> GigaChatClient:
        return GigaChatClient()
