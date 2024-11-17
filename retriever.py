from elasticsearch import Elasticsearch
from elasticsearch import Elasticsearch
from haystack.components.embedders import SentenceTransformersTextEmbedder, SentenceTransformersDocumentEmbedder
from haystack import component, Document
from sentence_transformers import SentenceTransformer


key="4pd-HHNXzRF_yapcrUOn"

@component
class SearchVS():
    
    @component.output_types(response=dict)
    def run(self,user_prompt: str):
        # Conectar ao Elasticsearch
        es = Elasticsearch(
            hosts="https://localhost:9200",
            http_auth=("elastic", key),
            verify_certs=False
        )

  

        embedder = SentenceTransformersTextEmbedder()

        # Inicializa o modelo de embeddings
        embedder.warm_up()
        # Inicializa o modelo de embeddings

        prompt_mimi=embedder.run(user_prompt)

        print(len(prompt_mimi['embedding']))

        queryVec = {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'content') + 1.0",
                    "params": {"query_vector": prompt_mimi["embedding"]}
                }
            }
        }

        response = es.search(index="vector_index", body={"query": queryVec, "size": 8})

        results = []
        for hit in response['hits']['hits']:
            doc_id = hit['_source']['doc_id']
            score = hit['_score']
            results.append({'doc_id': doc_id, 'score': score})
        

        return {"VS": results}
@component
class SearchKW():

    @component.output_types(response=dict)
    def run(self,user_prompt:str):
        es = Elasticsearch(
            hosts="https://localhost:9200",
            http_auth=("elastic", key),
            verify_certs=False
        )

        # Consulta por keywords
        response = es.search(
            index="keyword_index",
            query={
                "match_phrase": {
                    "content": user_prompt  # Use o termo textual para busca
                }
            },
            size=8  # Número de resultados retornados
        )

        # Exibição dos resultados
        print(f"Resultados da busca por frase '{user_prompt}':")
        results=[]
        for hit in response['hits']['hits']:
            doc_id = hit['_source']['doc_id']
            score = hit['_score']
            results.append({'doc_id': doc_id, 'score': score})
        

        return {"KW": results}