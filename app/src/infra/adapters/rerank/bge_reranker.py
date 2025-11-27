from sentence_transformers import CrossEncoder
import torch
from typing import List
from result import Result, Ok, Err

from src.core.domain.document import VectorisedDocument, ExtendedVectorisedDocument
from .interface import RerankerInterface


class BGEReranker(RerankerInterface):
    def __init__(self, model_name: str = "BAAI/bge-reranker-v2-m3"):
        self.model_name = model_name
        self._model = None

    def _get_model(self):
        if self._model is None:
            try:
                self._model = CrossEncoder(self.model_name)
            except Exception as e:
                raise ValueError(f"Failed to load reranker model {self.model_name}: {str(e)}")
        return self._model

    def rerank(
        self,
        query: str,
        documents: List[ExtendedVectorisedDocument],
        top_k: int = 5
    ) -> Result[List[ExtendedVectorisedDocument], str]:

        top_k = min(top_k, len(documents))

        try:
            model = self._get_model()
            pairs = []
            for doc in documents:
                doc_text = str(doc.text) if doc.text is not None else ""
                pairs.append([str(query), doc_text])

            for i, pair in enumerate(pairs):
                if not all(isinstance(text, str) for text in pair):
                    return Err(f"Invalid text types in pair {i}: {[type(text) for text in pair]}")

            scores = model.predict(pairs)
            scores = torch.sigmoid(torch.tensor(scores)).cpu().numpy()

            scored_docs = list(zip(scores, documents))
            scored_docs.sort(key=lambda x: x[0], reverse=True)
            reranked_docs = [doc for _, doc in scored_docs[:top_k]]

            for i, doc in enumerate(reranked_docs):
                doc.metadata["rerank_score"] = float(scored_docs[i][0])

            return Ok(reranked_docs)

        except Exception as e:
            return Err(f"Reranking failed: {str(e)}")