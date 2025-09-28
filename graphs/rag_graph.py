from langgraph.graph import StateGraph

from nodes.rag_node import choose_document_node, rag_node
from . import StartEndNodes

def rag_graph(graph:StateGraph) -> StartEndNodes:
    graph.add_node("choose_document", choose_document_node)
    graph.add_node("rag", rag_node)
    graph.add_edge("choose_document", "rag")
    return "choose_document", "rag"
