from typing import Tuple, Optional

from states import AppState
from nodes.greeting_node import greeting_node, ask_node, choose_upcomingevents_node, ask_node, tell_event_node
from nodes.ultils import user_ask
from nodes.router import event_router
from langgraph.graph import StateGraph, START, END

StartEndNodes = Tuple[Optional[str], Optional[str]]

def add_greet(graph_builder:StateGraph) -> StartEndNodes:
    graph_builder.add_node("greet", greeting_node)
    return None, "greet"

def choose_upcomingevent(graph_builder:StateGraph) -> StartEndNodes:
    graph_builder.add_node("ask", ask_node)
    graph_builder.add_node("choose_events", choose_upcomingevents_node)
    graph_builder.add_edge("ask", "choose_events")
    return "ask", "choose_events"

def tell_upcomingevent_or_response(graph_builder:StateGraph) -> StartEndNodes:
    graph_builder.add_node("user_ask", user_ask)
    graph_builder.add_node("tell_event", tell_event_node)    
    return None, None