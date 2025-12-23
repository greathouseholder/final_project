from dishka import Provider, Scope, provide

from src.infra.adapters.llm.interface import LLMInterface
from src.infra.adapters.preprocessing.interface import Preprocessor
from src.infra.adapters.preprocessing.llm_preprocessor import LLMPreprocessor
from src.infra.adapters.prompts.interface import PrompterInterface
from src.infra.adapters.validation.interface import ValidatorInterface


class LLMPreprocessorProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_llm_preprocessor(
        self,
        client: LLMInterface,
        prompter: PrompterInterface,
        validator: ValidatorInterface
    ) -> Preprocessor:
        return LLMPreprocessor(
            client=client,
            prompter=prompter,
            validator=validator
        )
