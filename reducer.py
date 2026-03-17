import sys
curr_word = None
postings = []
for line in sys.stdin:
    try:
        line = line.strip()
        key, count = line.split('\t', 1)
        word, doc = key.split(',', 1)
    except: continue
    if curr_word == word:
        postings.append("%s,%s" % (doc, count))
    else:
        if curr_word: print("%s\t%s" % (curr_word, " ".join(postings)))
        curr_word, postings = word, ["%s,%s" % (doc, count)]
if curr_word: print("%s\t%s" % (curr_word, " ".join(postings)))
