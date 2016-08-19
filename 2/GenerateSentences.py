import tweetTokenizer as t
import pickle as p

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
	ngrams = p.load( open("./ngrams","rb+") )
	bigrams = ngrams[2];
	while True:
		startWord = raw_input( "Enter Start Word: " ).strip().split(" ")
		nForGram = len( startWord ) + 1
		seed = ["<s>"] + startWord
		print seed
		for i in xrange(10):
			maxProbableSentence = seed
			maxProbabilityTillNow = 0.0;
			newWord = seed
			count = 0
			for k in ngrams[1]:
				k = k[0]
				if k == seed[0]:
					continue;
				if count==50:
					break;
				count+=1
				probability = getProbabiliy( seed+[k], nForGram )
				if probability > maxProbabilityTillNow:
					maxProbabilityTillNow = probability
					maxProbableSentence = seed + [k]
					newWord = k
			seed = maxProbableSentence
			print seed
			if newWord=="</s>":
				break;