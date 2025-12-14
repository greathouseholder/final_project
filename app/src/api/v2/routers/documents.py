from typing import List

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, File, Form, HTTPException, Query, UploadFile, status

from src.api.v2.schemas import Collection, Document, DocumentShort, DocumentUpdate
from src.core.application.databases import (
    CheckAdminUC,
    DeleteDocumentUC,
    GetAvaliableDocumentsUC,
    GetCollectionUC,
    GetDocumentUC,
    LoadingUC,
    UpdateDocumentUC,
)

router = APIRouter(prefix="/collections/{collection_id}/documents", tags=["documents"])

@router.get("/", response_model=List[DocumentShort])
@inject
async def get_documents(
    collection_id: int,
    get_avaliable_documents: FromDishka[GetAvaliableDocumentsUC],
    get_collection_uc: FromDishka[GetCollectionUC],
    telegram_id: int = Query(..., description="Telegram ID пользователя")
):
    """
    Получить список доступных документов.
    """
    collection: Collection = await get_collection_uc.execute(collection_id)
    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Коллекция не найдена"
        )
    if not collection.is_public and collection.owner_id != telegram_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет прав на просмотр этой коллекции"
        )

    documents: List[Document] = await get_avaliable_documents.execute(
            telegram_id=telegram_id,
            collection_id=collection_id
        )

    return [
        DocumentShort(
            document_id=doc.document_id,
            collection_id=doc.collection_id,
            name=doc.title
        )
        for doc in documents
    ]

@router.post("/", response_model=DocumentShort, status_code=status.HTTP_201_CREATED)
@inject
async def upload_document(
    collection_id: int,
    check_admin: FromDishka[CheckAdminUC],
    loading: FromDishka[LoadingUC],
    telegram_id: int = Form(...),
    title: str = Form(...),
    url: str = Form(None),
    file: UploadFile = File(...)
):
    """
    Загрузить новый документ.
    """
    if not await check_admin(telegram_id=telegram_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет прав на загрузку документов"
        )

    allowed_extensions = ['.txt', '.pdf', '.doc', '.docx']
    file_extension = file.filename.split('.')[-1].lower() if '.' in file.filename else ''
    if f'.{file_extension}' not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Данный формат файлов не поддерживается"
        )

    try:
        document: Document = await loading.execute(
            telegram_id=telegram_id,
            collection_id=collection_id,
            title=title,
            url=url,
            file=file
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Документ с таким названием уже существует"
        )

    return DocumentShort(
        document_id=document.document_id,
        collection_id=document.collection_id,
        name=document.title
    )

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_document(
    collection_id: int,
    document_id: int,
    check_admin: FromDishka[CheckAdminUC],
    delete_document_uc: FromDishka[DeleteDocumentUC],
    telegram_id: int = Query(..., description="Telegram ID пользователя")
):
    """
    Удалить существующий документ.
    """
    if not await check_admin(telegram_id=telegram_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет прав на удаление документов"
        )

    await delete_document_uc.execute(document_id)

@router.get("/{document_id}", response_model=Document)
@inject
async def get_document(
    collection_id: int,
    document_id: int,
    get_document_uc: FromDishka[GetDocumentUC],
    get_collection_uc: FromDishka[GetCollectionUC],
    telegram_id: int = Query(..., description="Telegram ID пользователя")
):
    """
    Получить конкретный документ.
    """
    collection: Collection = await get_collection_uc.execute(collection_id)
    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Коллекция не найдена"
        )
    if not collection.is_public and collection.owner_id != telegram_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет прав на просмотр этого документа"
        )

    document = await get_document_uc.execute(document_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ не найден"
        )

    return document

@router.patch("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def update_document(
    collection_id: int,
    document_id: int,
    document_data: DocumentUpdate,
    check_admin: FromDishka[CheckAdminUC],
    update_document_uc: FromDishka[UpdateDocumentUC]
):
    """
    Редактировать конкретный документ.
    """
    if not await check_admin(telegram_id=document_data.telegram_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет прав на редактирование этого документа"
        )

    try:
        await update_document_uc.execute(document_id, document_data)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ не найден"
        )
