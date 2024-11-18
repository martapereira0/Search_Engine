from elasticsearch import Elasticsearch
from elasticsearch import Elasticsearch
from haystack.components.embedders import SentenceTransformersTextEmbedder, SentenceTransformersDocumentEmbedder
from haystack import component, Document
from sentence_transformers import SentenceTransformer
import spacy

nlp = spacy.load("en_core_web_sm")

#key="4pd-HHNXzRF_yapcrUOn"
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

        response = es.search(index="vector_index", body={"query": queryVec, "size": 100})

        results = []
        for hit in response['hits']['hits']:
            doc_id = hit['_source']['doc_id']
            score = hit['_score']
            if score > 1.0:
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
        all_results = []
        user_prompt=extract_keywords(user_prompt)

        for keyword in user_prompt:
            # Consulta por uma única keyword
            response = es.search(
                index="keyword_index",
                query={
                    "match_phrase": {
                        "content": keyword  # Use cada termo textual para busca
                    }
                },
                size=8  # Número de resultados retornados por busca
            )

            # Adicionar resultados à lista geral
            for hit in response['hits']['hits']:
                doc_id = hit['_source']['doc_id']
                score = hit['_score']
                all_results.append({'doc_id': doc_id, 'score': score})

        # Ordenar os resultados por score em ordem decrescente
        all_results = sorted(all_results, key=lambda x: x['score'], reverse=True)

        # Remover duplicados, mantendo o maior score (opcional)
        unique_results = {}
        for result in all_results:
            if result['doc_id'] not in unique_results:
                unique_results[result['doc_id']] = result

        # Selecionar os 8 documentos com maior score
        final_results = list(unique_results.values())[:8]
        

        return {"KW": final_results}
    


def extract_keywords(text):
    # Processar o texto
    doc = nlp(text)
    # Extrair substantivos ou palavras relevantes
    keywords = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]
    return keywords
