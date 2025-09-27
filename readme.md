## Code Convention
python: pep8

Code and Folder structure:
*Basically, i aim for modular coding experience where each components can be its own 
states < fn_tools (partial) < nodes < graphs < main (or something else)
-----------------------------------------------

These should be seperated in its own folder
*

- All states should be under states folder, could be divided into parts with special decorator (see states section) to combine into a large app state automatically  
- Functions call, function that do not take app states as input can be put uder fn_tools folder  
- Under nodes folder, all function must take app states as input  
- For graphs, i think they should be put under graphs folder  
- Under tests folder, i usually put sample datas there  
- llms is where you would put your llms, could be your trained model or api
- Since this is a simple project, i will put every datas under datas folde: pdf, documents (for RAGs), database (for loggin in). In practice, we would need a different code base for this

## States

Since we need one big state for the whole application (what?), i have made dynamic class that auto combine any `dataclass` classes with decorator `from states.decorator import include_in_appstate`

Example usage of construction:

```python
from dataclasses import dataclass
from states.decorator import include_in_appstate

@dataclass
class EventState: # will not be included
    name: str
    description: str
    time: str
    place: str

@include_in_appstate
@dataclass
class SchoolState:
    location: str
    upcoming_events: List[EventState]

    @property
    def name(self) -> str:
        return "FPT University"
```

Later usage in nodes (functions should use exciplit states imported manually):

```python
from fn_tools.greeting_with_events import greeting_with_events
from states import AppState

def greeting_node(state:AppState) -> AppState:
    greet = greeting_with_events(state.studentstate, state.schoolstate)
    state.messages.append(greet)

    return state
```

Or in test you can see in test/student_school_event_state_test.py about how to construct one

```python
from states.students_states import StudentState
from states.school_state import EventState, SchoolState
from states import AppState

student_sample = StudentState(...)
event1 = EventState(...)
event2 = EventState(...)
school_sample = SchoolState(..., upcoming_events=[event1, event2])

app_state = AppState(
    studentstate=student_sample,
    schoolstate=school_sample
)
```

## fn_tools

This is the place where the logics of nodes lie. This is the bare level of functional.
*You can expect*:
- Individual classes as input as well as returns
- I recommend to call llms here, as you only need to use llm to solve problems, and this is the lowest one that could do so
- All prompts should be put this this level, for now, each functions has their own prompt as they are different functionally
- All functional tools should be here too, since they can not be standalone nodes
- Can only import from state
- In ultils, there are some warper that you can use

Example code:
``` python
from llms.gemini import gemini

def tell_events(event_str: str, user_query: str): # individual classes as input
    system_msg = """You are an ... relevant."""

    user_msg = f""" User query: {user_query} Selected events: {event_str}""" # all prompts here

    resp = gemini.invoke([
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_msg},
    ])

    return resp.content
```

## nodes

This is where standalone nodes are defined, use fn_tools, and state.AppState for typing only
*You can expect*:
- Only functions are being imported and called
- Takes the whole AppState as input and returns a whole dict
- Do not try to import llm here, however, since this is too strict (could create a lot of boiler plates), there is ultils.py where you can call llm exciplitly.

Example code:
```python
from fn_tools.greeting_with_events import greeting_with_events # only from fn_tools
from states import AppState # only for typing

def greeting_node(state:AppState) -> AppState: # input, output are AppState and dict
    greet = greeting_with_events(state.studentstate, state.schoolstate)
    return {"messages": [greet]}
```

## nodes (router)

Since i usually say "router nodes" so all router should be put in here also. There are many reasons to put routers under the same folder as nodes:

- Fixed type of input, output: takes the whole states and returns other nodes name (str)
- Can be its own nodes (fully functional)
- Do not necessary depend on functional calls (only if else or simple logic)
- Functionally operate on node level (from inputs of previous node, choose the next node)

Example code:
```python
from states import AppState

def event_router(state:AppState) -> str:
    msgs = state.cache
    if not msgs:
        return "user_ask"    
    else:
        return "tell_event"
```

## graphs

I am doing one big graph contain many smaller graphs, so, each functions defined in this should:
- Take graph_builder StateGraph as input, and returns a tuple of starting node and end node 
*The return type is defined as:*
``` python
StartEndNodes = Tuple[Optional[str], Optional[str]]
```
- The logic of this layer is to create seperate graph, knowing start and end node of this new graph 

Example code:

``` python
from nodes.greeting_node import ask_node, choose_upcomingevents_node
from langgraph.graph import StateGraph

StartEndNodes = ...

def add_greet(graph_builder:StateGraph) -> StartEndNodes: # input are StateGraph, output are tuple of str
    graph_builder.add_node("greet", greeting_node) # only add nodes
    return None, "greet" # no start, only end node is greet

def choose_upcomingevent(graph_builder:StateGraph) -> StartEndNodes:
    graph_builder.add_node("ask", ask_node)         
    graph_builder.add_node("choose_events", choose_upcomingevents_node)
    graph_builder.add_edge("ask", "choose_events") # create additional two nodes, then connect them
    return "ask", "choose_events" # return start and end node of this subgraph
```
In usage:

``` python 
# main.py

from states import AppState
from graphs.greeting_graph import add_greet, choose_upcomingevent
from langgraph.graph import StateGraph, START, END

graph = StateGraph(AppState)

_, greetnode = add_greet(graph) # greet subgraaph None -> ... -> greetnode
ask, eventnode = choose_upcomingevent(graph) # upcoming event subgraph  ask -> ... -> eventnode

graph.add_edge(START, greetnode)    # START  -> None -> ... -> greetnode
graph.add_edge(greetnode, ask)      # START  -> None -> ... -> greetnode -> ask -> ... -> eventnode
graph.add_edge(eventnode, END)      # START  -> None -> ... -> greetnode -> ask -> ... -> eventnode -> END
```


## How to build the main graph

- Create subgraph from graphs module
- Connect those subgraphs by the start and end nodes of each subgraph
- Profit

``` python
# main.py
from states import AppState
from graphs.greeting_graph import add_greet, choose_upcomingevent, event_router, tell_upcomingevent_or_response
from langgraph.graph import StateGraph, START, END

graph = StateGraph(AppState)
_, greetnode = add_greet(graph) 
ask, eventnode = choose_upcomingevent(graph)
tell_upcomingevent_or_response(graph)       # this does not start and end with any, you will see why later

graph.add_edge(START, greetnode)
graph.add_edge(greetnode, ask)
graph.add_conditional_edges(
    eventnode,
    event_router        # this takes care of the calling of tell_upcomingevent_or_response subgraph
)

app = graph.compile()
```