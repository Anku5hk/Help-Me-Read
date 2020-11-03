FROM ubuntu:16.04

MAINTAINER Ankush Kuwar "https://github.com/Anku5hk/"

RUN apt update && \
    apt install -y python3.8 python3-pip git && \
    pip3 install --upgrade pip && \
    git clone https://github.com/Anku5hk/Help-Me-Read.git && \ 
    cd Help-Me-Read/ && pip install -r reqiuirements.txt --no-cache-dir && \
    python3 -m nltk.downloader punkt 	 	

EXPOSE 5000

ENTRYPOINT [ "python" ]

CMD [ "gunicorn --bind 0.0.0.0:5000 wsgi:app" ]
