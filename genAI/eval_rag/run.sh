#!/usr/bin/sh

# generate the answer from a data store
papermill '[1]_rag_workflow.ipynb' 'rag_output.ipynb' \
    -p data_store_id '' \
    -p input_file '' \
    -p location '' \
    -p project_id ''

# evaluate the output compare to the actual answer
papermill '[2]_eval_workflow.ipynb' 'eval_output.ipynb' \
    -p FILE_INPUT '' \
