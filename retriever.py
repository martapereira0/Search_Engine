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
            basic_auth=("elastic", key),
            verify_certs=False
        )


        # Carregar modelo para gerar o vetor da query
        embedder = SentenceTransformer('paraphrase-MiniLM-L6-v2')

        # Gerar o vetor do prompt
        user_prompt_modi = embedder.encode([user_prompt])[0]
        # Inicializa o modelo de embeddings
            

        queryVec = {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                    "params": {"query_vector": user_prompt_modi}
                }
            }
        }

        response = es.search(index="vector_index", body={"query": queryVec, "size": 1})

        print("\nResultados da busca semântica:")
        

        return {"VS": response}
@component
class SearchKW():

    @component.output_types(response=dict)
    def run(self,user_prompt:str):
        es = Elasticsearch(
            hosts="https://localhost:9200",
            basic_auth=("elastic", key),
            verify_certs=False
        )
        # Consulta por keywords

        # Consulta por keywords
        response = es.search(
            index="keyword_index",
            query={
                "match_phrase": {
                    "content": user_prompt  # Use o termo textual para busca
                }
            },
            size=1  # Número de resultados retornados
        )

        # Exibição dos resultados
        print(f"Resultados da busca por frase '{user_prompt}':")
        

        return {"KW": response}