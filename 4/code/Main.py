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

posBigramCount = {}
posUnigramCount = {}
wordPosBigramCount = {}
wordCount = {}

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
	posBigramProb[ posBigram ] = 1.0 * posBigramCount[posBigram] / posUnigramCount[posBigram[0]];
	posBigramProb[ posBigram ] = -1 * math.log( posBigramProb[posBigram] )

# Compute the P( Wi | Ti )
print "3. Computing the Bigram Probability for a word, given tag..."
wordPosBigramProb = {}
for wordPosBigram in wordPosBigramCount:
	wordPosBigramProb[ wordPosBigram ] = 1.0 * wordPosBigramCount[wordPosBigram] / posUnigramCount[wordPosBigram[1]];
	wordPosBigramProb[ wordPosBigram ] = -1 * math.log( wordPosBigramProb[wordPosBigram] )


# Read the input from the user and Tokenize it
sent = raw_input("Enter a sentence for POS tagging: ")
print "4. Tokenizing..."
sent = sent.decode('utf8')
tokenizer = tweetTokenizer.Tokenizer()
tokenizer.tokenize(sent)
tokens = ["<s>"] + tokenizer.getTokens() + ["</s>"]
tokenizer.clearTokens()


tagdict = load('help/tagsets/upenn_tagset.pickle')
tagset = tagdict.keys()
posSequenceProbDict = { }
for tokenIndex in xrange(1, len(tokens)):
	for 
for()