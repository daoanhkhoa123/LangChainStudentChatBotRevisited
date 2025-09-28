from functools import partial

from states import AppState
from graphs.greeting_graph import greeting, tell_upcomingevent
from graphs.rag_graph import rag_graph
from nodes.router import router_by_dict, router_event

from langgraph.graph import StateGraph, START, END

graph = StateGraph(AppState)
greet_node, choose_event = greeting(graph)
graph.add_edge(START, greet_node)

# route event telling
tell_event, _ = tell_upcomingevent(graph)

# route rag
choose_document, rag = rag_graph(graph)

feature_dict = {
    choose_document: "Select a document from the available files, then read and process its content using a Retrieval-Augmented Generation (RAG) pipeline to answer questions or summarize information.",
    choose_event: "Retrieve details about upcoming school events (such as name, description, time, and place) and explain them clearly to the user.",
    # "nothing": "Generic chat. Not recommened until you are sure that user do not want to use any functions above"
}
graph.add_conditional_edges(choose_event, 
                            partial(router_event, 
                            dict = feature_dict, res_event = tell_event))

app = graph.compile()

if __name__ == "__main__":
    from tests.conftest import init_appstate
    app_state = init_appstate()

    for event in app.stream(app_state):
        print(event)

