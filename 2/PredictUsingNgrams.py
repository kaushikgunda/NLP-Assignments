import tweetTokenizer as t
import codecs, re, operator
from collections import OrderedDict

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
	fileIn = codecs.open('twitter.dump', encoding='utf-8')
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
			break;
		for i in xrange( n, len(line)+1 ):
			key = tuple( line[i-n:i] )
			ngrams[ key ]  = (ngrams[key]+1) if key in ngrams else 1

	sortedByValues = OrderedDict(sorted(ngrams.items(), key=lambda x: x[1], reverse=True))

	fileOut = open('twitter.ngrams', "w+")
	for k,v in sortedByValues.items():
		fileOut.write( str(k) )
		fileOut.write( " : " )
		fileOut.write( str(v) )
		fileOut.write( "\n")

	return ngrams

if __name__ == "__main__":
	tokensList = doTokenization();
	bigrams = generateNGrams( tokensList, n=2 )