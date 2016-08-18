import tweetTokenizer as t
import codecs, re

def formatTheSentences():
	fileIn = codecs.open('The Adventures of Sherlock Holmes.txt')
	fileOut = codecs.open('The Adventures of Sherlock Holmes.formated', "w+")
	fileInContent = ""
	for line in fileIn:
		if len(line.strip()) !=0:
			fileInContent += line
	fileInContent = "<s>" + fileInContent
		


def doTokenization():
	o = t.Tokenizer( )
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


def getProbability( word, n ):
	""" Get the probability of the word	to appear at the end of the line, using """
	fileIn = codecs.open('The Adventures of Sherlock Holmes.tokens')
	p = re.compile( "([A-Za-z0-9]+ +){"+str(n-1)+"}"+word+"$" )
	print p.pattern

	countNum = 0;
	countDen = 0;
	for line in fileIn:
		countDen += 1
		if p.match(line) is not None:
			countNum += 1 

	print countNum
	print countDen
	return 1.0 * countNum / countDen



if __name__ == "__main__":
	doTokenization();
	# word = "us"
	# print getProbability( word, 2 )