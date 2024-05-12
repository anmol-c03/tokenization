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
class special_tokenizer:
    def __init__(self) -> None:
        self.special_tokens={}
        self.inverse_special_tokens={}
        self.vocab={}
        self.merges={}

    def train(self,text) :
        text_chunk=re.findall(gpt2pat, text)
        tokens=[list(chunk.encode('utf-8')) for chunk in text_chunk]
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
    
    