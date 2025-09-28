from .ultils import str_pooling_tfidf
from states import AppState
from llms.gemini import gemini

_GREETING_ROUTER_DICT = {
    "rag": "Reading documents using RAG",
    "show_event": "Explaining and showing upcoming events",
    # "study_chat": "Chatting with bots to assist with studying",
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

def router_by_dict(state:AppState, dict:dict) -> str:
    system_msg = f"""
        You are a function chooser.
        You must choose exactly ONE of the following feature keys based on the user input:

        {dict}

        Rules:
        - Return only the feature key (e.g., choose_document) as your answer.
        - Do not write explanations or anything else.
        """

    user_msg = f"User says: {state.user_input}"

    resp = gemini.invoke([
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_msg},
    ]).content
    resp = str_pooling_tfidf(resp, dict)
    return resp

def router_event(state:AppState, dict:dict, res_event:str):
    msgs = state.cache
    if not msgs:
        return router_by_dict(state, dict)
    else:
        return res_event

def router_truefalse(state:AppState, res_true, res_false) -> str:
    raise NotImplementedError()
    msgs = state.cache
    if not msgs:
        return res_true
    else:
        return res_false
