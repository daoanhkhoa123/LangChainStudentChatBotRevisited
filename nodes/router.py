from .ultils import str_pooling_tfidf
from states import AppState
from llms.gemini import gemini

_GREETING_ROUTER_DICT = {
    "rag": "Reading documents using RAG",
    "show_event": "Explaining and showing upcoming events",
    "study_chat": "Chatting with bots to assist with studying",
    "normal_chat": "General chat"
}

def greeting_router(state:AppState) -> str:
    system_msg = f""" You are chooser function
    Available function:
    {_GREETING_ROUTER_DICT}
    """
    user_msg = f"""
    Decide for me what to do next based on my message:
    {state.user_input}
    """
    resp = gemini.invoke([
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_msg},
    ]).content
    node = str_pooling_tfidf(resp, _GREETING_ROUTER_DICT)
    return node

def event_router(state:AppState) -> str:
    msgs = state.cache
    if not msgs:
        return "user_ask"    
    else:
        return "tell_event"
