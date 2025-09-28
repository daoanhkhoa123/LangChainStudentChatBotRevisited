from typing import Tuple, Optional

from states import AppState
from nodes.greeting_node import greeting_node, user_input_node, choose_upcomingevents_node, user_input_node, tell_event_node
from nodes.ultils import llm_reponseuser

StartEndNodes = Tuple[Optional[str], Optional[str]]
from langgraph.graph import StateGraph, START, END

def greeting(graph_builer:StateGraph) -> StartEndNodes:
    graph_builer.add_node("greet", greeting_node)
    graph_builer.add_node("userinput", user_input_node)
    # graph_builer.add_conditional_edges("userinput",...)
    return "greet"

def add_greet(graph_builder:StateGraph) -> StartEndNodes:
    graph_builder.add_node("greet", greeting_node)
    return None, "greet"

def choose_upcomingevent(graph_builder:StateGraph) -> StartEndNodes:
    graph_builder.add_node("ask", user_input_node)
    graph_builder.add_node("choose_events", choose_upcomingevents_node)
    graph_builder.add_edge("ask", "choose_events")
    return "ask", "choose_events"

def tell_upcomingevent_or_response(graph_builder:StateGraph) -> StartEndNodes:
    graph_builder.add_node("user_ask", llm_reponseuser)
    graph_builder.add_node("tell_event", tell_event_node)    
    return None, None