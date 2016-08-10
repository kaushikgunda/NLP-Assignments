from string import punctuation
import re
import

smileys = """:D :-D :) :-) :-E >-) :( :-( :-< :P :-O :-* :-@ :'( :-$ :-\ :-# (((H))) :-X `:-) :^) :-& E-:-) <:-) :-> (-}{-) :-Q $_$ @@ :-! :-D :*) :@ :-@ :-0 :-----) %-( :-.) :-($) (:I     |-O :@) <(-_-)> d[-_-]b ~:0 -@--@- \VVV/ \%%%/ :-# :'-) {:-) ;) ;-) O:-) O*-) |-O (:-D @>--;-- @-}--- =^.^= O.o \_/) (o.o) (___)0 ~( 8^(I)"""

regex = {}
regex['smileys'] = "|".join( map(re.escape,smileys.split()) )
regex['mentions'] =  r".*?(@\w+)"
regex['tags'] = r".*(#[^ ]+)"
regex['email'] = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
regex['url'] = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
regex['ellipses'] = r"...$"
regex['punct'] = punctuation


class Tokenizer(object):
	"""docstring for Tokenizer"""

	def __init__(self, text):
		super(Tokenizer, self).__init__()
		self.text = text
		self.tokens = []

	def tokenize( self, text ):
		lines = text.split("\n")
		for line in lines:
			self.tokens.append( tokenizeWord( line ) );
		return self.tokens;

	def tokenizeWord( self, sentence ):
		sentence = removePattern( sentence, regex['smileys'] )
		sentence = [ removeMentions( word,regex['mentions'] ) 	for word in sentence ]
		sentence = [ removeTag( word,regex['tags'] ) 	for word in sentence ]
		sentence = [ removeUrl( word,regex['url'] ) 	for word in sentence ]

	def removePattern( self, sentence, pattern ):
		patterns = re.findall( pattern, sentence )
		self.tokens.extend( patterns )
		return removeElementsFromStr( sentence, patterns )

	def removeElementsFromStr( self, sentence, emoticons):
		words = []
		for em in emoticons:
			l = sentence.split(em)
			if len(l)!=0:
				words.append( l[0].strip() )
			if len(l)!=1:
				sentence = l[1].strip()
		if len(sentence.strip()) != 0:
			words.append( sentence.strip() )
		return words