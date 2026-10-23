from manager import cache_writer
from tokenizer import tokenize_brut
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np


def section_maker(filename):
    #all file tokenize
    content = tokenize_brut(filename)
    
    #set of English stop words
    stopWords = set(stopwords.words('english'))
    #create an object of WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()
    #correpondance between pos_tag tags dans lemmatize pos
    tags_and_pos = {
        ("CC", "CD", "DT", "EX", "FW", "IN", "LS", "MD", "NN", "NNS", "NNP", "NNPS", "PDT", "POS", "PRP", "PRP$", "RP", "SYM", "TO", "UH", "WDT", "WP", "WP$", "WRB"): "n",
        ("VB", "VBD", "VBG", "VBN", "VBP", "VBZ"): "v",
        ("JJ", "JJR", "JJS"): "a",
        ("RB", "RBR", "RBS"): "r"
    }
    #fucntion to return the appropriate lemmatize pos
    def posCheck(value):
        for key in tags_and_pos.keys():
            if value in key:
                return tags_and_pos[key]
        return "n"
    
    words_and_tags = pos_tag(content)
    content_lemmatized = []
    for word in words_and_tags:
        content_lemmatized.append(lemmatizer.lemmatize(word[0], posCheck(word[1])))
    
    #clean tokens = tokens which get lemmatized, punctuation and stopwords filtered
    clean_tokens = []
    for word in content_lemmatized:
        if word not in stopWords:
            clean_tokens.append(word)
            
    #break clean_tokens into chunks of size N
    N = 750
    chunk_clean_tokens = [clean_tokens[i:i + N] for i in range(0, len(clean_tokens), N)]
    
    sections = [" ".join(chunk) for chunk in chunk_clean_tokens]
            
    return sections

def topics(filename):
    #get sections of the book
    sections = section_maker(filename)
    
    #CountVectorizer converts a collection of text documents to a matrix of token counts.
    #vectorizer here is just an instance of CountVectorizer
    vectorizer = CountVectorizer(min_df=2, max_df=0.8)
    
    #fit, to learn the vocabulary
    #it looks at all documents (all sections) and builds a list of all the unique words that exist in the whole.
    #it's basically just a learning step
    #
    #transform, build the matrix
    #it takes each document and counts, for each word of the vocabulary learned, how many times it appears in that specific document.
    X = vectorizer.fit_transform(sections)
    
    #return the vocabulary words, in the same order as the matrix columns
    vocab = vectorizer.get_feature_names_out()
    
    #LatentDirichletAllocation is used to identify topics
    #in LDA, a topic is a group of words that tend to appear together
    #n_components is the number of topics to extract, based on the number of sections
    lda = LatentDirichletAllocation(
        n_components=min(10, max(2, len(sections) // 3)),
        random_state=42
    )
    
    #train the LDA model on the matrix X
    lda.fit(X)
    
    topics_dict = {}
    #lda.components_ is a matrix where each row is a topic,
    #each column is a word from vocab, and each value is the importance
    #of that word for that topic
    for i, line in enumerate(lda.components_, start=1):
        #argsort returns the indices that would sort the array from smallest to largest
        #[-10:] takes the 10 indices with the highest scores
        #[::-1] reverses the order so the most important word comes first
        top_indices = np.argsort(line)[-10:][::-1]
        
        #use the indices to retrieve the actual words from vocab
        top_words = [vocab[index] for index in top_indices]
        
        topics_dict[i] = top_words
    
    cache_writer(f"topics/topics_{filename}", topics_dict)
    return topics_dict