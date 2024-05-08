import os
from .tokenization import basic_tokenizer
text= open('taylorswift.txt','r',encoding='utf-8').read()

os.makedirs('models',exist_ok=True)
 
tokenizer=basic_tokenizer()
tokenizer.train(text,)
