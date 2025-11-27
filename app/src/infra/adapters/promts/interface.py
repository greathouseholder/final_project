from abc import ABC, abstractmethod


class PrompterInterface(ABC):
    @abstractmethod
    async def get_prompt(self, **kwargs):
        pass