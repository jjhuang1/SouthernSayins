import pykov
#pykov.__version__

phrases = ["Hi my name is max +", "Hi I am +", "Hi I am +", "Hi I am max and you are grace +"]

#T = pykov.Chain({('Hi', 'my'): 0.5, ('Hi', 'I'): 0.5, ('my', 'name'): 1.0, ('name', 'is'): 1.0, ('is', 'max'): 1.0, ('I', 'am'): 1.0, ('am', 'max'): 0.5, ('am', 'grace'): 0.5})
#print(T.walk(100, "Hi", "max"))

# Reads a file
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

# Creates a list with all the pronouns from the file
def construct_phrases_list(phrasesFile):
    phrasesData = readFile(phrasesFile)
    phrasesLines = phrasesData.split("\n")
    return phrasesLines


def buildMarkovChain(phrasesFile):
    phrases = construct_phrases_list(phrasesFile)
    print(phrases)
    wordCount = buildWordCount(phrases)
    connectionsCount = buildConnectionsCount(phrases)

    vector = pykov.Matrix()

    for connection in connectionsCount:
        initialState = connection[0]
        #print("(" + str(connectionsCount[connection]) + ", " + str(wordCount[initialState]) + ")")
        probability = (float(connectionsCount[connection]) / float(wordCount[initialState]))
        #print(probability)
        vector[connection] = probability

    return pykov.Chain(vector)


def buildWordCount(phrases):
    wordCount = dict()
    for phrase in phrases:
        words = phrase.split(" ")
        for index in range(len(words)):
            word = words[index]
            if word not in wordCount:
                wordCount[word] = 0
            wordCount[word] = wordCount.get(word) + 1
    return wordCount

def buildConnectionsCount(phrases):
    connectionsCount = dict()
    for phrase in phrases:
        words = phrase.split(" ")
        for index in range(len(words) - 1):
            currState = (words[index], words[index + 1])
            if currState not in connectionsCount:
                connectionsCount[currState] = 0
            connectionsCount[currState] = connectionsCount.get(currState) + 1
    return connectionsCount

def addApost(newPhrase):
    for word in newPhrase:
        if '\x92' in word:
            word.replace('x92', "'")

#print(buildWordCount(phrases))
#print(buildConnectionsCount(phrases))
#print(buildMarkovChain(phrases))

mc = buildMarkovChain('sayings.txt')
newPhrases = mc.walk(100, '+', '+\r')
newPhrases = newPhrases[1:len(newPhrases)-1]
#newPhrase = addApost(newPhrase)
newPhrases = " ".join(newPhrases)
print(newPhrases.split('+')[0].strip())
