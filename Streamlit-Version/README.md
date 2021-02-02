# Help-Me-Read [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1D-Gntt8EAPWyP2QEpKV6dnZCglTbXi32?usp=sharing)
Awesome app created with Streamlit + HuggingFace🤗 to get summary, question-answer, translate to language from given input text. It uses [T5 (Text-To-Text Transfer Transformer)](https://github.com/google-research/text-to-text-transfer-transformer#released-model-checkpoints) for summaries/translation and ['Question Generation using transformers'](https://github.com/patil-suraj/question_generation) for question answer generation.
#### Some details: 
The Goal of this project is to meaningfully summarize huge posts/blogs using machine learning. Also to get text marked for important sentences, to save time while reading huge posts. 
It uses T5 model, pre-trained on C4(Colossal Clean Crawled Corpus) which is a very huge unlabeled text dataset, achieve SOTA results on many NLP benchmarks while being flexible enough to be fine-tuned for other tasks. Using T5 allows to use the same model, loss function, and hyperparameters on any NLP task, including machine translation, document summarization, question answering, and classification tasks. Using T5 is so simple that one needs to input text like "summarize: text-needed-to-be-summarize-here" and it'll give output summary for the text, Awesome!!. I have used the t5-small(which has 60 million parameters)for summarization which is the smallest available and the HuggingFace version due to its ease of use. T5 does abstractive summarization which is a technique in which the summary is generated and not extracted. For question answer generation there were new recent models like MiniLM and ProphetNet but they are a bit hard to get working. The defualt T5 only generates answers given text and questions, So currently i have used another pretrained t5-small which can generate QAs given only text and it works just fine.   

## Requirements
```
pytorch 1.6.0
streamlit
transformers 3.1.0
```

## Installation
- Install conda/miniconda.
- Inside Anaconda prompt create a new env using requirements.txt `$ conda env create --file requirements.txt -name myenv`
- Activate the env `$ activate myenv`
- Install punkt `$ python -m nltk.downloader punkt` (i couldn't put this one inside requirements.txt).

## Run
- Just hit `$ streamlit run to_the_folder/help_me_read.py` inside Anaconda prompt.
#### Note: When running this for the first time models will be downloaded(~500mb).

## Future
- Cheap/Efficient Extractive Summarization.
- Process large text.
- Reduce the inference time by using smaller models.
- Take inputs from URLs directly.

## Screens
Home
![3](/Streamlit-Version/screens/home.png)
Summarization
![2](/Streamlit-Version/screens/QAs.png)
Questions and Answers
![1](/Streamlit-Version/screens/summarize.png)
