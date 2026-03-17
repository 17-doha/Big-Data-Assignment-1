import sys
import os
import re
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()
REMOVE_STOPWORDS = os.environ.get('REMOVE_STOPWORDS', 'false').lower() == 'true'

stop_words = set()
if os.path.exists("stopwords.txt"):
    with open("stopwords.txt", "r") as f:
        for line in f:
            stop_words.add(line.strip().lower())

doc_id = os.environ.get('mapreduce_map_input_file', 'unknown_doc')
doc_id = os.path.basename(doc_id)

for line in sys.stdin:
    words = re.findall(r'[a-z0-9]+', line.lower())
    for word in words:
        if REMOVE_STOPWORDS and word in stop_words:
            continue
        if len(word) > 1:
            stemmed = stemmer.stem(word)
            print("%s,%s\t1" % (stemmed, doc_id))
