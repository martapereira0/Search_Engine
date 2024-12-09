from flask import Flask, render_template, request
from PIPELINES import retrieval
import pandas as pd
import ir_datasets
app = Flask(__name__)

# Dados simulados para pesquisa
RESULTS = [
    "Resultado 1",
    "Resultado 2",
    "Outro resultado interessante",
    "Mais um resultado",
    "Resultado de exemplo",
    "Resultado aleatório",
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query', '').lower()
    # Filtrar resultados baseados na pesquisa
    results=retrieval(query,3)['JD']['documents']
    print(results)
    formatted_results = []
    for doc in results:
        dataset = ir_datasets.load("beir/nfcorpus")
        df_docs = pd.DataFrame(dataset.docs_iter())
        doc_id = doc.content
        doc_title = df_docs.loc[df_docs['doc_id'] == doc_id, 'title'].values[0]
        formatted_results.append({'title': doc_title, 'score': doc.score})
    return render_template('results.html', query=query, results=formatted_results)

if __name__ == '__main__':
    app.run(debug=True)
