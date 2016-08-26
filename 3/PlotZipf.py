"""
python PlotZipf.py n director1 director2 director3 ...
n 			-> 	n in n-grams
director1	->	directory containing utf-8 books
"""


import sys, os, codecs, math
import pickle as p
from collections import OrderedDict
from matplotlib import pyplot as ppl

# For importing the Tokenizer.
sys.path.insert( 0, '../2' )

import tweetTokenizer as t
o = t.Tokenizer( ignoreList= [ 'email', 'url', 'ellipses', 'punct', 'unicodeEmoji' ] )


def doTokenization( inpDir ):
	if inpDir[-1] != '/':
		inpDir += '/'
	files = [ inpDir+x for x in os.listdir(inpDir) ]
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

def getProbabiliy( words, n ):
	""" Returns Bigram probability """
	countNum, countDen = 0, 0;
	prob = 1.0
	countOfUnigrams = len( ngrams[1] )

	for x in xrange( 1, n ):
		numStr = tuple( words[ : x+1] )
		countNum = sum( [ ngrams[x][i] if i==numStr else 0 for i in ngrams[x] ] )
		if x-1 == 0:
			countDen = 0
			countN1grams = len(ngrams[1])
		else:
			denomStr = tuple( words[ : x] )
			countDen = sum( [ ngrams[x-1][i] if i==denomStr else 0 for i in ngrams[x-1] ] )
			countN1grams = len(ngrams[x-1])
		prob *= 1.0 * (countNum+1)/(countDen+countN1grams)

	for x in xrange( len(words)-n+1 ):
		numStr = tuple( words[ : x+n-1] )
		countNum = sum( [ ngrams[n][i] if i==numStr else 0 for i in ngrams[n] ] )
		denomStr = tuple( words[ : x+n-2] )
		countDen = sum( [ ngrams[n-1][i] if i==denomStr else 0 for i in ngrams[n-1] ] )
		countN1grams = len(ngrams[n-1])
		prob *= 1.0 * (countNum+1)/(countDen+countN1grams)

	return prob




if __name__ == "__main__":

	n = int(sys.argv[1])
	inpDirs = sys.argv[2:]

	for inpDir in inpDirs:
		print "####### Processing {0} #######".format(inpDir)
		i = 1
		n = 1;
		ngrams = {}
		print "{0}. Tokenizing".format(i);	i+=1
		tokensList = doTokenization( inpDir );

		print "{0}. Generating {1}-grams".format(i,1);	i+=1
		ngrams[1] = generateNGrams( tokensList, n=1 )
		for x in xrange(2,7):
			print "{0}. Generating {1}-grams".format(i,x);	i+=1
			ngrams[x] = generateNGrams( tokensList, n=x )
		print "{0}. Pickling all n-grams".format(i,x);	i+=1

		grams = ngrams[n];

		print "{0}. Computing X-coordinates".format(i);	i+=1
		x = [ math.log(t) for t in xrange( 1, len(grams)+1 ) ]
		print "{0}. Computing Y-coordinates".format(i);	i+=1
		y = [ math.log(grams[t]) for t in grams ]

		ppl.plot( x, y, label=inpDir.split('/')[-2] )

	ppl.title( "Zipf curve using {0}-grams".format(n) )
	ppl.xlabel('log(rank)')
	ppl.ylabel('log(frequency)')
	ppl.legend( loc='upper right' )
	ppl.show();