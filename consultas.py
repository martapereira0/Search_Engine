from elasticsearch import Elasticsearch

# Conectar ao Elasticsearch
es = Elasticsearch(
    hosts="https://localhost:9200",
    basic_auth=("elastic", "4pd-HHNXzRF_yapcrUOn"),
    verify_certs=False
)

print(es.count(index="keyword_index"))


# Consulta semântica (vetorial)
from sentence_transformers import SentenceTransformer
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

# Carregar modelo para gerar o vetor da query
model = SentenceTransformer('all-MiniLM-L6-v2')
query_vector = model.encode("How fish increases immunity?").tolist()

queryVec = {
    "script_score": {
        "query": {"match_all": {}},
        "script": {
            "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
            "params": {"query_vector": query_vector}
        }
    }
}

response = es.search(index="vector_index", body={"query": queryVec, "size": 8})

print("\nResultados da busca semântica:")
for hit in response['hits']['hits']:
    print(hit["_source"]['doc_id'] + ": " + hit["_source"]['section'] + "\n")

print("\n\n\n")

# Consulta por keywords
query_keyword = "Finland"  # Termo para buscar na indexação de keywords

# Consulta por keywords
response = es.search(
    index="keyword_index",
    query={
        "match_phrase": {
            "content": query_keyword  # Use o termo textual para busca
        }
    },
    size=5  # Número de resultados retornados
)

# Exibição dos resultados
print(f"Resultados da busca por frase '{query_keyword}':")
if response['hits']['hits']:
    for hit in response['hits']['hits']:
        print(hit["_source"])
else:
    print("Nenhum resultado encontrado.")

count = es.count(index="keyword_index")
print(f"\n\n\n Total de documentos no índice 'keyword_index': {count['count']}")
