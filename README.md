# Help-Me-Read
Awesome app created with Streamlit + HuggingFace🤗 to get summary, question-answer, translate to language from given input text. It uses [T5 (Text-To-Text Transfer Transformer)](https://github.com/google-research/text-to-text-transfer-transformer#released-model-checkpoints) for summaries/translation and ['Question Generation using transformers'](https://github.com/patil-suraj/question_generation) for question answer generation.

## Installation
- Install conda/miniconda.
- Inside Anaconda prompt create a new env using requirements.txt '$ conda env create --file requirements.txt -name myenv'
- Activate the env '$ activate myenv'
- Install punkt '$ python -m nltk.downloader punkt' (i couldn't put this one inside requirements.txt).

## Run
- Just hit '$ streamlit run to_the_folder/help_me_read.py' inside Anaconda prompt.

## Future
- Reduce the inference time by using smaller models.
- Take inputs from URLs directly.
