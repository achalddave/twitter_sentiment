import answer
import get_tweets

def refactor_sentiment(result):
	if result == "+":
		return "positive"
	elif result == "-":
		return "negative"
	else:
		return "neutral"

def main():
	n = answer.NB()
	n.learn_cpd("+", open("data/train_pos.txt"))
	n.learn_cpd("-", open("data/train_neg.txt"))
	while True:
		classify_string = raw_input("Type a string to classify!\n If you want to exit, type \"exit\" without the quotes.\n If you want to see it work on live tweets, type \"twitter\" without the quotes.\n")
		if classify_string == "exit":
			break
		elif classify_string == "twitter":
			print ""
			tweets = get_tweets.get_tweets()
			for tweet in tweets:
				result = refactor_sentiment(n.classify(tweet))
				print "The tweet is: ", tweet
				print "\tSentiment is: ", result
			print ""
		else:
			result = refactor_sentiment(n.classify(classify_string))
			print "This string is: ", result, "\n"

if __name__ == "__main__":
	main()
