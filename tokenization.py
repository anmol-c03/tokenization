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