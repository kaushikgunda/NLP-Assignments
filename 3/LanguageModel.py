import sys, os, codecs
import pickle as p
from collections import OrderedDict

# For importing the Tokenizer.
sys.path.insert( 0, '../2' )

import tweetTokenizer as t


def doTokenization():
	o = t.Tokenizer( ignoreList= [ 'email', 'url', 'ellipses', 'punct', 'unicodeEmoji' ] )
	files = [ "./Books/"+x for x in os.listdir("./Books/") ]
	fileOut = open('books.tokens', "w+")
	for f in files:
		fileIn = codecs.open(f, encoding='utf-8')
		tokensList = []
		lines = ""
		for line in fileIn:
			o.tokenize(line.strip())
			tokens = o.getTokens()
			o.clearTokens();
			if len(tokens) != 0:
				tokensList.append( tokens )
		for line in tokensList:
			fileOut.write( str(line) )
			fileOut.write( "\n" )
	fileOut.close()
	return tokensList



def generateNGrams( tokensList, n ):
	ngrams = {}
	for line in tokensList:
		if len(line) < n:
			continue;
		for i in xrange( 0, len(line)-n+1 ):
			key = tuple( line[i:i+n] )
			ngrams[ key ] = (ngrams[key]+1) if key in ngrams else 1

	sortedByValues = OrderedDict(sorted(ngrams.items(), key=lambda x: x[1], reverse=True))
	if len(sortedByValues) != 0 and n==2:
		fileOut = open('books.ngrams', "w+")
		for k,v in sortedByValues.items():
			fileOut.write( str(k) )
			fileOut.write( " : " )
			fileOut.write( str(v) )
			fileOut.write( "\n")
	return sortedByValues


def wordIsFoundInNgram( ngram, n, word ):
	i, j = len(ngram)-1, len(word)-1
	if i+1<n:
		return False
	while n>0 and j>=0:
		if ngram[i].lower() != word[j].lower():
			return False;
		i-=1;
		j-=1;
		n-=1;
	return True
	

ngrams = {}

def getProbabiliy( words ):
	""" Returns Bigram probability """
	countNum, countDen = 0, 0;
	prob = 1.0
	countOfUnigrams = len( ngrams[1] )

	for x in xrange( len(words) ):
		numStr = ( words[x-1], words[x] ) if x!=0 else ( words[x] )
		denomStr = words[x]
		if x!=0:
			numStr = ( words[x-1], words[x] )
			countNum = sum( [ ngrams[2][i] if i==numStr else 0 for i in ngrams[2] ] )
		else:
			numStr = ( words[x] )
			countNum = sum( [ ngrams[1][i] if i==numStr else 0 for i in ngrams[1] ] )
		
		countDen = sum( [ ngrams[1][i] if i==denomStr else 0 for i in ngrams[1] ] )
		prob *= 1.0 * (countNum+1)/(countDen+countOfUnigrams)

	return prob




if __name__ == "__main__":

	i = 1	
	if len(sys.argv) == 1:
		print "{0}. Tokenizing".format(i);	i+=1
		tokensList = doTokenization();

		print "{0}. Generating {1}-grams".format(i,1);	i+=1
		ngrams[1] = generateNGrams( tokensList, n=1 )
		for x in xrange(2,7):
			print "{0}. Generating {1}-grams".format(i,x);	i+=1
			ngrams[x] = generateNGrams( tokensList, n=x )
		print "{0}. Pickling all n-grams".format(i,x);	i+=1
		p.dump( ngrams, open("./ngrams","wb+") )
	else:
		print "{0}. Loading n-grams".format(i);	i+=1
		ngrams = p.load( open("./ngrams","rb+") )

	while True:
		seedSentence = raw_input( "Enter sentence: " ).strip().split(" ")
		print getProbabiliy( seedSentence )