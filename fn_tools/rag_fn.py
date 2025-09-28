import os
from datas import DOCUMENTS, get_index_path, get_doc_path
from llms.gemini import gemini, gemini_embedding

from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA

def choose_document_prompt(prompt:str):
    system_msg = f"""
    You are a document chooser.
    Available documents: {DOCUMENTS}
    Rules:
    - Read the user input carefully.
    - RETURN ONLY the file name EXACTLY as it appears in DOCUMENTS.
    - Do not write anything else.
    """
    user_msg = prompt

    resp = gemini.invoke([
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_msg}
    ]).content.strip()

    return resp

def build_or_load_index(docname:str):
    print(get_doc_path(docname))
    print(get_index_path(docname))
    try:
        vectordb = FAISS.load_local(get_index_path(docname), gemini_embedding, allow_dangerous_deserialization=True)
    except:
        loader = PyPDFLoader(get_doc_path(docname))
        pages =loader.load()
        vectordb = FAISS.from_documents(pages, gemini_embedding)
        vectordb.save_local(get_index_path(docname))
    
    return vectordb

def build_qa_chain(doc_name):
    retriever = build_or_load_index(doc_name).as_retriever()
    return RetrievalQA.from_chain_type(
    llm=gemini,
    retriever=retriever,
    return_source_documents=True
    )
