from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
	return render_template("home.html")

@app.route("/generate/", methods=['GET'])
def generate():
	import pykov

	phrasesData = ''
	with open('sayings.txt', "rt") as f:
   		phrasesData = f.read()
	phrasesLines = phrasesData.split("\n")
	phrases = phrasesLines

	wordCount = dict()
	for phrase in phrases:
		words = phrase.split(" ")
		for index in range(len(words)):
			word = words[index]
			if word not in wordCount:
				wordCount[word] = 0
			wordCount[word] = wordCount.get(word) + 1

	connectionsCount = dict()
	for phrase in phrases:
		words = phrase.split(" ")
		for index in range(len(words) - 1):
			currState = (words[index], words[index + 1])
			if currState not in connectionsCount:
				connectionsCount[currState] = 0
			connectionsCount[currState] = connectionsCount.get(currState) + 1

	vector = pykov.Matrix()

	for connection in connectionsCount:
		initialState = connection[0]
		probability = (float(connectionsCount[connection]) / float(wordCount[initialState]))
		vector[connection] = probability
	mc = pykov.Chain(vector)

	newPhrases = mc.walk(100, '+', '+\r')
	newPhrases = newPhrases[1:len(newPhrases)-1]

	newPhrases = " ".join(newPhrases)
	newPhrase = newPhrases.split('+')[0].strip()
	return newPhrase.replace("í", "'")


if __name__ == "__main__":
	app.run(debug=True)