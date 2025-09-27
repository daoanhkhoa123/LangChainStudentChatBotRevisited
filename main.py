from states import AppState
from graphs.greeting_graph import add_greet, choose_upcomingevent, event_router, tell_upcomingevent_or_response

from langgraph.graph import StateGraph, START, END

graph = StateGraph(AppState)
_, greetnode = add_greet(graph)
ask, eventnode = choose_upcomingevent(graph)
tell_upcomingevent_or_response(graph)

graph.add_edge(START, greetnode)
graph.add_edge(greetnode, ask)
graph.add_conditional_edges(
    eventnode,
    event_router
)

app = graph.compile()


if __name__ == "__main__":
    from tests.student_school_event_state_test import app_state

    for event in app.stream(app_state):
        print(event)

