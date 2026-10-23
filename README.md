# Bookworm

Bookworm is a lightweight NLP engine that analyzes books from Project
Gutenberg and generates structured "book cards" — summaries of a book's
vocabulary, themes, characters, locations, and similarity to other books.

## Requirements

- Python 3.12
- pip

## Setup

```bash
# venv configration
python -m venv venv
source venv/bin/activate

# deactivate venv
deactivate

# package installation
pip install -r requirements.txt
python setup.py
```

`setup.py` downloads the NLTK data required for tokenization, POS tagging,
lemmatization, and named entity recognition.

## Usage

Each command operates on a book identified by its Project Gutenberg ID.

```bash
# Download and clean a book
python bookworm.py --download <ID>

# Tokenize the book content
python bookworm.py --tokenize <ID>

# Lexical diversity metrics (vocabulary richness)
python bookworm.py --lexdiv <ID>

# Main topics for each section of the book
python bookworm.py --topics <ID>

# Characters and locations mentioned in the book
python bookworm.py --entities <ID>

# Short summary of the book
python bookworm.py --summarize <ID>

# 5 books similar to the given book
python bookworm.py --similar <ID>

# Full book card (compiles all the above)
python bookworm.py --card <ID>
```

## Project structure

```
bookworm/
├── bookworm.py        # CLI entry point
├── cleaner.py         # text cleaning (header/footer removal, spacing)
├── downloader.py       # book download from Project Gutenberg
├── tokenizer.py        # tokenization, stopwords, punctuation filtering
├── lexdiv.py            # lexical diversity metrics
├── topics.py            # topic modeling (LDA)
├── entities.py          # named entity recognition
├── summarize.py         # text summarization
├── similar.py            # book similarity (TF-IDF + cosine similarity)
├── card.py               # book card aggregation
├── info.py               # book metadata from the catalog
├── manager.py            # cache read/write
├── diagrams/             # pipeline diagrams
├── cache/                # cached results (gitignored)
├── books/                # downloaded books (gitignored)
├── pg_catalog.csv        # Project Gutenberg catalog
└── requirements.txt
```

## Notes

- Heavy operations (topic modeling, summarization, similarity) are cached
  in the `cache/` folder to avoid recomputation.
- The `--similar` option relies on a fixed collection of 21 books from
  Project Gutenberg, defined in `download_books.py`.