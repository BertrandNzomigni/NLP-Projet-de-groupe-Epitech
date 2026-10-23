import string
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from manager import cache_writer

#fileName is for the file name
#tokenize_mode is a boolean paramater which determine the output, true for word tokenize and false for sent tokenize
#tokenizer take the text, and the tokenize_mode of tokenize looking for, and return the list of tokens appropriate 
def tokenize(fileName, tokenize_mode):
    #set of English stop words
    stopWords = set(stopwords.words('english'))
    
    with open(f"books/{fileName}", encoding="utf-8", errors="replace") as file:
        #parse the csv content
        ebook_content = file.read()

        #let's clean the content and remove any over spaces or newline, before tokenized sentences
        ebook_content = " ".join(ebook_content.split())
        sent_tokenized = sent_tokenize(ebook_content)
        
        #set of special characters which are not punctuation
        extra_punct = {'"', '"', ''', ''', '—', '–', '…', '``', "'", '-', ':', '*', "’", "”", "“", "‘"}
        
        if not tokenize_mode: 
            cache_writer(f"tokenize/tokenize_{fileName}", sent_tokenized)  
            return sent_tokenized
        else:
            word_tokenized = []
            for sentence in sent_tokenized:
                words = word_tokenize(sentence)
                for w in words:
                    if w not in stopWords and w not in string.punctuation and not w.startswith("'") and w not in extra_punct:
                        word_tokenized.append(w)
            cache_writer(f"tokenize/tokenize_{fileName}", word_tokenized)
            return word_tokenized
        
def tokenize_brut(fileName):    
    with open(f"books/{fileName}", encoding="utf-8", errors="replace") as file:
        #parse the csv content
        ebook_content = file.read()

        #let's clean the content and remove any over spaces or newline, before tokenized sentences
        ebook_content = " ".join(ebook_content.split())
        sent_tokenized = sent_tokenize(ebook_content)
        
        #set of special characters which are not punctuation
        extra_punct = {'"', '"', ''', ''', '—', '–', '…', '``', "''", '-', ':', '*', "’", "”", "“", "‘"}
        
        word_tokenized = []
        for sentence in sent_tokenized:
            words = word_tokenize(sentence)
            #lowercase tokens to avoid "king" and "King" to be recognized as different
            words = [w.lower() for w in words]
            for w in words:
                if w not in string.punctuation and not w.startswith("'") and w not in extra_punct:
                    word_tokenized.append(w)
        cache_writer(f"tokenize/brut/tokenize_brut_{fileName}", word_tokenized)
        return word_tokenized