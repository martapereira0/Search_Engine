from elasticsearch import Elasticsearch
from elasticsearch import Elasticsearch
from haystack.components.embedders import SentenceTransformersTextEmbedder, SentenceTransformersDocumentEmbedder
from haystack import component, Document
from sentence_transformers import SentenceTransformer
import spacy
from typing import List,Dict
import hashlib


nlp = spacy.load("en_core_web_sm")

# key="4pd-HHNXzRF_yapcrUOn"
key="FS2ICIGE6xeta*f8dzwf"

@component
class SearchVS():
    
    def __init__(self,size) -> None:
        self.size=size

    @component.output_types(documents=List[Document])
    def run(self,prompt_mod: Dict):
        # Conectar ao Elasticsearch
        es = Elasticsearch(
            hosts="https://localhost:9200",
            http_auth=("elastic", key),
            verify_certs=False
        )

        keyword_prompts = prompt_mod.get("vector_prompt", []) 
        if not keyword_prompts or not isinstance(keyword_prompts, list):  
            raise ValueError("O dicionário de entrada não contém a chave 'vector_prompt' ou ela não é uma lista.")  
          
        all_documents = []  
  
        for user_prompt in keyword_prompts:
            embedder = SentenceTransformersTextEmbedder()

            # Inicializa o modelo de embeddings
            embedder.warm_up()
            # Inicializa o modelo de embeddings

            prompt_mimi=embedder.run(user_prompt)
            # print(len(prompt_mimi['embedding']))

            queryVec = {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'content') + 1.0",
                        "params": {"query_vector": prompt_mimi["embedding"]}
                    }
                }
            }

            results = []
            seen_ids = set()  # Set para controlar IDs já vistos

            response = es.search(index="vector_index", body={"query": queryVec, "size": self.size})

            for hit in response['hits']['hits']:
                doc_id = hit['_source']['doc_id']
                score = hit['_score']
                if doc_id not in seen_ids:
                    doc=Document(  
                    id=hashlib.sha256(doc_id.encode()).hexdigest(),
                    content=doc_id,
                    score=score  
                )
                    seen_ids.add(doc_id)  # Marca o ID como já visto
            all_documents.append(doc)
        print("VS", all_documents)
        return {"documents": all_documents}
    
@component
class SearchKW():

    def __init__(self,size) -> None:
        self.size=size

    @component.output_types(documents=List[Document])
    def run(self,prompt_mod:Dict):
        es = Elasticsearch(
            hosts="https://localhost:9200",
            http_auth=("elastic", key),
            verify_certs=False
        )
        all_results = []
        keyword_prompts = prompt_mod.get("keyword_prompt", [])  
        if not keyword_prompts or not isinstance(keyword_prompts, list):  
            raise ValueError("O dicionário de entrada não contém a chave 'keyword_prompt' ou ela não é uma lista.")  
        print(prompt_mod)
        print(keyword_prompts)
        # for keyword in keyword_prompts[0]:
        user_prompt=extract_keywords(keyword_prompts[0])
        # for prompt in user_prompt:
            # Consulta por uma única keyword
        print(user_prompt)
        response = es.search(
            index="keyword_index",
            query = {
                "bool": {
                    "should": [
                        {"match": {"content": keyword}} for keyword in user_prompt
                    ],
                    "minimum_should_match": 1
                }
            },
            size=self.size  # Número de resultados retornados por busca
        )
        # Adicionar resultados à lista geral
        for hit in response['hits']['hits']:
            doc_id = hit['_source']['doc_id']
            score = hit['_score']
            doc=Document(  
            id=hashlib.sha256(doc_id.encode()).hexdigest(),
            content=doc_id,    
            score= score,

                
        )                      
            all_results.append(doc)

        print("KW", all_results)
        return {"documents": all_results}
    


def extract_keywords(text):
    # Processar o texto
    print(text)
    doc = nlp(text)
    # Extrair substantivos ou palavras relevantes
    keywords = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]
    print(keywords)
    print("---")
    return keywords
