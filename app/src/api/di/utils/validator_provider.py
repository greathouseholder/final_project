from dishka import Provider, Scope, provide

from src.infra.adapters.validation.interface import ValidatorInterface
from src.infra.adapters.validation.validate_preprocessor import ValidatorPreprocessing


class ValidationProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_validator_interface(self) -> ValidatorInterface:
        return ValidatorPreprocessing()
