import answer

def main():
	n = answer.NB()
	n.learn_cpd("+", open("data/train_pos.txt"))
	n.learn_cpd("-", open("data/train_neg.txt"))
	while True:
		classify_string = raw_input("Type a string to classify!  If you want to exit, type \"exit\" without the quotes.\n")
		if classify_string == "exit":
			break
		result = n.classify(classify_string)
		if result == "+":
			result = "positive"
		elif result == "-":
			result = "negative"
		else:
			result = "neutral"
		print "This string is: ", result, "\n"

if __name__ == "__main__":
	main()
