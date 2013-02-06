import sys
sys.path.insert(0, 'twitter/')

import twitter

api = twitter.Api(consumer_key="ElptdK9AGjxOBuORbiuTQ",
    consumer_secret="iufJBk1qhX84VVeCeeqeOJrVgDkqmtiVobNTpMKUA",
    access_token_key="370357185-yFfM8KRTOLuQJqfaURThsTN53clQK5oxAyTbvmb0",
    access_token_secret="1nSEOq2a6STHJm4gIVObMI0bkoL6cG8zH7n0qQ2bKc")

def get_tweets():
    statuses = api.GetSearch("a")
    #statuses = api.GetPublicTimeline()
    text = []
    for s in statuses:
        text.append(s.text)
        #print s.GetText()
    return text

if __name__ == "__main__":
    get_tweets()
