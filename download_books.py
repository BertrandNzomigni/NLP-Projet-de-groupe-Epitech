from downloader import download

BOOK_IDS = [11,12,16,55,113,120,236,108,834,1661,61262,69087,70114,35,36,84,159,164,345,68283]

for book_id in BOOK_IDS:
    download(book_id)