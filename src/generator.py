import sys,argparse, random, math

words = []
startString = "Lesbian ipsum dolor sit amet, "

terminators = ["?", ".", "!"]
intermediates = [";", ":", ",", ",", ","]

frequencyQueue = []

def generateText(wordCount, paragraphCount):
    text = startString
    paragraphSizes = []
    while len(paragraphSizes) != paragraphCount:
        paragraphSizes = divideWordsByParagraph(wordCount, paragraphCount)
    print "paragraph sizes"
    print paragraphSizes
    print "paragraph count"
    print paragraphCount
    for p in range(0, paragraphCount):
        text += generateParagraph(paragraphSizes[p]) + '\n'
    return text


def generateParagraph(paragraphSize):
    paragraph = ""
    print "paragraph size"
    print paragraphSize
    sentenceSizes = divideParagraphIntoSentences(paragraphSize)
    print "sentence sizes "
    print sentenceSizes
    for s in range(0, len(sentenceSizes)):
        paragraph += generateSentence(sentenceSizes[s]) + " "
    return paragraph


def divideParagraphIntoSentences(paragraphWordCount):
    if paragraphWordCount <= 10:
        return [paragraphWordCount]
    numSentences = int(math.ceil(paragraphWordCount/9))
    print "num sentences"
    print numSentences
    sentenceSizes = []
    numShortSentences = int(math.floor(numSentences/3))
    randomShortSentenceIndices = []
    # seed short sentences
    for s in range(0, numShortSentences):
        index = random.randint(0, numSentences-1)
        if index not in randomShortSentenceIndices:
            randomShortSentenceIndices.append(index)
    numLongSentences = int(math.ceil(numSentences/6))
    randomLongSentenceIndices = []
    for l in range(0, numLongSentences):
        index = random.randint(0, numSentences-1)
        if index not in randomShortSentenceIndices and index not in randomLongSentenceIndices:
            randomLongSentenceIndices.append(index)
    remainder = paragraphWordCount
    for n in range(0, numSentences):
        if remainder <= 0:
            return sentenceSizes
        if n == numSentences - 1:
            size = remainder
        elif n in randomShortSentenceIndices:
            size = random.randint(2, 8)
        elif n in randomLongSentenceIndices:
            size = random.randint(11, 15)
        else:
            size = random.randint(9, 12)
        sentenceSizes.append(size)
        remainder -= size
    return sentenceSizes


def generateSentence(sentenceSize):
    sentence = []
    while len(sentence) < sentenceSize:
        word = getWordFilteredByFrequency()
        if len(sentence) == 0:
            word = capitalizeWord(word)
        sentence.append(word)
    sentence = " ".join(punctuate(sentence))
    sentence = terminate(sentence)
    return sentence


def getWordFilteredByFrequency():
    word = getRandomWord()
    queueLength = random.randint(10, 15)
    while len(frequencyQueue) > 0 and word in frequencyQueue:
        word = getRandomWord()
    frequencyQueue.append(word)
    while len(frequencyQueue) > queueLength:
        frequencyQueue.pop(0)
    return word

def getRandomWord():
    return words[random.randint(0,len(words)-1)]


def capitalizeWord(word):
    wordChunks = word.split(" ")
    wordChunks[0] = wordChunks[0].capitalize()
    return " ".join(wordChunks)


def terminate(sentence):
    return sentence + terminators[1]


def punctuate(sentence):
    wordCount = len(sentence)
    if wordCount > 10:
        numIntermediates = random.randint(math.floor(wordCount/20),math.floor(wordCount/10) + 1)
        for x in range(0,numIntermediates):
            intermediateChoiceIndex = random.randint(0,len(intermediates)-1)
            intermediatePlacementIndex = random.randint(math.floor(wordCount * 1/6), math.floor(wordCount * 2/3))
            punctuatedWord = sentence[intermediatePlacementIndex] + intermediates[intermediateChoiceIndex]
            sentence[intermediatePlacementIndex] = punctuatedWord
    return sentence


def divideWordsByParagraph(count, numParas):
    sizes = []
    if count == 0:
        return sizes
    remainder = count
    for p in range(0, numParas):
        if remainder == 0:
            return sizes
        if p == numParas - 1:
            size = remainder
        else:
            if p == 0:
                size = random.randint(math.ceil(remainder/6), math.floor(remainder/4))
            else:
                size = random.randint(math.ceil(remainder/5), math.floor(remainder/3))
        sizes.append(size)
        remainder -= size
    return sizes


def loadWords():
    with open("data/words.txt", "r") as wordFile:
        for line in wordFile:
            words.append(line.strip())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', dest='total_words', help='total number of words')
    parser.add_argument('-p', dest='num_paragraphs', help='number of paragraphs')

    args = parser.parse_args()

    numWords = args.total_words
    numParas = args.num_paragraphs

    totalWordCount = 100
    totalParagraphCount = 1

    if numWords:
        totalWordCount = int(numWords)

    if numParas:
        totalParagraphCount = int(numParas)

    loadWords()

    text = generateText(totalWordCount, totalParagraphCount)

    print text


if __name__ == "__main__":
    main()
