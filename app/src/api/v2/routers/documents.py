from typing import List
from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from src.api.v2.schemas import Document, DocumentShort, DocumentUpdate
from src.core.application.embeddings.schemas.load_data import LoadDataRequest
from src.core.application.embeddings.use_cases.load_data import LoadingUC
from src.core.application.rdb.schemas import DocumentResponse, UpdateDocumentRequest
from src.core.application.rdb.use_cases import (
    CheckAdminUC,
    DeleteDocumentUC,
    GetAvailableDocumentsUC,
    GetDocumentUC,
    GetUserIdUC,
    UpdateDocumentUC,
)
from src.core.domain.document import CoreDocument

router = APIRouter(
    prefix="/collections/{collection_id}/documents", tags=["documents"])


@router.get("/", response_model=List[DocumentShort])
@inject
async def get_documents(
    telegram_id: int,
    collection_id: int,
    get_user_id_uc: FromDishka[GetUserIdUC],
    get_avaliable_documents_uc: FromDishka[GetAvailableDocumentsUC]
):
    """
    Получить список доступных документов.
    """
    try:
        user_id: UUID = await get_user_id_uc.execute(telegram_id)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        ) from None

    documents: List[DocumentResponse] = \
        await get_avaliable_documents_uc.execute(collection_id, user_id)

    return [
        DocumentShort(
            document_id=doc.document_id,
            collection_id=doc.collection_id,
            name=doc.title
        )
        for doc in documents
    ]


@router.post("/", response_model=DocumentShort,
             status_code=status.HTTP_201_CREATED)
@inject
async def upload_document(
    collection_id: int,
    get_user_id_uc: FromDishka[GetUserIdUC],
    check_admin_uc: FromDishka[CheckAdminUC],
    loading_uc: FromDishka[LoadingUC],
    telegram_id: int = Form(...),
    title: str = Form(...),
    description: str = Form(None),
    url: str = Form(None),
    file: UploadFile = File(...)
):
    """
    Загрузить новый документ.
    """
    try:
        user_id: UUID = await get_user_id_uc.execute(telegram_id)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        ) from None

    if not await check_admin_uc.execute(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет прав на загрузку документов"
        )

    allowed_extensions = ['.txt', '.pdf', '.doc', '.docx']
    file_extension = file.filename.split(
        '.')[-1].lower() if '.' in file.filename else ''
    if f'.{file_extension}' not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Данный формат файлов не поддерживается"
        )

    if f'.{file_extension}' == '.txt':
        try:
            async with file:
                content = await file.read()
                text = content.decode('utf-8')
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error)
            ) from error
    else:  # TO-DO
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Данный формат файлов не поддерживается"
        )

    document = CoreDocument(
        text=text,
        metadata={
            "title": title,
            "description": description,
            "url": url
        }
    )
    loading_request = LoadDataRequest(
        data=document
    )

    try:  # TO-DO
        loaded_document = await loading_uc.execute(loading_request)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        ) from error

    return DocumentShort(
        document_id=loaded_document.document.document_id,
        collection_id=loaded_document.collection_id,
        name=loaded_document.document.title
    )


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_document(
    collection_id: int,
    telegram_id: int,
    document_id: int,
    get_user_id_uc: FromDishka[GetUserIdUC],
    check_admin_uc: FromDishka[CheckAdminUC],
    delete_document_uc: FromDishka[DeleteDocumentUC]
):
    """
    Удалить существующий документ.
    """
    try:
        user_id: UUID = await get_user_id_uc.execute(telegram_id)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        ) from None

    if not await check_admin_uc.execute(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет прав на удаление документа"
        )

    try:
        await delete_document_uc.execute(document_id, user_id)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        ) from error


@router.get("/{document_id}", response_model=Document)
@inject
async def get_document(
    telegram_id: int,
    collection_id: int,
    document_id: int,
    get_user_id_uc: FromDishka[GetUserIdUC],
    get_document_uc: FromDishka[GetDocumentUC]
):
    """
    Получить конкретный документ.
    """
    try:
        user_id: UUID = await get_user_id_uc.execute(telegram_id)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        ) from None

    try:
        document: DocumentResponse = await get_document_uc.execute(document_id, user_id)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        ) from error

    return Document(
        document_id=document.document_id,
        collection_id=document.collection_id,
        title=document.title,
        file_name=document.file_name,
        file_size=document.file_size,
        created_at=None,
        metadata=document.metadata
    )


@router.patch("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def update_document(
    collection_id: int,
    document_id: int,
    document_data: DocumentUpdate,
    get_user_id_uc: FromDishka[GetUserIdUC],
    check_admin_uc: FromDishka[CheckAdminUC],
    update_document_uc: FromDishka[UpdateDocumentUC]
):
    """
    Редактировать конкретный документ.
    """
    try:
        user_id: UUID = await get_user_id_uc.execute(document_data.telegram_id)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        ) from None

    if not await check_admin_uc.execute(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет прав на редактирование документа"
        )

    update_document_request = UpdateDocumentRequest(
        document_id=document_id,
        title=document_data.title
    )

    try:
        await update_document_uc.execute(update_document_request, user_id)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        ) from error
