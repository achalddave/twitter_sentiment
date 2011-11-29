from Vector import Vector
import string
import re
import numpy as np

from stopwords import stopwords
new_stop_words = set()
for word in stopwords:
    if "'" in word:
        new_stop_words.add(word.replace("'",""))
stopwords = stopwords.union(new_stop_words)

def sanitize(line):
    text = line.split(",", 1)[1][1:][:-1]
    words = text.split()
    words = [word for word in words if "@" not in word]
    words = [word for word in words if "#" not in word] 
    words = [word.lower() for word in words if not word.startswith("http")] 
    words = [word.lower() for word in words if word not in stopwords]
    text = " ".join(words)
    words = re.findall("\w+", text)
    words.extend(re.findall("['\-/()=:;]['\-/()=:;]+", text))
    words = {word for word in words if 
                        len(word) > 1 
                        and word.lower() != "rt"}
    return words


def info_bernuilly(p):
    return -p*np.log(p)-(1-p)*np.log(1-p)


if __name__ == "__main__":

    positives = Vector()
    negatives = Vector()
    both = Vector()

    documents = 0.0
    p = 0.0
    n = 0.0

    f = open("positive.txt")
    for line in f:
        for word in sanitize(line):
            positives[word] += 1
            both[word] += 1
            documents += 1
            p += 1
    f.close()

    f = open("negative.txt")
    for line in f:
        for word in sanitize(line):
            negatives[word] += 1
            both[word] += 1
            documents += 1
            n += 1
    f.close()

    features = []
    for word in both:
        p_both = both[word] / documents
        p_pos = positives[word] / p or 0.001/p
        p_neg = negatives[word] / n or 0.001/n
        gain = info_bernuilly(p_both) - p/documents * info_bernuilly(p_pos) - n/documents * info_bernuilly(p_neg)
        features.append((word, gain))

    for word in [w[0] for w in sorted(features, key=lambda x: -x[1])[:250]]:
        print word
