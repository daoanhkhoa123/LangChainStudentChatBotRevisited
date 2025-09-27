from states import AppState

def event_router(state:AppState) -> str:
    msgs = state.cache
    if not msgs:
        return "user_ask"    
    else:
        return "tell_event"
