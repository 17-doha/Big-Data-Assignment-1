import sys
curr_key = None
curr_count = 0
for line in sys.stdin:
    line = line.strip()
    key, count = line.split('\t', 1)
    if curr_key == key:
        curr_count += int(count)
    else:
        if curr_key: print("%s\t%s" % (curr_key, curr_count))
        curr_key, curr_count = key, int(count)
if curr_key: print("%s\t%s" % (curr_key, curr_count))
