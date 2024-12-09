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

#result= retrieval("How plant-based diets help prevent specific diseases.")
#result=retrieval("Natural treatments for rheumatoid arthritis.")
#result=retrieval("Effects of high-cholesterol foods on heart disease risk.")
#result=retrieval("Traditional medicine vs. holistic treatments.")
#result=retrieval("Studies on the effectiveness of Vitamin D in cancer prevention.")
"""
# Imprimir os documentos e scores de cada pesquisa
print("VS (Pesquisa 1):")
for doc in result['VS']['VS']:
    print(f"Document ID: {doc['doc_id']}, Score: {doc['score']}")

# Imprimir a quantidade de documentos da pesquisa VS
vs_docs = result['VS']['VS']
print(f"\nQuantidade de documentos retornados na pesquisa VS: {len(vs_docs)}")

print("\nKW (Pesquisa 2):")
for doc in result['KW']['KW']:
    print(f"Document ID: {doc['doc_id']}, Score: {doc['score']}")

# Imprimir a quantidade de documentos da pesquisa KW
kw_docs = result['KW']['KW']
print(f"\nQuantidade de documentos retornados na pesquisa KW: {len(kw_docs)}")

# Encontrar os documentos em comum entre as duas pesquisas
vs_doc_ids = {doc['doc_id'] for doc in vs_docs}
kw_doc_ids = {doc['doc_id'] for doc in kw_docs}

# Documentos em comum
common_docs = vs_doc_ids.intersection(kw_doc_ids)

# Imprimir os documentos em comum
print("\nDocumentos em comum nas duas pesquisas:")
for doc_id in common_docs:
    print(doc_id)

# Imprimir a quantidade de documentos em comum
print(f"\nQuantidade de documentos em comum: {len(common_docs)}")"""

#print(result)