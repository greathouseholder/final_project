from dishka import Provider, Scope, provide

from src.infra.adapters.llm.interface import LLMInterface
from src.infra.adapters.preprocessing.llm_preprocessor import LLMPreprocessor
from src.infra.adapters.prompts.jinjaPrompter import JinjaPrompter
from src.infra.adapters.validation.interface import ValidatorInterface


class LLMPreprocessorProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_llm_preprocessor(
        self,
        client: LLMInterface,
        prompter: JinjaPrompter,
        validator: ValidatorInterface
    ) -> LLMPreprocessor:
        return LLMPreprocessor(
            client=client,
            prompter=prompter,
            validator=validator
        )
