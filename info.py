from downloader import download

def info(id):
    #get the data from download
    data = download(id)
    
    return {
        "id": str(data["Text#"]),
        "authors": data["Authors"],
        "bookshelves": data["Bookshelves"]
    }