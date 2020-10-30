# Help-Me-Read [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1D-Gntt8EAPWyP2QEpKV6dnZCglTbXi32?usp=sharing)
An End-To-End machine learning web application created with Flask + BootStrap + HuggingFace🤗 to generate summary and question-answer from given input text. It uses [T5 (Text-To-Text Transfer Transformer)](https://github.com/google-research/text-to-text-transfer-transformer#released-model-checkpoints) for summaries and ['Question Generation using transformers'](https://github.com/patil-suraj/question_generation) for question answer generation.
#### Some details: 
This is a Web application is created with flask(a python microframework), for NLP models HuggingFace is used and for styling and other purposses HTML+CSS+Javascript is used. The goal was to help user read their text, it can be a blog text, some long passage etc. This application takes advantage of multitask model nameed T5 to generate abstractive summary, generate questions from the given text and verify thier answers using a NLP technique called Semantic textual similarity (MRPC in short).
To get started, user needs to input some text they want to read, then can summarize the given text or also can generate questions based on the texts summary. User can later attend the questions generated to verify their knowledge about the text and can also get results of they did from the model. 
## Requirements
```
pytorch 1.6.0 or above
transformers 3.1.0 or above
```

## Installation
- Install conda/miniconda.
- Inside Anaconda prompt create a new env `$ conda env create -name helpmeread_env`
- Activate the env `$ activate helpmeread_env`
- Upgrade pip `$ pip install -U pip`
- Install dependencies `$ pip install -r requirements.txt`
- Finally Install punkt `$ python -m nltk.downloader punkt`

## Run
- From Anaconda prompt cd to the directory and hit `python wsgi.py`.
#### Note: When running this for the first time models will be downloaded(~400mb).

## Future
- Cheap/Efficient Extractive Summarization.
- Get MiniLM to work.
- Take inputs from URLs directly.

## Screens
Home
