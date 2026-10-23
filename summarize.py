from manager import cache_writer
from tokenizer import tokenize
import spacy
import pandas

import sys, io
# pytextrank prints an unwanted debug message on import (likely from icecream)
# temporarily redirect stdout to suppress it
old_stdout = sys.stdout
sys.stdout = io.StringIO()

import pytextrank
# restore normal stdout
sys.stdout = old_stdout

from langdetect import detect

def summarize(id):

    sentences = " ".join(tokenize(id, False)[:100])
    lang = detect(sentences)

    nlp = spacy.load(f"{lang}_core_web_trf")
    nlp.add_pipe("textrank")

    doc = nlp(sentences)

    result = list()
    for element in doc._.textrank.summary(limit_phrases=2, limit_sentences=2):
        result.append(str(element))

    cache_writer(f"summaries/summary_{id}",result)

    return result

    