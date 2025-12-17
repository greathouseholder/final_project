from typing import List

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Body, HTTPException, Query, status

from src.api.v2.schemas import Collection, CollectionCreate, CollectionShort, CollectionUpdate
from src.core.application.databases import (
    CheckAdminUC,
    CreateCollectionUC,
    DeleteCollectionUC,
    GetAvaliableCollectionsUC,
    GetCollectionUC,
    UpdateCollectionUC,
)

router = APIRouter(prefix="/collections", tags=["collections"])

mock_collections = []
mock_users = {}


@router.get("/", response_model=List[CollectionShort])
@inject
async def get_collections(
    get_avaliable_collections: FromDishka[GetAvaliableCollectionsUC],
    telegram_id: int = Query(..., description="Telegram ID пользователя")
):
    """
    Получить список коллекций пользователя.
    """
    available_collections: List[Collection] = await get_avaliable_collections.execute(
        telegram_id=telegram_id
    )

    return [
        CollectionShort(
            collection_id=col.collection_id,
            name=col.name,
            description=col.description
        )
        for col in available_collections
    ]
    # return available_collections


@router.post("/", response_model=CollectionShort,
             status_code=status.HTTP_201_CREATED)
@inject
async def create_collection(
    collection_data: CollectionCreate,
    check_admin: FromDishka[CheckAdminUC],
    create_collection: FromDishka[CreateCollectionUC]
):
    """
    Создать новую коллекцию.
    """
    if not await check_admin(telegram_id=collection_data.telegram_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет прав на создание коллекции"
        )

    try:
        collection: Collection = await create_collection.execute(collection_data)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Коллекция с таким именем уже существует"
        )

    return CollectionShort(
        collection_id=collection.collection_id,
        name=collection_data.name,
        description=collection_data.description
    )


@router.delete("/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_collection(
    collection_id: int,
    check_admin: FromDishka[CheckAdminUC],
    delete_collection: FromDishka[DeleteCollectionUC],
    telegram_id: int = Query(..., description="Telegram ID пользователя")
):
    """
    Удалить коллекцию по ID.
    """
    if not await check_admin(telegram_id=telegram_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет прав на удаление коллекции"
        )

    await delete_collection.execute(collection_id)


@router.get("/{collection_id}", response_model=Collection)
@inject
async def get_collection(
    collection_id: int,
    get_collection: FromDishka[GetCollectionUC],
    telegram_id: int = Query(..., description="Telegram ID пользователя")
):
    """
    Получить информацию о конкретной коллекции.
    """
    collection = await get_collection.execute(collection_id)
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

    return collection


@router.patch("/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def update_collection(
    collection_id: int,
    collection_data: CollectionUpdate,
    check_admin: FromDishka[CheckAdminUC],
    update_collection: FromDishka[UpdateCollectionUC]
):
    """
    Обновить информацию о коллекции.
    """
    if not await check_admin(telegram_id=collection_data.telegram_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет прав на редактирование этой коллекции"
        )

    try:
        await update_collection.execute(collection_id, collection_data)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Коллекция не найдена"
        )
