import regex as re

gpt2pat = re.compile(r"""'s|'t|'re|'ve|'m|'ll|'d| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+""")

def get_stats(ids,counts=None):
    counts={} if counts is None else counts
    for pair in zip(ids,ids[1:]):
        counts[pair]=counts.get(pair,0)+1
    return counts

def merge(tokens,pair,target):
    newtokens=[]
    i=0
    while i < len(tokens):
        if i<len(tokens)-1 and tokens[i]==pair[0] and tokens[i+1]==pair[1]:
            newtokens.append(target)
            i+=2
        else:
            newtokens.append(tokens[i])
            i+=1
    return newtokens 

def make_tokens(compiled_pattern,text):    #return tokenized chunks of text_chunks defined by re.findall()
      text_chunk=re.findall(compiled_pattern, text)
      tokens=[list(chunk.encode('utf-8')) for chunk in text_chunk]
      return tokens


class special_tokenizer:
    def __init__(self,pattern=None) -> None:
        self.pattern=gpt2pat if pattern is  None else pattern
        self.compiled_pattern=re.compile(self.pattern)
        self.special_tokens={}
        self.inverse_special_tokens={}
        self.vocab={}
        self.merges={}

    def train(self,text) :
        tokens=make_tokens(self.compiled_pattern,text)
        merges = {} # (int, int) -> int
        vocab={k:bytes([k]) for k in range(256)}
        for i in range(10):
            stats = {}
            for chunk_ids in tokens:
                get_stats(chunk_ids, stats)
            pair = max(stats, key=stats.get)
            idx = 256 + i
            ids = [merge(chunk_ids, pair, idx) for chunk_ids in tokens]
            merges[pair] = idx
            vocab[idx]=vocab[pair[0]]+vocab[pair[1]]
        self.merges=merges
        self.vocab=vocab

    def register_special_tokens(self,s):
        self.special_tokens=s
        self.inverse_special_tokens={v:k for k,v in self.special_tokens.items()}

    def decode(self,tokens):
        bytes=[]
        for token in tokens:
            if token in self.vocab:
                bytes.append(self.vocab[token])
            elif token in self.special_tokens:
                bytes.append(self.special_tokens[token].encode('utf-8'))
            else:
                raise ValueError('invalid token')
        text_bytes=b''.join(bytes)
        raw_text=text_bytes.decode('utf-8',errors='replace')
        return raw_text
    
    def encode_chunk(self,chunk_tokens):
        ids=list(chunk_tokens)
        while len(ids)>=2:
            stats=get_stats(ids)
            pair=min(stats,key= lambda p: self.merges.get(p,float('inf')))
            if pair not in self.merges:
                break
            target=self.merges[pair]
            ids=merge(ids,pair,target)
        
        return ids

    def encode_ordinary_text(self,text):
        tokens=make_tokens(self.compiled_pattern,text)
        ids=[]
        for chunk_token in tokens:
            ids.extend(self.encode_chunk(chunk_token))
        return ids
        


    

