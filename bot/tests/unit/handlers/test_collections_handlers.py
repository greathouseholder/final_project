import pytest
import bot_app.handlers.collections_handlers as ch
import bot_app.states as st

@pytest.mark.asyncio
async def test_add_collection_success(callback_query, fsm_context):

    await ch.add_collection(callback_query, fsm_context)

    current_state = await fsm_context.get_state()

    assert current_state == st.AddNewcollection.coll_name.state
    assert callback_query.answer.call_count == 1
    assert callback_query.message.answer.call_count == 1

    call_args, call_kwargs = callback_query.message.answer.call_args

    assert call_args[0] == "Введите название коллекции: "
    assert "reply_markup" in call_kwargs
    assert call_kwargs["reply_markup"] == ch.kb.cancel_button_keyboard