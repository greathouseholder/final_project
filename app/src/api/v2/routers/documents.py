from typing import List
from uuid import UUID

import chardet
import pdfplumber
from dishka.integrations.fastapi import FromDishka, inject
from docx import Document as Document_docx
from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from src.api.v2.exceptions import handle_exception
from src.api.v2.schemas import Document, DocumentShort, DocumentUpdate, UploadDocumentRequest
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

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


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

    try:
        documents: List[DocumentResponse] = \
            await get_avaliable_documents_uc.execute(collection_id, user_id)
    except Exception as exc:
        return handle_exception(exc)

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
    metadata: UploadDocumentRequest,
    file: UploadFile = File(...)
):
    """
    Загрузить новый документ.
    """
    try:
        user_id: UUID = await get_user_id_uc.execute(metadata.telegram_id)
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
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Данный формат файлов не поддерживается"
        )

    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Размер файла превышает допустимый лимит в {MAX_FILE_SIZE / (1024*1024):.1f} МБ"
        )

    try:
        if f'.{file_extension}' == '.txt':
            content = await file.read()
            detected = chardet.detect(content)
            encoding = detected['encoding'] or 'utf-8'
            try:
                text = content.decode(encoding)
            except UnicodeDecodeError:
                text = content.decode('utf-8', errors='replace')
        elif f'.{file_extension}' == '.pdf':
            content = await file.read()
            with pdfplumber.open(content) as pdf:
                pages = [page.extract_text() for page in pdf.pages]
                text = '\n'.join(pages)
        elif f'.{file_extension}' in ['.doc', '.docx']:
            content = await file.read()
            if f'.{file_extension}' == '.docx':
                doc = Document_docx(content)
                text = '\n'.join([para.text for para in doc.paragraphs])
            else:
                raise HTTPException(
                    status_code=status.HTTP_501_NOT_IMPLEMENTED,
                    detail="На данный момент файлы .doc не поддерживаются."
                )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла внутренняя ошибка сервера"
        ) from None

    document = CoreDocument(
        text=text,
        metadata={
            "title": metadata.title,
            "description": metadata.description,
            "url": metadata.url,
            "filename": file.filename,
            "filesize": round(file_size / (1024 * 1024), 1)
        }
    )
    loading_request = LoadDataRequest(
        data=document
    )

    try:  # TO-DO
        loaded_document = await loading_uc.execute(loading_request)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла внутренняя ошибка сервера"
        ) from None

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
    except Exception as exc:
        return handle_exception(exc)


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
    except Exception as exc:
        return handle_exception(exc)

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
    except Exception as exc:
        return handle_exception(exc)
