import ir_datasets

dataset = ir_datasets.load("cranfield")
for query in dataset.queries_iter():
    print(query)


