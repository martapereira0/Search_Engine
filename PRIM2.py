#------------------------Pipeline de Indexação------------------------------ 
import ir_datasets
from haystack_integrations.document_stores.elasticsearch import ElasticsearchDocumentStore
from haystack import Pipeline
from haystack_integrations.components.retrievers.elasticsearch import ElasticsearchBM25Retriever
#from haystack.nodes import PreProcessor
from haystack import Document
import spacy
import pandas as pd

from haystack_integrations.document_stores.elasticsearch import ElasticsearchDocumentStore
from haystack import Pipeline
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.converters import TextFileToDocument
from haystack.components.preprocessors import DocumentSplitter
from haystack.components.writers import DocumentWriter 

from spacy_ner import SpacyNERComponent

dataset = ir_datasets.load("beir/nfcorpus")

# Carregar o modelo spaCy para NER 
nlp = spacy.load("en_core_web_sm")

haystack_docs = [
    Document(
        content=doc.text,
        meta={"doc_id": doc.doc_id, "title": doc.title}
    )
    for doc in dataset.docs_iter()
]

document_store = ElasticsearchDocumentStore(hosts = "http://localhost:9200")

splitter = DocumentSplitter()
doc_embedder = SentenceTransformersDocumentEmbedder(model="sentence-transformers/multi-qa-mpnet-base-dot-v1")
writer = DocumentWriter(document_store)
spacy_ner = SpacyNERComponent()

indexing_pipeline = Pipeline()
#COmponente que add à base de dados elastic por keywords
indexing_pipeline.add_component("spacy_ner", instance=spacy_ner)# Componente spacy que classifica NER e adiciona aos metadados
indexing_pipeline.add_component("splitter", splitter)  # Divide documentos grandes
indexing_pipeline.add_component("doc_embedder", doc_embedder) # Embedding dos documentos (faz mais sentido dividir em frases antes deste paço mas não sei bem como mantemos tudo relacionado ao mesmo documento)
# componente para adicionar docs ao elastic por embeddings
indexing_pipeline.add_component("writer", writer) # Escreve documentos no Elasticsearch

# conectar todos os componentes
indexing_pipeline.connect("spacy_ner", "splitter")
indexing_pipeline.connect("splitter", "doc_embedder")
indexing_pipeline.connect("doc_embedder", "writer")


#correr a pipeline 
indexing_pipeline.run({
    "documents": haystack_docs
    })

"""
#------------------------Pipeline de Consulta------------------------------ 

from haystack_integrations.document_stores.elasticsearch import ElasticsearchDocumentStore
from haystack import Pipeline
from haystack.components.embedders import SentenceTransformersTextEmbedder 
from haystack_integrations.components.retrievers.elasticsearch import ElasticsearchEmbeddingRetriever

model = "sentence-transformers/multi-qa-mpnet-base-dot-v1"

document_store = ElasticsearchDocumentStore(hosts = "http://localhost:9200")


retriever = ElasticsearchEmbeddingRetriever(document_store=document_store)
text_embedder = SentenceTransformersTextEmbedder(model=model)

query_pipeline = Pipeline()
query_pipeline.add_component("text_embedder", text_embedder) #embeddings da pergunta para vetorial
query_pipeline.add_component("retriever", retriever) #retriver vetorial
#componente que manda pergunta para o retriever por keywords


query_pipeline.connect("text_embedder.embedding", "retriever.query_embedding")
#conectar todos os componentes

#correr com pergunta
result = query_pipeline.run({"text_embedder": {"text": "historical places in Instanbul"}})

print(result)
"""
