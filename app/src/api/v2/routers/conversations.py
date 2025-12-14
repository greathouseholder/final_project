from typing import List

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, HTTPException, Query, status

from src.api.v2.schemas import ConversationCreate, ConversationShort, ConversationUpdate
from src.core.application.databases import (
    CreateConversationUC,
    DeleteConversationUC,
    GetAvaliableConversationsUC,
    GetCollectionUC,
    UpdateConversationUC,
)

router = APIRouter(prefix="/conversations", tags=["conversations"])

@router.get("/", response_model=List[ConversationShort])
@inject
async def get_conversations(
    get_avaliable_conversations: FromDishka[GetAvaliableConversationsUC],
    telegram_id: int = Query(..., description="Telegram ID пользователя")
):
    conversations = await get_avaliable_conversations.execute(telegram_id=telegram_id)
    return [
        ConversationShort(
            conversation_id=conv.conversation_id,
            collection_id=conv.collection_id,
            name=conv.name
        )
        for conv in conversations
    ]

@router.post("/", response_model=ConversationShort, status_code=status.HTTP_201_CREATED)
@inject
async def create_conversation(
    conversation_data: ConversationCreate,
    create_conversation_uc: FromDishka[CreateConversationUC],
    get_collection_uc: FromDishka[GetCollectionUC]
):
    collection = await get_collection_uc.execute(conversation_data.collection_id)
    if not collection:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Желаемой коллекции не существует"
        )

    try:
        conversation = await create_conversation_uc.execute(conversation_data)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Диалог с таким названием для этой коллекции уже существует"
        )

    return ConversationShort(
        conversation_id=conversation.conversation_id,
        collection_id=conversation.collection_id,
        name=conversation.name
    )

@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_conversation(
    conversation_id: int,
    delete_conversation_uc: FromDishka[DeleteConversationUC],
    telegram_id: int = Query(..., description="Telegram ID пользователя")
):
    try:
        await delete_conversation_uc.execute(conversation_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Диалог не найден"
        )

@router.patch("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def update_conversation(
    conversation_id: int,
    conversation_data: ConversationUpdate,
    update_conversation_uc: FromDishka[UpdateConversationUC]
):
    try:
        await update_conversation_uc.execute(conversation_id, conversation_data)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Диалог не найден"
        )