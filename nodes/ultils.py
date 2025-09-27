from llms.gemini import gemini
from states import AppState
def user_ask(state:AppState):
    response = gemini.invoke([
        {"role": "user", "content": state.user_input},
    ])
    return {"messages": [response.content]}

def system_ask(prompt):
    response = gemini.invoke([
        {"role": "system", "content": prompt},
    ])

    return {"messages": [response.content]}