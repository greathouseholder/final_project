from dishka import Provider, Scope, provide

from src.infra.adapters.embeddings.frida import FridaEmbedder


class FridaEmbedderProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_frida(self) -> FridaEmbedder:
        return FridaEmbedder()
