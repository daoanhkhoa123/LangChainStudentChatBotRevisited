import os

BASE_DIR = os.path.dirname(__file__)
DOCUMENT_EXTENSIONS = {".pdf", ".doc", ".docx", ".txt"}

DOCUMENTS = [
    f for f in os.listdir(BASE_DIR)
    if os.path.isfile(os.path.join(BASE_DIR, f))
    and os.path.splitext(f)[1].lower() in DOCUMENT_EXTENSIONS
]

def get_doc_path(docname:str):
    return os.path.join("datas", docname)

def get_index_path(docname:str):
    return os.path.join("datas", f"{docname}_index")

if __name__ == "__main__":
    print("Documents found in datas folder:")
    for doc in DOCUMENTS:
        print(doc)
