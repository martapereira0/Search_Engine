import ir_datasets

dataset = ir_datasets.load("beir/nfcorpus")

docs = dataset.docs_iter()

queries = dataset.queries_iter()


# Create a pandas df with a col for the id, title, text, and url

import pandas as pd

df = pd.DataFrame(columns=['id', 'title', 'text', 'url'])
for iter in docs:
    df = df.append({'id': iter.doc_id, 'title': iter.title, 'text': iter.text, 'url': iter.url}, ignore_index=True)


