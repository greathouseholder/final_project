import torch
from transformers import BertTokenizer, BertModel
from result import Result, Ok, Err

from src.core.domain.document import CoreDocument, VectorisedDocument
from src.infra.adapters.embeddings.interface import EmbedderInterface


class BertEncoder(EmbedderInterface):
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained('DeepPavlov/rubert-base-cased')
        self.device = torch.device("cpu")
        self.model = BertModel.from_pretrained('DeepPavlov/rubert-base-cased').to(self.device)
        self.model.eval()

    def embed(self, text: str) -> Result[list[float], str]:
        if not text or not text.strip():
            return Err("Text is empty or whitespace")
        try:
            inputs = self.tokenizer(
                text,
                return_tensors='pt',
                padding=True,
                truncation=True,
                max_length=512
            ).to(self.device)
            with torch.no_grad():
                outputs = self.model(**inputs)

            last_hidden_state = outputs.last_hidden_state
            cls_embedding = last_hidden_state[:, 0, :]

            embedding_np = cls_embedding.cpu().detach().numpy()[0]
            return Ok(embedding_np.tolist())
        except Exception as e:
            return Err(f"Embedding failed: {str(e)}")

    def embed_document(self, document: CoreDocument) -> Result[VectorisedDocument, str]:
        embedding = self.embed(document.text)
        return Ok(VectorisedDocument(text=document.text, metadata=document.metadata, embedding=embedding.value))