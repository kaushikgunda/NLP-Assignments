from nltk.corpus import brown
from nltk.data import load
import math
import tweetTokenizer

# brown.words()
# brown.tagged_words()
# brown.tagged_sents()

# Add start and end tags to each sentence in the Brown-data
print "1. Adding Start and End tags to the sentences..."
tagged_sents = [ [('<s>','OTH')] + x + [('</s>','OTH')] for x in brown.tagged_sents() ]

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


# Read the input from the user and Tokenize it
sent = raw_input("Enter a sentence for POS tagging: ")
print "4. Tokenizing..."
sent = sent.decode('utf8')
tokenizer = tweetTokenizer.Tokenizer()
tokenizer.tokenize(sent)
tokens = ["<s>"] + tokenizer.getTokens() + ["</s>"]
tokenizer.clearTokens()

transProbForNewToken = -1 * math.log( 1.0 / (posUnigramCount[posBigram[0]]+tagsCount) )
emissionProbForNewToken = -1 * math.log( 1.0 / (posUnigramCount[wordPosBigram[1]]+wordCount) )

posSequenceProbDict = { }
token = tokens[1]
prevToken = tokens[0]
for tagIndex in xrange( len(tagset) ):
	tag = tagset[tagIndex]
	transProb = posBigramProb[ (prevToken, token) ] if (prevToken,token) in posBigramProb else transProbForNewToken
	emissProb = wordPosBigramProb[ (token,tag) ] if (token,tag) in wordPosBigramProb else emissionProbForNewToken
	posSequenceProbDict[ tagset[tagIndex] ] =  transProb + emissProb

for tokenIndex in xrange(2, len(tokens)):
	print "{0} of {1}".format( tokenIndex, len(tokens) )
	temp = { }
	prevToken = tokens[tokenIndex-1]
	token = tokens[tokenIndex]
	for tagSeq in posSequenceProbDict:
		for currTag in tagset:
			transProb = posBigramProb[ (prevToken, token) ] if (prevToken,token) in posBigramProb \
															else transProbForNewToken
			emissProb = wordPosBigramProb[ (token,currTag) ] if (token,currTag) in wordPosBigramProb \
															else emissionProbForNewToken
			key = tuple( list(tagSeq) + [currTag] )
			temp[ key ] = transProb + emissProb
	posSequenceProbDict = temp;

sortedByValues = OrderedDict(sorted(posSequenceProbDict.items(), key=lambda x: x[1], reverse=True))
print sortedByValues[ sortedByValues.keys()[-1] ]