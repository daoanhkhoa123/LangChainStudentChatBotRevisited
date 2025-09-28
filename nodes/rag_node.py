from states import AppState
from fn_tools.rag_fn import choose_document_prompt, build_qa_chain
from langchain.chains import RetrievalQA


def choose_document_node(appstate:AppState) -> AppState:
    appstate.user_input = input("What document do you want to read:\n")
    doc_name = choose_document_prompt(appstate.user_input)
    return {"cache": [doc_name]}

def rag_node(appstate:AppState) -> AppState:
    qa_chain = build_qa_chain(appstate.cache[-1])
    appstate.user_input = input("What do you want to ask?\n")
    msg = qa_chain.run(appstate.user_input)
    return {"messages": [msg]}
    