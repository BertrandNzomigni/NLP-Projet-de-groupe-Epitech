import json
import os

def cache_writer(filename, content):
    #create directories if necessary
    os.makedirs(f"cache/{os.path.dirname(filename)}", exist_ok=True)
    with open(f"cache/{filename}.json", "w", encoding="utf-8") as file:
        json.dump(content, file, indent=4, skipkeys=True, ensure_ascii=False)

def cache_reader(filename):
    with open(f"cache/{filename}.json", "r", encoding="utf-8") as file:
        return json.load(file)