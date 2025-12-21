from typing import List
from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, HTTPException, status

from src.api.v2.exceptions import handle_exception
from src.api.v2.schemas import Collection, CollectionCreate, CollectionShort, CollectionUpdate
from src.core.application.rdb.schemas import (
    CollectionResponse,
    CreateCollectionRequest,
    CreateUserRequest,
    UpdateCollectionRequest,
    UserResponse,
)
from src.core.application.rdb.use_cases import (
    CheckAdminUC,
    CreateCollectionUC,
    DeleteCollectionUC,
    GetAvailableCollectionsUC,
    GetCollectionUC,
    GetUserIdUC,
    UpdateCollectionUC,  # требуется CreateUserUC
)

router = APIRouter(prefix="/collections", tags=["collections"])


@router.get("/", response_model=List[CollectionShort])
@inject
async def get_collections(
    telegram_id: int,
    get_user_id_uc: FromDishka[GetUserIdUC],
    get_avaliable_collections_uc: FromDishka[GetAvailableCollectionsUC],
) -> List[CollectionShort]:
    """
    Получить список коллекций пользователя.
    """
    try:
        user_id: UUID = await get_user_id_uc.execute(telegram_id)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        ) from None

    available_collections: List[CollectionResponse] = \
        await get_avaliable_collections_uc.execute(user_id)

    return [
        CollectionShort(
            collection_id=collection.collection_id,
            name=collection.name,
            description=collection.description
        )
        for collection in available_collections
    ]


@router.post("/", response_model=CollectionShort,
             status_code=status.HTTP_201_CREATED)
@inject
async def create_collection(
    collection_data: CollectionCreate,
    get_user_id_uc: FromDishka[GetUserIdUC],
    check_admin_uc: FromDishka[CheckAdminUC],
    create_collection_uc: FromDishka[CreateCollectionUC]
):
    """
    Создать новую коллекцию.
    """
    try:
        user_id: UUID = await get_user_id_uc.execute(collection_data.telegram_id)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        ) from None

    if not await check_admin_uc.execute(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет прав на создание коллекции"
        )

    try:
        collection: CollectionResponse = await create_collection_uc.execute(
            CreateCollectionRequest(
                name=collection_data.name,
                description=collection_data.description,
                is_public=collection_data.is_public
            ),
            user_id)
    except Exception as exc:
        return handle_exception(exc)

    return CollectionShort(
        collection_id=collection.collection_id,
        name=collection.name,
        description=collection.description
    )


@router.delete("/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_collection(
    telegram_id: int,
    collection_id: int,
    get_user_id_uc: FromDishka[GetUserIdUC],
    check_admin_uc: FromDishka[CheckAdminUC],
    delete_collection_uc: FromDishka[DeleteCollectionUC]
):
    """
    Удалить коллекцию по ID.
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
            detail="У вас нет прав на удаление коллекции"
        )

    try:
        await delete_collection_uc.execute(collection_id, user_id)
    except Exception as exc:
        return handle_exception(exc)


@router.get("/{collection_id}", response_model=Collection)
@inject
async def get_collection(
    telegram_id: int,
    collection_id: int,
    get_user_id_uc: FromDishka[GetUserIdUC],
    get_collection_uc: FromDishka[GetCollectionUC]
):
    """
    Получить информацию о конкретной коллекции.
    """
    try:
        user_id: UUID = await get_user_id_uc.execute(telegram_id)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        ) from None

    try:
        collection: CollectionResponse = await get_collection_uc.execute(collection_id, user_id)
    except Exception as exc:
        return handle_exception(exc)

    return Collection(
        collection_id=collection.collection_id,
        name=collection.name,
        description=collection.description,
        document_count=collection.document_count,
        is_public=collection.is_public,
        created_at=None
    )


@router.patch("/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def update_collection(
    collection_id: int,
    collection_data: CollectionUpdate,
    get_user_id_uc: FromDishka[GetUserIdUC],
    check_admin_uc: FromDishka[CheckAdminUC],
    update_collection_uc: FromDishka[UpdateCollectionUC]
):
    """
    Обновить информацию о коллекции.
    """
    try:
        user_id: UUID = await get_user_id_uc.execute(collection_data.telegram_id)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        ) from None

    if not await check_admin_uc.execute(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет прав на редактирование коллекции"
        )

    try:
        await update_collection_uc.execute(
            request=UpdateCollectionRequest(
                collection_id=collection_id,
                name=collection_data.name,
                description=collection_data.description,
                is_public=None
            ),
            user_id=user_id)
    except Exception as exc:
        return handle_exception(exc)
