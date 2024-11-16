import spacy
from haystack import component, Document

@component
class SpacyNERComponent:
    def __init__(self, model_name="en_core_web_sm"):
        self.nlp = spacy.load(model_name)

    @component.output_types(documents=list[Document])
    def run(self, documents: list[Document]):
        for doc in documents:
            doc_nlp = self.nlp(doc.content)
            entities = [(ent.text, ent.label_) for ent in doc_nlp.ents]
            doc.meta["entities"] = entities
        return documents # docs com as entidades já adicionadas aos metadados
