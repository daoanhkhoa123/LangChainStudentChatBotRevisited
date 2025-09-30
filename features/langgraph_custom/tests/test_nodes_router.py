import pytest
from unittest import  mock

from nodes.router import greeting_router

_GREETING_ROUTER_DICT = {
    "rag": "Reading documents using RAG",
    "show_event": "Explaining and showing upcoming events",
    "study_chat": "Chatting with bots to assist with studying",
    "normal_chat": "General chat"
}

@mock.patch("nodes.router.str_pooling_tfidf")
@mock.patch("nodes.router.gemini")
def test_greeting_router(mock_gemini, mock_strpool, appstate_sample):
    # appstate mock
    appstate_sample.user_input = "i want to read books"
    
    # gemini api mock
    mock_resp = mock.MagicMock()
    mock_resp.content = "show_event"
    mock_gemini.invoke.return_value = mock_resp

    # str pool mock
    mock_strpool.return_value = "show_event"

    result = greeting_router(appstate_sample)
    
    mock_gemini.invoke.assert_called_once()
    mock_strpool.assert_called_once_with("show_event", _GREETING_ROUTER_DICT)

    assert result == "show_event"

def test_greeting_router_real(appstate_sample):
    appstate_sample.user_input = "i want to read books"
    result = greeting_router(appstate_sample)
    assert result == "rag"
