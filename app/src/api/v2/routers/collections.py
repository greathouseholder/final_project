from typing import List
from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status

from src.api.v2.exceptions import handle_exception
from src.api.v2.helpers import check_admin_rights, get_user_id
from src.api.v2.schemas import Collection, CollectionCreate, CollectionShort, CollectionUpdate
from src.core.application.rdb.schemas import (
    CreateCollectionRequest,
    UpdateCollectionRequest,
)
from src.core.application.rdb.use_cases.collection import (
    CreateCollectionUC,
    DeleteCollectionUC,
    GetAvailableCollectionsUC,
    GetCollectionUC,
    UpdateCollectionUC,
)
from src.core.application.rdb.use_cases.user import CheckAdminUC, RegisterUserUC

router = APIRouter(prefix="/collections", tags=["collections"])


@router.get("/", response_model=List[CollectionShort])
@inject
async def get_collections(
    telegram_id: int,
    register_user_uc: FromDishka[RegisterUserUC],
    get_avaliable_collections_uc: FromDishka[GetAvailableCollectionsUC],
) -> List[CollectionShort]:
    """
    Получить список коллекций пользователя.
    """
    try:
        user_id = await get_user_id(telegram_id, None, register_user_uc)
        available_collections = await get_avaliable_collections_uc.execute(user_id)

        return [
            CollectionShort(
                collection_id=collection.collection_id,
                name=collection.name,
                description=collection.description
            )
            for collection in available_collections
        ]
    except Exception as exc:
        raise handle_exception(exc) from None


@router.post("/", response_model=CollectionShort,
             status_code=status.HTTP_201_CREATED)
@inject
async def create_collection(
    collection_data: CollectionCreate,
    register_user_uc: FromDishka[RegisterUserUC],
    check_admin_uc: FromDishka[CheckAdminUC],
    create_collection_uc: FromDishka[CreateCollectionUC]
):
    """
    Создать новую коллекцию.
    """
    try:
        user_id = await get_user_id(None, collection_data, register_user_uc)
        await check_admin_rights(user_id, check_admin_uc)

        collection = await create_collection_uc.execute(
            CreateCollectionRequest(
                name=collection_data.name,
                description=collection_data.description,
                is_public=collection_data.is_public
            ),
            user_id
        )

        return CollectionShort(
            collection_id=collection.collection_id,
            name=collection.name,
            description=collection.description
        )
    except Exception as exc:
        raise handle_exception(exc) from None


@router.delete("/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_collection(
    telegram_id: int,
    collection_id: UUID,
    register_user_uc: FromDishka[RegisterUserUC],
    check_admin_uc: FromDishka[CheckAdminUC],
    delete_collection_uc: FromDishka[DeleteCollectionUC]
):
    """
    Удалить коллекцию по ID.
    """
    try:
        user_id = await get_user_id(telegram_id, None, register_user_uc)
        await check_admin_rights(user_id, check_admin_uc)
        await delete_collection_uc.execute(collection_id, user_id)
    except Exception as exc:
        raise handle_exception(exc) from None


@router.get("/one", response_model=Collection)
@inject
async def get_collection(
    telegram_id: int,
    collection_id: UUID,
    register_user_uc: FromDishka[RegisterUserUC],
    get_collection_uc: FromDishka[GetCollectionUC]
):
    """
    Получить информацию о конкретной коллекции.
    """
    try:
        user_id = await get_user_id(telegram_id, None, register_user_uc)
        collection = await get_collection_uc.execute(collection_id, user_id)

        return Collection(
            collection_id=collection.collection_id,
            name=collection.name,
            description=collection.description,
            document_count=collection.document_count,
            is_public=collection.is_public,
            created_at=collection.created_at
        )
    except Exception as exc:
        raise handle_exception(exc) from None


@router.patch("/one", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def update_collection(
    collection_data: CollectionUpdate,
    register_user_uc: FromDishka[RegisterUserUC],
    check_admin_uc: FromDishka[CheckAdminUC],
    update_collection_uc: FromDishka[UpdateCollectionUC]
):
    """
    Обновить информацию о коллекции.
    """
    try:
        user_id = await get_user_id(None, collection_data, register_user_uc)
        await check_admin_rights(user_id, check_admin_uc)

        await update_collection_uc.execute(
            request=UpdateCollectionRequest(
                collection_id=collection_data.collection_id,
                name=collection_data.name,
                description=collection_data.description,
                is_public=collection_data.is_public
            ),
            user_id=user_id
        )
    except Exception as exc:
        raise handle_exception(exc) from None
