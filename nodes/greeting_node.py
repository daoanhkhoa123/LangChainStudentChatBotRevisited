from fn_tools.greeting_with_events import greeting_with_events, choose_events, tell_events
from states import AppState

def greeting_node(state:AppState) -> AppState:
    greet = greeting_with_events(state.studentstate, state.schoolstate)
    return {"messages": [greet]}

def choose_upcomingevents_node(state:AppState) -> AppState:
    events = state.schoolstate.upcoming_events
    events =  choose_events(events, state.user_input)
    return {"cache": events}

def user_input_node(state:AppState):
    user_input = input("Your prompt here:\n")
    return {"user_input": user_input}

def tell_event_node(state:AppState):
    events = state.cache
    response = tell_events(events, state.user_input)
    return {"messages": [response]} 
