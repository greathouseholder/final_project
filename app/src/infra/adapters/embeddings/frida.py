from sentence_transformers import SentenceTransformer
from result import Result

from src.core.domain.document import CoreDocument, VectorisedDocument
from src.infra.adapters.embeddings.interface import EmbedderInterface


class FridaEmbedder(EmbedderInterface):
    def __init__(self, model_name: str = "ai-forever/FRIDA"):
        self.model_name = model_name
        self._model = None

    def _get_model(self):
        if self._model is None:
            try:
                self._model = SentenceTransformer(self.model_name)
            except Exception as e:
                raise ValueError(
                    f"Failed to load model {self.model_name}: {str(e)}")
        return self._model

    def embed(self, text: str, is_query: bool = False) -> Result[list[float], str]:
        if not text.strip():
            return Result.Err("Empty text provided")

        prefix = "search_query: " if is_query else "search_document: "
        prefixed_text = prefix + text

        try:
            model = self._get_model()
            embedding = model.encode(
                [prefixed_text],
                normalize_embeddings=True)
            vector = embedding[0].tolist()
            return Result.Ok(vector)
        except Exception as e:
            return Result.Err(f"Embedding failed: {str(e)}")

    def embed_document(self, document: CoreDocument) -> Result[VectorisedDocument, str]:
        embed_result = self.embed(document.text, is_query=False)
        if isinstance(embed_result, Result.Err):
            return Result.Err(embed_result.unwrap_err())

        vector = embed_result.unwrap()
        try:
            vectorised_doc = VectorisedDocument(
                text=document.text,
                metadata=document.metadata,
                embedding=vector
            )
            return Result.Ok(vectorised_doc)
        except Exception as e:
            return Result.Err(f"Failed to create VectorisedDocument: {str(e)}")
