
import tweetTokenizer as t
import codecs

o = t.Tokenizer()
fileIn = codecs.open('tweeter.dump', encoding='utf-8')
fileOut = open( "tweeter.tokens", "w" )

for line in fileIn:
	o.tokenize( line )
	tokens = str(o.getTokens()).strip();
	if len(tokens) != 0:
		fileOut.write( str(o.getTokens()) )
		fileOut.write( "\n" )
	o.clearTokens()