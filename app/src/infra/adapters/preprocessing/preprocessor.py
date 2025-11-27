from typing import List, Any

from src.core.domain.document import CoreDocument
from .interface import Preprocessor
from src.infra.adapters.llm.webGenerator import LLMClient
from src.core.application.generation.schemas.answer import Message, MessageRole, LLMResponse
from jinja2 import Template
from src.infra.adapters.chunks.langchainSplitter import LangChainSplitter

class Preprocess(Preprocessor):
    def __init__(self, llm_model):
        self.llm_model: str = llm_model
    def preprocess(self, document: CoreDocument) -> List[CoreDocument]:
        pass # переделывай



