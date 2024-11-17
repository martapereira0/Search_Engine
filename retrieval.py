from haystack import Pipeline

from haystack import Pipeline
from spacy_ner import SpacyNERComponent


def retrieval_pipeline(prompt):
    """  
        Lida com a prompt e faz as pesquisas

    """

    p = Pipeline()
    p.add_component("VS", SearchVS())
    p.add_component("KW", SearchKW())

    
    res = p.run({"user_prompt": prompt})
    return res