from elasticsearch import Elasticsearch

# Conexão com o Elasticsearch
es = Elasticsearch(
    hosts="https://localhost:9200",
    basic_auth=("elastic", "4pd-HHNXzRF_yapcrUOn"),
    verify_certs=False
)

# Nome do índice a ser deletado
index_name = "vector_index"

# Apagar o índice
try:
    response = es.indices.delete(index=index_name, ignore=[400, 404])  # Ignora erros de índice inexistente
    print(f"Índice '{index_name}' deletado com sucesso.")
except Exception as e:
    print(f"Erro ao deletar o índice: {e}")