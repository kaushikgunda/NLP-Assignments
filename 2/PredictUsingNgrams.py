import tweetTokenizer as t
import codecs, re, operator, sys
from collections import OrderedDict
from matplotlib import pyplot as ppl

def formatTheSentences():
	fileIn = codecs.open('The Adventures of Sherlock Holmes.txt')
	fileOut = codecs.open('The Adventures of Sherlock Holmes.formated', "w+")
	fileInContent = ""
	for line in fileIn:
		if len(line.strip()) !=0:
			fileInContent += line
	fileInContent = "<s>" + fileInContent
		


def doTokenization():
	o = t.Tokenizer( ignoreList= [ 'email', 'url', 'ellipses', 'punct', 'unicodeEmoji' ] )
	fileIn = codecs.open('twitter_small.dump', encoding='utf-8')
	fileOut = open('twitter.tokens', "w+")
	tokensList = []
	lines = ""
	for line in fileIn:
		o.tokenize(line.strip())
		temp = o.getTokens();
		o.clearTokens();
		if len(temp) != 0:
			tokens = [ "<s>" ]
			tokens.extend( temp )
			tokens.extend( ["</s>"] )
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
			key = tuple( line[i:i+n+1] )
			ngrams[ key ] = (ngrams[key]+1) if key in ngrams else 1

	sortedByValues = OrderedDict(sorted(ngrams.items(), key=lambda x: x[1], reverse=True))

	if len(sortedByValues) != 0:
		fileOut = open('twitter.ngrams', "w+")
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
		if ngram[i] != word[j]:
			return False;
		i-=1;
		j-=1;
		n-=1;
	return True
	

ngrams = {}

def getProbabiliy( word, n ):
	countNum, countDen = 0,0;
	for ngram in ngrams[n].keys():
		countNum += ( ngrams[n][ngram] if wordIsFoundInNgram( ngram, n, word ) else 0 )
	if n-1 == 0:
		countDen = sum( [ ngrams[1][x] for x in ngrams[1].keys() ] )
		return ( 1.0 * (countNum+1) / (countDen) )
	else:
		for ngram in ngrams[n-1].keys():
			countDen += ( ngrams[n-1][ngram] if wordIsFoundInNgram( ngram, n, word[:-1] ) else 0 )
	# print countNum, " : ", countDen, " :: ", len(ngrams[n-1]), " :: ", len(ngrams[n]), " :: "
	return ( 1.0 * (countNum+1) / (countDen+len(ngrams[n-1])) )



if __name__ == "__main__":
	i = 1
	print "{0}. Tokenizing".format(i);	i+=1
	tokensList = doTokenization();

	word = raw_input("Enter the word for finding the probability to be at the end of a sentence:\n");
	word = word.decode('utf-8').strip()
	o = t.Tokenizer( ignoreList= [ 'email', 'url', 'ellipses', 'punct', 'unicodeEmoji' ] )
	o.tokenize(word)
	word = o.getTokens()
	o.clearTokens()
	word.extend( ["</s>"] );
	print word


	ngrams[1] = generateNGrams( tokensList, n=1 )
	for x in xrange(2,7):
		ngrams[x] = generateNGrams( tokensList, n=x )

	y = []
	for x in xrange(1,7):
		print "{0}. Generating \'{1}-grams\'".format(i,x);	i+=1
		probability = getProbabiliy( word=word, n=x );
		y.append( probability )
		print "   probability: ", str(probability)

	ppl.plot( range(len(y)), y )
	ppl.show()