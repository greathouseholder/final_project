from sentence_transformers import SentenceTransformer
from result import Result, Ok, Err


from src.core.domain.document import CoreDocument, VectorisedDocument
from .interface import EmbedderInterface


class BGEEmbedder(EmbedderInterface):
    def __init__(self, model_name: str = "BAAI/bge-m3"):
        self.model_name = model_name
        self._model = None

    def _get_model(self):
        if self._model is None:
            try:
                self._model = SentenceTransformer(self.model_name)
            except Exception as e:
                raise ValueError(f"Failed to load model {self.model_name}: {str(e)}")
        return self._model

    def embed(self, text: str) -> Result[list[float], str]:
        if not text.strip():
            return Err("Empty text provided")

        try:
            model = self._get_model()
            embedding = model.encode([text], normalize_embeddings=True, batch_size=1)
            vector = embedding[0].tolist()
            return Ok(vector)
        except Exception as e:
            return Err(f"Embedding failed: {str(e)}")

    def embed_document(self, document: CoreDocument) -> Result[VectorisedDocument, str]:
        embed_result = self.embed(document.text)
        if isinstance(embed_result, Err):
            return Err(embed_result.unwrap_err())

        vector = embed_result.unwrap()
        try:
            vectorised_doc = VectorisedDocument(
                text=document.text,
                metadata=document.metadata,
                embedding=vector
            )
            return Ok(vectorised_doc)
        except Exception as e:
            return Err(f"Failed to create VectorisedDocument: {str(e)}")