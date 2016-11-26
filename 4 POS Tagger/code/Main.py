from nltk.corpus import brown
from nltk.data import load
from collections import OrderedDict
import math
import tweetTokenizer


# brown.words()
# brown.tagged_words()
# brown.tagged_sents()

# Add start and end tags to each sentence in the Brown-data
print "1. Adding Start and End tags to the sentences..."
tagged_sents = [ [('<s>','OTH')] + [ (word.lower(),tag) for (word,tag) in x] + [('</s>','OTH')] for x in brown.tagged_sents() ]
train_sent = tagged_sents[100:]
test_sent = [ [word.lower() for word in x] for x in brown.sents()[:100] ]

tagdict = load('help/tagsets/upenn_tagset.pickle')
tagset = tagdict.keys()
tagsCount = len(tagset)
wordCount = len( brown.words() )
posBigramCount = {}
posUnigramCount = {}
wordPosBigramCount = {}

# Calculate the Counts 
print "2. Computing the counts..."
for tagged_sent in tagged_sents:
	for i in xrange( 1, len(tagged_sent) ):
		posBigram = ( tagged_sent[i-1][1], tagged_sent[i][1] )
		prevPos = tagged_sent[i-1][1]
		posBigramCount[posBigram] =  1 + ( posBigramCount[posBigram] if posBigram in posBigramCount else 0 )
		posUnigramCount[ prevPos ] = 1 + ( posUnigramCount[prevPos] if prevPos in posUnigramCount else 0 )
		wordPos = tagged_sent[i]
		wordPosBigramCount[ wordPos ] = 1 + ( wordPosBigramCount[ wordPos ] if wordPos in wordPosBigramCount else 0 )

# Compute the P( Ti | Ti-1 )
print "3. Computing the Bigram Probability for the tags..."
posBigramProb = {}
for posBigram in posBigramCount:
	posBigramProb[ posBigram ] = 1.0 * (posBigramCount[posBigram]+1) / (posUnigramCount[posBigram[0]]+tagsCount)
	posBigramProb[ posBigram ] = -1 * math.log( posBigramProb[posBigram] )

# Compute the P( Wi | Ti )
print "3. Computing the Bigram Probability for a word, given tag..."
wordPosBigramProb = {}
for wordPosBigram in wordPosBigramCount:
	wordPosBigramProb[ wordPosBigram ] = 1.0 * (wordPosBigramCount[wordPosBigram]+1) / (posUnigramCount[wordPosBigram[1]]+wordCount);
	wordPosBigramProb[ wordPosBigram ] = -1 * math.log( wordPosBigramProb[wordPosBigram] )

transProbForNewToken = -1 * math.log( 1.0 / (posUnigramCount[posBigram[0]]+tagsCount) )
emissionProbForNewToken = -1 * math.log( 1.0 / (posUnigramCount[wordPosBigram[1]]+wordCount) )


def getPairwiseProbabilities( prevToken, curToken):
	prevTags = ["OTH"] if prevToken=="<s>" else tagset
	curTags = ["OTH"] if curToken=="</s>" else tagset
	probs = {}
	for prevTagIndx in xrange(len(prevTags)):
		prevTag = prevTags[prevTagIndx]
		for curTagIndx in xrange(len(curTags)):
			curTag = curTags[curTagIndx]
			tagGivenTag = posBigramProb[(prevTag,curTag)] if (prevTag,curTag) in posBigramProb else transProbForNewToken
			tagGivenWord = wordPosBigramProb[(prevToken,curToken)] if (prevToken,curToken) in wordPosBigramProb else emissionProbForNewToken
			probs[ (prevTag,curTag) ] = tagGivenTag + tagGivenWord
	probs = OrderedDict( sorted(probs.items(), key=lambda x:x[1], reverse=True) )
	return probs


# Evaluate the pair-wise probabilites
print "4. Testing.."
posTagProbabltyBySent = []
for sentIndex in xrange(100):
	sent = test_sent[sentIndex]
	print "Sentence-{0}".format( sentIndex )
	i += 1
	tokens = ["<s>"] + sent + ["</s>"]
	tagToWordProbab = []
	for tokenIndex in xrange(1,len(tokens)):
		prevToken = tokens[tokenIndex-1]
		curToken = tokens[tokenIndex]
		tagToWordProbab += [ getPairwiseProbabilities( prevToken, curToken ) ]
	posTagProbabltyBySent += [ tagToWordProbab ]



# Track the max-probabilities from right-to-left
print "4. Generating tags..."
res = []
for i in xrange(len(posTagProbabltyBySent)):
	print "Sentence-{0}".format(i)
	tagToWordProbabInSent = posTagProbabltyBySent[i]
	lastWordProbs = tagToWordProbabInSent[-1]
	tagForLastWord = lastWordProbs.keys()[0][0]
	resTagSents = [ tagForLastWord ]
	for indx in xrange(len(tagToWordProbabInSent)):
		tagProbs = tagToWordProbabInSent[indx]
		for item in tagProbs:
			key = item[0]
			if key[-1]==resTagSents[-1]:
				resTagSents += key[0]
				break;
	resTagSents = reversed(resTagSents)
	res += resTagSents
	posTagProbabltyBySent = posTagProbabltyBySent[1:]
	i+=1