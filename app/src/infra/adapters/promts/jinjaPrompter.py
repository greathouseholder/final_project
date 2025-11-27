from enum import Enum

from src.infra.adapters.promts.interface import PrompterInterface
import os
import jinja2

class CaseEnum(Enum):
    preprocess = 'preprocess'
    preprocess_query = 'preprocess_query'
    generate_answer = 'generate_answer'


FileMapping = {
    CaseEnum.preprocess: 'preprocess_prompt.txt',
    CaseEnum.generate_answer: 'generate_answer.txt',
    CaseEnum.preprocess_query: 'preprocess_query.txt'
}

class JinjaPrompter(PrompterInterface):
    _templates_path: str = os.path.join(os.path.dirname(__file__), 'templates')

    def __init__(self):
        self._env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self._templates_path),
            trim_blocks=True,
            enable_async=True
        )
        self._template = None

    async def get_prompt(self, case: CaseEnum, **kwargs):
        self._template = self._env.get_template(FileMapping[case])
        return await self._template.render_async(**kwargs)