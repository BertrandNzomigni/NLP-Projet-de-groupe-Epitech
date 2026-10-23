from tokenizer import tokenize
from manager import cache_writer

def lexdiv(fileName, tokenize_mode):
    #get the tokens list
    tokens = tokenize(fileName, tokenize_mode)
    #lower case all the words
    tokens = [w.lower() for w in tokens]
    #total number of word tokens
    tok = len(tokens)
    
    #sort tokens list (remove duplicates)
    tokens_sorted = list(dict.fromkeys(tokens))
    #number of unique word tokens
    typ = len(tokens_sorted)
    
    #tokens_occured_once stock numbers of word from tokens_sorted occurring only once in tokens list
    tokens_occured_once = []
    for word in tokens_sorted:
        if tokens.count(word) == 1:
            tokens_occured_once.append(word)
    #number of word tokens occurring only once
    hap = len(tokens_occured_once)
    
    #Type-Token Ratio, the closer it is to 1, the more varied the vocabulary.
    ttr = typ/tok
    
    #mean tokens sorted length
    total_chars = 0
    for word in tokens_sorted:
        total_chars += len(word)
    mwl = total_chars/len(tokens_sorted)
    
    #ttr reverse, how much time each unique token is repeated
    mwf = tok/typ
    
    #store the metrics in cache
    metrics = {
        "tok": tok,
        "typ": typ,
        "hap": hap,
        "ttr": ttr,
        "mwl": mwl,
        "mwf": mwf
    }
    cache_writer(f"lexdiv/lexdiv_{fileName}", metrics)
    
    return metrics
    