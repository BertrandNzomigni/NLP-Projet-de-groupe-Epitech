import spacy
from langdetect import detect
from manager import cache_writer, cache_reader
from tokenizer import tokenize

def entity_recognition(id):
    
    sentences = tokenize(id, False)
    
    lang = detect(sentences[0])
    
    result = {"characters":list(),"locations":list()}
    
    nlp = spacy.load(f"{lang}_core_web_trf")
    
    character_set = set()
    location_set = set()
    
    for i in range(0,len(sentences),100):
        doc = nlp(" ".join(sentences[i:i+100]))
        for ent in doc.ents:
            if ent.label_ == "PERSON" and not ent.text in character_set:
                result["characters"].append(ent.text)
                character_set.add(ent.text)
            elif ent.label_ == "GPE" and not ent.text in location_set:
                result["locations"].append(ent.text)
                location_set.add(ent.text)
                
    cache_writer(f"entities/entities_{id}",result)
    
    return result
