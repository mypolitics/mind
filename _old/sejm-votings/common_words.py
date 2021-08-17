from collections import Counter
import json

with open('db.txt', "r", encoding="utf8") as file:
    lines = file.read().split("\n")
    text = ""

    for line in lines:
        if len(line) == 0 or line[0] != "{":
            continue

        data = json.loads(line)
        text += " " + data["topic"]

    n_print = 300
    text_modified = text\
        .lower()\
        .replace(".", "")\
        .replace(",", "")\
        .replace("(", "")\
        .replace(")", "")
    arr = text_modified.split()
    arr_filtered = filter(lambda x: len(x) > 4, arr)
    word_counter = Counter(arr_filtered)
    for word, count in word_counter.most_common(n_print):
        print(word + "\t" + str(count))