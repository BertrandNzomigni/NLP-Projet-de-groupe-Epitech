import os
import argparse
from manager import cache_reader, cache_writer
from downloader import download
from tokenizer import tokenize
from lexdiv import lexdiv
from topics import topics
from entities import entity_recognition
from summarize import summarize
from similar import similarity
from card import card

# create the parser
parser = argparse.ArgumentParser()

#ARGUMENTS
# positional argument
parser.add_argument("id", type=int, help="book id")
# optional arguments
parser.add_argument("--download", action="store_true")
parser.add_argument("--tokenize", action="store_true")
parser.add_argument("--lexdiv", action="store_true")
parser.add_argument("--topics", action="store_true")
parser.add_argument("--entities", action="store_true")
parser.add_argument("--summarize", action="store_true")
parser.add_argument("--similar", action="store_true")
parser.add_argument("--card", action="store_true")

#parse command line
args = parser.parse_args()


#generic helper to avoid repeating the same cache-check pattern for every option
def run_with_cache(cache_path, compute_func, formatter=None):
    if os.path.exists(f"cache/{cache_path}.json"):
        result = cache_reader(cache_path)
    else:
        result = compute_func()
        cache_writer(cache_path, result)
    return formatter(result) if formatter else result


#nomenclature: only one action runs at a time, using elif keeps behavior
#unchanged even if multiple flags are passed together (collision)
try:
    if args.download:
        download(args.id)
        print("File downloaded successfully")

    elif args.tokenize:
        print(run_with_cache(
            f"tokenize/tokenize_{args.id}",
            lambda: tokenize(args.id, False)
        ))

    elif args.lexdiv:
        print(run_with_cache(
            f"lexdiv/lexdiv_{args.id}",
            lambda: lexdiv(args.id, True)
        ))

    elif args.entities:
        print(run_with_cache(
            f"entities/entities_{args.id}",
            lambda: entity_recognition(args.id)
        ))

    elif args.summarize:
        print(run_with_cache(
            f"summaries/summary_{args.id}",
            lambda: summarize(args.id),
            formatter="\n".join
        ))

    elif args.topics:
        print(run_with_cache(
            f"topics/topics_{args.id}",
            lambda: topics(args.id)
        ))

    elif args.similar:
        print(run_with_cache(
            f"similarity/similar_{args.id}",
            lambda: similarity(args.id)
        ))

    elif args.card:
        print(run_with_cache(
            f"card/card_{args.id}",
            lambda: card(args.id)
        ))

    else:
        print("No option provided. Use --download, --tokenize, --lexdiv, "
              "--topics, --entities, --summarize, --similar, or --card.")

except FileNotFoundError:
    print(f"Error: book {args.id} not found. Did you run --download {args.id} first?")
except Exception as e:
    print(f"Error: {e}")