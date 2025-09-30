import pytest
from nodes.ultils import str_pooling_tfidf

_doc_values = {
    "rag": "Reading documents, books, files using RAG",
    "show_event": "Explaining and showing upcoming events",
    "study_chat": "Chatting with bots to assist with studying",
    "normal_chat": "General chat"
}
@pytest.mark.parametrize("key, values, expected",[
    ("i want to read some books", _doc_values, "rag"),
    ("what is the upcoming events?", _doc_values, "show_event"),
    ("i want to study", _doc_values, "study_chat")
    ])
def test_str_pooling_tfidf_correctness(key, values, expected):
    res = str_pooling_tfidf(key, values)
    assert res == expected

def test_empty_dict():
    with pytest.raises(ValueError):
        str_pooling_tfidf("apple", {})

def test_empty_key():
    dct = {"apple": "fruit", "banana": "fruit"}
    result = str_pooling_tfidf("", dct)
    assert result in dct.keys()

def test_non_ascii():
    dct = {"café": "drink", "theater": "place"}
    result = str_pooling_tfidf("i want to drink", dct)
    assert result == "café"