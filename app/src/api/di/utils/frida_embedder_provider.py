from dishka import Provider, Scope, provide

from src.infra.adapters.embeddings.frida import FridaEmbedder
from src.infra.adapters.embeddings.interface import EmbedderInterface


class FridaEmbedderProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_frida(self) -> EmbedderInterface:
        return FridaEmbedder()
