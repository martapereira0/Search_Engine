import ir_datasets

dataset = ir_datasets.load("nfcorpus")
for doc in dataset.docs_iter():
    doc


