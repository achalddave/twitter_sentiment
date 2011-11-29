import sys
import re
import numpy as np
from numpy import log

from Vector import Vector


# ==== Cleaning Text ===

# Load stopwords
from stopwords import stopwords
new_stop_words = set()
for word in stopwords:
    if "'" in word:
        new_stop_words.add(word.replace("'",""))
stopwords = stopwords.union(new_stop_words)


# Sanitizer
def sanitize(text):
    """
    clean up:
        1. split a string into a list of words
        2. remove all @ handles
        3. remove all hash tags
        4. remove all liks
        5. remove all stopwords
        6. throw away punctuation, except smiley faces
        7. make the final vector of words a set

    @args:
        text --> a string
    """
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

# ===============


# ==== Feature Selection ====

# Info gain formula
def info_bernuilli(p):
    """
    computes the entropy of a Bernuilli distr

    @args:
        p --> probability p in Bernuilli(p)
    """
    return -p*np.log(p)-(1-p)*np.log(1-p)

# 250 features with highest info gain
def select_features():
    """
    Selects 250 words with the highest information gain. Refer to 
    slides for details
    """

    positives = Vector()
    negatives = Vector()
    both = Vector()

    documents = 0.0
    p = 0.0
    n = 0.0

    f = open("data/train_pos.txt")
    for line in f:
        for word in sanitize(line):
            positives[word] += 1
            both[word] += 1
            documents += 1
            p += 1
    f.close()

    f = open("data/train_neg.txt")
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
        gain = info_bernuilli(p_both) \
                - p/documents * info_bernuilli(p_pos) \
                - n/documents * info_bernuilli(p_neg)
        features.append((word, gain))

    for word in [w[0] for w in sorted(features, key=lambda x: -x[1])[:250]]:
        print word

#==================

class NB(object):
    
    def __init__(self):
        """
        Should do:
            1. define the possible classes
            2. define features
            3. define CPDs
            4. define priors
        """

        self.classes = ["+", "-"]
        self.features = set()
        feature_list = open("data/features.txt")
        for line in feature_list:
            self.features.add(line.strip().lower())
        self.cpds = {"+": Vector(),
                     "-": Vector()}
        for vector in self.cpds.values():
            vector.default = 1
        self.priors = {"+": 0.6, "-": 0.4}

    def learn_cpd(self, cls, tweets):
        """
        Should do:
            learn the CPD for a given class

        @args:
            cls --> a string, "+" or "-" 
            tweets --> an iterable of tweets (a file object, list, etc)
        """
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

    def posterior(self, cls, sanitized_tweet):
        """
        Computes the posterior of a sanitized tweet, P(C|tweet)

        @args:
            cls --> a string, "+" or "-". determines CPD to use
            sanitized_tweet --> a set of words in the tweet
        """
        p = log(self.priors[cls])
        cpd = self.cpds[cls]
        for feature in self.features:
            if feature in sanitized_tweet:
                p += log(cpd[feature])
            else:
                p += log(1 - cpd[feature])
        return p


    def classify(self, tweet):
        """
        Given a text, classify its sentiment. Picks the class with the largest posterior.
      
        However, if we are not confident, ie if not P(C1|tweet) < 2*P(C2|tweet), 
        then we refuse to classify, and return neutral, "~". 

        @args:
            tweet --> a string, text of the tweet
        """
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


def eval_performance(n):
    w = 0
    t = 0
    for tweet in open("data/verify_pos.txt"):
        t += 1.0
        if "+" != n.classify(tweet):
            w += 1.0
    for tweet in open("data/verify_neg.txt"):
        t += 1.0
        if "-" != n.classify(tweet):
            w += 1.0
    for tweet in open("data/verify_neutral.txt"):
        t += 1.0
        if "~" != n.classify(tweet):
            w += 1.0

    print "Error: %s" % (w/t)

def classify_text(n, txt):
    print "That text is: %s" % n.classify(txt)

def main():
    n = NB()
    n.learn_cpd("+", open("data/train_pos.txt"))
    n.learn_cpd("-", open("data/train_neg.txt"))
    if "--verify" in sys.argv:
        eval_performance(n)
    elif "--features" in sys.argv:
        select_features()
    else:
        classify_text(n, sys.argv[1])

if __name__ == "__main__":
    main()
