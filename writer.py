

from elasticsearch import Elasticsearch
from haystack.components.embedders import SentenceTransformersTextEmbedder, SentenceTransformersDocumentEmbedder
from haystack import component, Document


#key="4pd-HHNXzRF_yapcrUOn"
key="qwWTCM+LacryzqIqFlzn"

@component
class save_kw():

    @component.output_types(documents=list[Document])
    def run(self, documents: list[Document]):
        """
        Indexa documentos baseados em keywords no Elasticsearch.

        Args:
            documents (list): Lista de objetos `Document` da biblioteca Haystack.
        """
        print(" A guardar no keyword_index")
        index_name = "keyword_index"

        # Configurar conexão com Elasticsearch
        es = Elasticsearch(
            hosts="https://localhost:9200",
            http_auth=("elastic", key),
            verify_certs=False
        )

        # Criar o índice, se não existir
        keyword_mapping = {
            "mappings": {
                "properties": {
                    "doc_id": {"type": "keyword"},
                    "entity": {"type": "text"},
                    "label": {"type": "keyword"},
                    "content": {"type": "text"},  # Adiciona o campo content
                    "title": {"type": "text"}    # Adiciona o campo title
                }
            }
        }
        es.indices.create(index=index_name, body=keyword_mapping, ignore=400)

        # Processar e indexar os documentos
        for doc in documents:
            # Extrair informações do objeto Document para um dicionário
            doc_body = {
                "doc_id": doc.meta.get("doc_id"),
                "title": doc.meta.get("title"),
                "content": doc.content,
                "entities": doc.meta.get("entities")
            }

            # Indexar o documento
            es.index(index=index_name, id=doc.id, document=doc_body)

        print(f"Documentos indexados no índice '{index_name}' com sucesso.")
        return {"documents": documents}


@component
class save_vs():

    @component.output_types(documents=list[Document])
    def run(self, documents: list[Document]):
        """
        Indexa documentos baseados em embeddings no Elasticsearch.

        Args:
            documents (list): Lista de dicionários com documentos contendo texto para embeddings.
            index_name (str): Nome do índice no Elasticsearch.
            model_name (str): Nome do modelo de embeddings para geração de vetores.
        """
        es = Elasticsearch(
            hosts="https://localhost:9200",
            http_auth=("elastic", key),
            verify_certs=False
        )
        
        print(" A guardar no vector_index")

        # Usar o embedder de documento
        embedder = SentenceTransformersDocumentEmbedder()

        # Inicializa o modelo de embeddings
        embedder.warm_up()  # Prepara o modelo para uso

        # Nome do índice no Elasticsearch
        index_name = "vector_index"

        # Criar o índice, se não existir
        vector_mapping = {
            "mappings": {
                "properties": {
                    "doc_id": {"type": "keyword"},
                    "content": {
                        "type": "dense_vector",
                        "dims": 768  # Ou outro valor de dimensão dependendo do modelo
                    }
                }
            }
        }

        # Criar o índice, caso não exista
        es.indices.create(index=index_name, body=vector_mapping, ignore=400)

        # Gerar os embeddings para os documentos
        embedded_docs = embedder.run(documents)

        # Indexar os documentos no Elasticsearch
        for doc in embedded_docs['documents']:
            # Extraímos o vetor de embeddings diretamente do documento
            vector = doc.embedding
            # Verificar o tamanho do vetor de embedding
            print(f"Tamanho do vetor gerado: {len(doc.embedding)}")


            # Estrutura do documento para indexação
            body = {
                "doc_id": doc.meta.get("doc_id", "unknown"),  # Garantir que 'doc_id' está nos metadados
                "content": vector
            }

            print(doc)

            # Indexar o documento no Elasticsearch
            es.index(index=index_name, id=doc.id, body=body)

        print(f"Documentos indexados no índice '{index_name}' com sucesso.")
        return {"documents": documents}

