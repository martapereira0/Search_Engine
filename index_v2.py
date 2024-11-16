from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

# Conectar ao Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

import pickle
# Carregar os embeddings gerados do ficheiro binário
with open('embeddings.pkl', 'rb') as f:
    embeddings = pickle.load(f)

import json
with open('entities.json', 'r') as f:
    entities = json.load(f)

# Criar índice de vetores
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

# Indexar embeddings
actions = []
for i, embedding in enumerate(embeddings):
    actions.append({
        "_op_type": "index",
        "_index": "vector_index",
        "_id": i,
        "_source": embedding
    })
bulk(es, actions)
print("Embeddings indexados com sucesso.")

# Criar índice de keywords
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

# Indexar entidades
actions = []
for i, entity in enumerate(entities):
    actions.append({
        "_op_type": "index",
        "_index": "keyword_index",
        "_id": i,
        "_source": entity
    })
bulk(es, actions)
print("Entidades indexadas com sucesso.")
