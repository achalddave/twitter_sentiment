import sys
import urllib
import json
import HTMLParser

URL = "http://search.twitter.com/search.json?q=%s&rpp=100&lang=en"
PARSER = HTMLParser.HTMLParser()

def get_tweets(keyword):
    req = URL % urllib.quote(keyword)
    print "Loading %s" % req
    res = urllib.urlopen(req)
    parsed = json.load(res)
    texts = get_texts(parsed)
    return texts

def get_texts(parsed):
    return [PARSER.unescape(p["text"]).encode("utf8").strip() for p in parsed["results"]]

if __name__ == "__main__":
    if len(sys.argv) < 1:
        print "no arg"
    else:
        texts = get_tweets(" ".join(sys.argv[1:]))
        tweets = open("tweets.txt", "a")
        for text in texts:
            tweets.write(text)
            tweets.write("\n")
        tweets.close()

"""
curl --data-binary @tweets.txt "http://twittersentiment.appspot.com/api/bulkClassify" > sentiment.txt
"""
