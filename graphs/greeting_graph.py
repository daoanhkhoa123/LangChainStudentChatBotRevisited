
from states import AppState
from nodes.greeting_node import greeting_node, choose_upcomingevents_node, tell_event_node
from . import StartEndNodes

from langgraph.graph import StateGraph, START, END

def greeting(graph_buidler:StateGraph) -> StartEndNodes:
    graph_buidler.add_node("greet", greeting_node)
    graph_buidler.add_node("choose_events", choose_upcomingevents_node)
    graph_buidler.add_edge("greet", "choose_events")
    return "greet", "choose_events"

def tell_upcomingevent(graph_builder:StateGraph) -> StartEndNodes:
    graph_builder.add_node("tell_event", tell_event_node)    
    return "tell_event", "tell_event"