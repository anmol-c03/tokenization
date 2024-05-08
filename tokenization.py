from unicodedata import category

def get_stats(ids):
    counts={}
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


class basic_tokenizer:
    def __init__(self):
        self.merges={}
        self.vocab=self.build_vocab(self.merges)

    def build_vocab(self):
        vocab={index:bytes([index]) for index in range(256)}
        for pair,index in self.merges.items():
            p0,p1=pair
            vocab[index]=vocab[p0]+vocab[p1]
    
    def train(self,tokens,vocab_size):
        assert vocab_size>=256
        num_iters=vocab_size-256
        target=255
        ids=list(tokens)
        merges={}
        for i in range(num_iters):
            if len(ids)<2:
                break
            stats=get_stats(ids)
            pair=max(stats,key=stats.get)
            target=target+1
            ids=merge(ids,pair,target)
            merges[pair]=target

        self.merges=merges
        