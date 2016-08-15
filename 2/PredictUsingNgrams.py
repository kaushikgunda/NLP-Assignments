import tweetTokenizer as t
import codecs

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
	fileIn = codecs.open('The Adventures of Sherlock Holmes.txt')
	fileOut = codecs.open('The Adventures of Sherlock Holmes.tokens', "w+")
	tokensList = [ "<s>" ]
	sentences = []
	for line in fileIn:
		o.tokenize( line )
		tokens = o.getTokens();
		o.clearTokens()
		if len(tokens) == 0:
			tokensList.extend( ["</s>"] )
			if len(tokensList) > 2:
				sentences.append( tokensList )
			tokensList = [ "<s>" ]
		else:
			tokensList.extend( tokens )
			if '.' in tokensList:
				indx = tokensList.index( '.' )
				tmp = tokensList[:indx+1]
				tmp.append( ["</s>"] )
				if len(tmp) > 2:
					sentences.append( tmp )
				tmp = ["<s>"]
				tmp.extend( tokensList[indx+1:] )
				tokensList = tmp;
	if len(sentences) != 0:
		tokensList.append( ["</s>"] )
		if len(tokensList) == 2:
			sentences.append( tokensList )

	for sentence in sentences:
		tmp = ""
		for word in sentence[1:-1]:
			tmp += word + " "
		fileOut.write( tmp.strip() )
		fileOut.write( "\n" )

	fileOut.close()


def getProbability( word, n ):
	""" Get the probability of the word	to appear at the end of the line, using """
	probability = 1.0


if __name__ == "__main__":
	doTokenization();
	word = "us"
	print getProbability( word, 2 )