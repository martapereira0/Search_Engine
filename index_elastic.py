from elasticsearch import Elasticsearch
import json
import pickle

# Carregar as entidades extraídas do ficheiro JSON
with open('entities.json', 'r') as f:
    entities = json.load(f)

# Carregar os embeddings gerados do ficheiro binário
with open('embeddings.pkl', 'rb') as f:
    embeddings = pickle.load(f)


# 6. Indexar no Elasticsearch
es = Elasticsearch()

# 6.1 Criar o Índice para Vetores
vector_mapping = {
    "mappings": {
        "properties": {
            "doc_id": {"type": "keyword"},
            "section": {"type": "text"},
            "vector": {"type": "dense_vector", "dims": 384}
        }
    }
}
es.indices.create(index="vector_index", body=vector_mapping, ignore=400)
print("Índice de vetores criado.")

# 6.2 Indexar Embeddings no Elasticsearch
for i, embedding in enumerate(embeddings):
    es.index(index="vector_index", id=i, body=embedding)
print("Dados vetoriais indexados com sucesso.")

# 6.3 Criar o Índice para Keywords
keyword_mapping = {
    "mappings": {
        "properties": {
            "doc_id": {"type": "keyword"},
            "entity": {"type": "text"},
            "label": {"type": "keyword"}
        }
    }
}
es.indices.create(index="keyword_index", body=keyword_mapping, ignore=400)
print("Índice de keywords criado.")

# 6.4 Indexar Keywords no Elasticsearch
for i, entity in enumerate(entities):
    es.index(index="keyword_index", id=i, body=entity)
print("Entidades indexadas com sucesso.")