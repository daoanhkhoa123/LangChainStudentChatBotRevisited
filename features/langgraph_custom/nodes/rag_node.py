from states import AppState
from fn_tools.rag_fn import choose_document_prompt, build_qa_chain
from langchain.chains import RetrievalQA


def choose_document_node(appstate:AppState) -> AppState:
    appstate.user_input = input("What document do you want to read:\n")
    doc_name = choose_document_prompt(appstate.user_input)
    return {"cache": [doc_name]}

def rag_node(appstate:AppState) -> AppState:
    if not appstate.cache[-1]:
        return {"messages": ["Sorry, i can not find the document you wanted"]}

    qa_chain = build_qa_chain(appstate.cache[-1])
    appstate.user_input = input("What do you want to ask?\n")
    res = qa_chain.invoke(appstate.user_input)

    msg = res["result"]
    soucres = [doc.metadata.get("source", "unknown") for doc in res["source_documents"]]
    return {"messages": [msg], "cache": soucres}

    