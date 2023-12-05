# What it is
This code will automatically generate the answer from RAG based workflow
and evaluate the answer based

# How to run
Ensure that all the necessary library requirements is installed correctly
```
google-cloud-aiplatform
google-cloud-discoveryengine
papermill
```

Then open the either `run.sh` or `run.ipynb`
and change the parameter, like the data_store_id and the dataset filename

The result will be the csv files with generated answer and judgement
and it is summarized in the output notebook
