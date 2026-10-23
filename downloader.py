import urllib.request
import pandas
from cleaner import clean, normalize_spaces

def download(id):
    catalog = pandas.read_csv('pg_catalog.csv')
    #data store every informations on book{"Text#"} == id
    data = catalog[catalog["Text#"] == id].iloc[0]

    urllib.request.urlretrieve(
        f"https://www.gutenberg.org/ebooks/{id}.txt.utf-8",
        f"books/{id}"
    )

    with open(f"books/{id}", "r") as file:
        content = file.readlines()

    content = normalize_spaces(clean(content))

    with open(f"books/{id}", "w") as file:
        file.writelines(content)
        
    #for --info
    return data