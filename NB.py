import re

from Vector import Vector
from numpy import log

from stopwords import stopwords
new_stop_words = set()
for word in stopwords:
    if "'" in word:
        new_stop_words.add(word.replace("'",""))
stopwords = stopwords.union(new_stop_words)


def sanitize(text):
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

class NB(object):
    
    def __init__(self):
        self.classes = ["+", "-"]
        self.features = set()
        feature_list = open("features.txt")
        for line in feature_list:
            self.features.add(line.strip().lower())
        self.cpds = {"+": Vector(),
                     "-": Vector()}
        for vector in self.cpds.values():
            vector.default = 1
        self.priors = {"+": 0.6, "-": 0.4}

    def learn_cpd(self, cls, tweets):
        counter = self.cpds[cls]
        total = 0.0
        for tweet in tweets:
            total += 1
            tweet = sanitize(tweet)
            for word in tweet:
                if word in self.features:
                    counter[word] += 1

        for key in counter:
            counter[key] = counter[key] / total
        
        counter.default = 1/total
        print "Total %s tweets: %s" % (cls, total)

    def posterior(self, cls, sanitized_tweet):
        p = log(self.priors[cls])
        cpd = self.cpds[cls]
        for feature in self.features:
            if feature in sanitized_tweet:
                p += log(cpd[feature])
            else:
                p += log(1 - cpd[feature])
        return p


    def classify(self, tweet):
        tweet = sanitize(tweet)
        posteriors = {}
        for cls in self.classes:
            posteriors[cls] = self.posterior(cls, tweet)
        pos = posteriors["+"]
        neg = posteriors["-"]

        if pos > log(2) + neg:
            return "+"
        elif neg > log(2) + pos:
            return "-"
        else:
            return "~"

if __name__ == "__main__":
    n = NB()
    n.learn_cpd("+", open("positive2.txt"))
    n.learn_cpd("-", open("negative2.txt"))
    w = 0
    t = 0
    for tweet in open("positive2.txt"):
        t += 1.0
        if "+" != n.classify(tweet):
            w += 1.0
    print w/t

