from llms.gemini import gemini
from states import AppState

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

from typing import Dict


def llm_reponseuser(state:AppState):
    response = gemini.invoke([
        {"role": "user", "content": state.user_input},
    ])
    return {"messages": [response.content]}

def llm_responsesystem(prompt):
    response = gemini.invoke([
        {"role": "system", "content": prompt},
    ])

    return {"messages": [response.content]}

def str_pooling_tfidf(key: str, dict: Dict[str,str]) -> str:
    keys, values = zip(*dict.items())
    corpus = [key] + [k + v for k, v in zip(keys, values)]
    vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(1, 3))
    tfidf_matrix = vectorizer.fit_transform(corpus)
    
    key_vec = tfidf_matrix[0] # type: ignore
    value_vecs = tfidf_matrix[1:] # type: ignore
    
    sims = (value_vecs @ key_vec.T).toarray().flatten()
    return keys[np.argmax(sims)]
