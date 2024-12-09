import ir_datasets
from haystack import Pipeline
from haystack import Document
from haystack import Pipeline
from haystack.components.preprocessors import DocumentSplitter
from writer import save_vs,save_kw
from llm import LLMPrompt,JoinDocuments
from retriever import SearchVS,SearchKW
from spacy_ner import SpacyNERComponent
import os

dataset = ir_datasets.load("beir/nfcorpus")

haystack_docs = [
    Document(
        content=doc.text,
        meta={"doc_id": doc.doc_id, "title": doc.title}
    )
    for doc in dataset.docs_iter()
]


#Para testar usamos poucos docs
# haystack_docs=haystack_docs[:2]

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

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






def retrieval(prompt,size):

    join_documents = JoinDocuments(join_mode="distribution_based_rank_fusion")
    retrieval_pipeline = Pipeline()
    retrieval_pipeline.add_component("PE",LLMPrompt())
    retrieval_pipeline.add_component("VS", SearchVS(size))
    retrieval_pipeline.add_component("KW", SearchKW(size))
    retrieval_pipeline.add_component("JD",join_documents)
    retrieval_pipeline.connect("PE","VS")
    retrieval_pipeline.connect("PE","KW")
    retrieval_pipeline.connect("KW","JD")
    retrieval_pipeline.connect("VS","JD")
    res = retrieval_pipeline.run({"user_prompt": prompt})
    
    return res

#indexing(haystack_docs)

result= retrieval("How plant-based diets help prevent specific diseases.",5)
print(result)