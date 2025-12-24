from dishka import Provider, Scope, provide

from src.infra.adapters.prompts.interface import PrompterInterface
from src.infra.adapters.prompts.jinjaPrompter import JinjaPrompter


class JinjaProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_jinja(self) -> PrompterInterface:
        return JinjaPrompter()
