import nltk
nltk.download('punkt_tab')

import ir_datasets
from nltk.tokenize import sent_tokenize
import spacy
from sentence_transformers import SentenceTransformer
import json
import pickle


# 2. Carregar o Dataset NFCorpus
dataset = ir_datasets.load("beir/nfcorpus")

# Verificar estrutura
#print(f"Campos disponíveis no dataset: {dataset.docs_cls()._fields}")

# 3. Pré-processamento: Segmentar os Documentos em Frases
#nltk.download('punkt')  # Baixar o pacote de segmentação de frases

documents = []
for doc in dataset.docs_iter():
    doc_id = doc.doc_id
    text = doc.text
    sections = sent_tokenize(text)  # Segmentação em frases
    documents.append({"doc_id": doc_id, "sections": sections})

#print("Documento segmentado:", documents[:1])  # Exibe os primeiros documentos segmentados

# 4. Aplicar NER (Reconhecimento de Entidades Nomeadas)
#spacy.cli.download("en_core_web_sm")  # Baixar o modelo de NER do spaCy

nlp = spacy.load("en_core_web_sm")  # Carregar o modelo de NER
entities = []

for document in documents:
    for section in document["sections"]:
        doc = nlp(section)
        for ent in doc.ents:
            entities.append({"doc_id": document["doc_id"], "text": ent.text, "label": ent.label_})

# Salvar as entidades extraídas em um ficheiro JSON
with open('entities.json', 'w') as f:
    json.dump(entities, f)

#print("Entidades extraídas:", entities[:5])  # Exibe as primeiras entidades extraídas

# 5. Geração de Embeddings para Busca Vetorial
model = SentenceTransformer('all-MiniLM-L6-v2')  # Carregar modelo de embeddings

embeddings = []
for document in documents:
    for section in document["sections"]:
        vector = model.encode(section)  # Gerar embeddings para cada secção
        embeddings.append({"doc_id": document["doc_id"], "section": section, "vector": vector.tolist()})

# Salvar os embeddings gerados em um ficheiro binário
with open('embeddings.pkl', 'wb') as f:
    pickle.dump(embeddings, f)
