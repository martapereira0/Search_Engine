import ir_datasets
from haystack import Pipeline
from haystack import Document
from haystack import Pipeline
from haystack.components.preprocessors import DocumentSplitter
from writer import save_vs,save_kw
from retriever import SearchVS,SearchKW
from spacy_ner import SpacyNERComponent

dataset = ir_datasets.load("beir/nfcorpus")

haystack_docs = [
    Document(
        content=doc.text,
        meta={"doc_id": doc.doc_id, "title": doc.title}
    )
    for doc in dataset.docs_iter()
]

#Para testar usamos poucos docs
haystack_docs=haystack_docs[:2]



def indexing(docs):
    indexing_pipeline = Pipeline()
    #COmponente que add à base de dados elastic por keywords
    indexing_pipeline.add_component("spacy_ner", SpacyNERComponent())# Componente spacy que classifica NER e adiciona aos metadados
    indexing_pipeline.add_component("writer_kw", save_kw()) # Escreve documentos no Elasticsearch
    indexing_pipeline.add_component("splitter", DocumentSplitter(split_by="sentence", split_length=3, split_overlap=0))
    indexing_pipeline.add_component("writer_vs", save_vs()) # Escreve documentos no Elasticsearch

    # # conectar todos os componentes
    indexing_pipeline.connect("spacy_ner","writer_kw")
    indexing_pipeline.connect("spacy_ner", "splitter")
    indexing_pipeline.connect("splitter", "writer_vs")


    res=indexing_pipeline.run({
    "documents": docs
    })

    return "Indexação concluida"






def retrieval(prompt):
    retrieval_pipeline = Pipeline()
    retrieval_pipeline.add_component("VS", SearchVS())
    retrieval_pipeline.add_component("KW", SearchKW())

    res = retrieval_pipeline.run({"VS":{"user_prompt": prompt},"KW": {"user_prompt": prompt}})

    print(res)