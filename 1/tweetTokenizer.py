from string import punctuation
import re, itertools

smileys = """:D :-D :) :-) :-E >-) :( :-( :-< :P :-O :-* :-@ :'( :-$ :-\ :-# (((H))) :-X `:-) :^) :-& E-:-) <:-) :-> (-}{-) :-Q $_$ @@ :-! :-D :*) :@ :-@ :-0 :-----) %-( :-.) :-($) (:I     |-O :@) <(-_-)> d[-_-]b ~:0 -@--@- \VVV/ \%%%/ :-# :'-) {:-) ;) ;-) O:-) O*-) |-O (:-D @>--;-- @-}--- =^.^= O.o \_/) (o.o) (___)0 ~( 8^(I)"""

regex = {}
regex['smileys'] = "|".join( map(re.escape,smileys.split()) )
regex['mentions'] =  r".*?(@\w+)"
regex['tags'] = r".*?(#[A-Za-z0-9]+)"
regex['email'] = r".*?(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
regex['url'] = ".*?(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)"
regex['ellipses'] = r".*...$"
regex['punct'] = r".*?("+re.escape(punctuation)+")"


class Tokenizer(object):

	def __init__(self):
		super(Tokenizer, self).__init__()
		self.tokens = []

	def tokenize( self, text ):
		self.text = text
		lines = self.text.split("\n")
		for line in lines:
			self.__tokenizeWord( line );
	
	def __getTokens( self ):
		return self.tokens;

	def __tokenizeWord( self, sentence ):
		sentence = self.__removePattern( sentence, regex['smileys'] )
		print sentence
		sentence = [ self.__removePattern( word,regex['mentions'] ) 	for word in sentence ]
		sentence = list(itertools.chain.from_iterable(sentence))
		print sentence
		sentence = [ self.__removePattern( word,regex['tags'] ) 	for word in sentence ]
		sentence = list(itertools.chain.from_iterable(sentence))
		print sentence
		sentence = [ self.__removePattern( word,regex['url'] ) 	for word in sentence ]
		sentence = list(itertools.chain.from_iterable(sentence))
		print 1, sentence
		sentence = [ self.__removePattern( word,regex['punct'] ) 	for word in sentence ]
		sentence = list(itertools.chain.from_iterable(sentence))
		print 2, sentence
		for word in sentence:
			if len( word.strip() ) != 0:
				self.tokens.append( word )		
		return self.tokens

	def __removePattern( self, sentence, pattern ):
		patterns = re.findall( pattern, sentence )
		print patterns, sentence
		self.tokens.extend( patterns )
		return self.__removeElementsFromStr( sentence, patterns )

	def __removeElementsFromStr( self, sentence, patterns):
		words = []
		for pat in patterns:
			l = sentence.split(pat)
			if len(l)!=0:
				words.append( l[0].strip() )
			if len(l)!=1:
				sentence = l[1].strip()
		if len(sentence.strip()) != 0:
			words.append( sentence.strip() )
		return words