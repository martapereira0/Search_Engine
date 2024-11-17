from elasticsearch import Elasticsearch

# Conectar ao Elasticsearch
ca_cert_path = "http_ca.crt"

es = Elasticsearch(
    hosts="https://localhost:9200",
    basic_auth=("elastic", "RyioJAFpJA1D*4TPkpfU"),
    verify_certs=False
)

print(es.count(index="keyword_index"))