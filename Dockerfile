FROM python

RUN mkdir -p /home/tokenizer

COPY . /home/tokenizer

WORKDIR /home/tokenizer

RUN apt update -y && \
    apt install nano -y && \
    pip install regex 

CMD [ "python3","train.py" ]
# if you want to use the test.py ,replace CMD [ "python3","train.py" ] with CMD [ "python3","test.py" ]
# remove test.py from .dockerignore
