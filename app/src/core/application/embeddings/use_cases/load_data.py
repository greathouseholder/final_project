from typing import List
from uuid import UUID

from result import Err, Ok, Result

from src.core.application.embeddings.schemas.load_data import LoadDataRequest
from src.core.domain.document import CoreDocument, VectorisedDocument
from src.core.domain.rdb_entities import Document as RDBDocument
from src.infra.adapters.chunks import ChunkAdapterInterface
from src.infra.adapters.embeddings import EmbedderInterface
from src.infra.adapters.rdb.interface import RDBRepository
from src.infra.adapters.vdb import VectorDBInterface


class LoadingUC:
    """
    Use Case: Загрузка документа в систему RAG
    1. Создаёт запись в RDB (таблица documents)
    2. Чанкует текст
    3. Эмбеддит чанки
    4. Загружает чанки в векторную БД (Qdrant) с привязкой к collection_id и document_id
    """
    __slots__ = ("_vdb_gateway", "_embedder", "_chunk_adapter", "_rdb_repo")

    def __init__(
        self,
        vdb_gateway: VectorDBInterface,
        embedder: EmbedderInterface,
        chunk_adapter: ChunkAdapterInterface,
        rdb_repo: RDBRepository,
    ):
        self._vdb_gateway = vdb_gateway
        self._embedder = embedder
        self._chunk_adapter = chunk_adapter
        self._rdb_repo = rdb_repo

    async def execute(
        self,
        request: LoadDataRequest,
        collection_id: UUID,
        title: str = "Без названия",
        file_name: str = "unknown",
        file_size: int = 0,
    ) -> Result[str, str]:
        """
        :param request: LoadDataRequest — содержит CoreDocument (text + metadata), chunk_size, chunk_overlap
        :param collection_id: UUID коллекции из RDB
        :param title: Название документа (для отображения пользователю)
        :param file_name: Оригинальное имя файла
        :param file_size: Размер файла в байтах
        :return: Ok(document_id) или Err(сообщение об ошибке)
        """
        core_doc: CoreDocument = request.data

        try:
            rdb_document: RDBDocument = await self._rdb_repo.create_document(
                collection_id=collection_id,
                title=title or core_doc.metadata.get("title", "Без названия"),
                description=core_doc.metadata.get("description"),
                file_name=file_name,
                file_size=file_size,
                payload=core_doc.metadata,
            )

            document_id: UUID = rdb_document.document_id

            text_chunks: List[str] = self._chunk_adapter.split(
                text=core_doc.text,
                chunk_size=request.chunk_size,
                chunk_overlap=request.chunk_overlap,
            )

            if not text_chunks:
                return Err("Документ пустой после чанкинга")

            vectorised_chunks: List[VectorisedDocument] = []
            for chunk_text in text_chunks:
                chunk_doc = CoreDocument(text=chunk_text, metadata=core_doc.metadata.copy())
                embed_result = self._embedder.embed_document(chunk_doc)
                if embed_result.is_err():
                    return Err(f"Ошибка эмбеддинга: {embed_result.err()}")
                vectorised_chunks.append(embed_result.value)

            batch_size = 100
            for i in range(0, len(vectorised_chunks), batch_size):
                batch = vectorised_chunks[i:i + batch_size]
                add_result = await self._vdb_gateway.bulk_add(
                    documents=batch,
                    collection_id=collection_id,
                    document_id=document_id,
                )
                if add_result.is_err():
                    return Err(f"Ошибка загрузки в VDB (батч {i//batch_size}): {add_result.err()}")

            await self._rdb_repo.increment_document_count(collection_id)

            return Ok(str(document_id))

        except Exception as e:
            return Err(f"Неожиданная ошибка при загрузке документа: {str(e)}")