from string import punctuation
import re, itertools

smileys = """:D :-D :) :-) :-E >-) :( :-( :-< :P :-O :-* :-@ :'( :-$ :-\ :-# (((H))) :-X `:-) :^) :-& E-:-) <:-) :-> (-}{-) :-Q $_$ @@ :-! :-D :*) :@ :-@ :-0 :-----) %-( :-.) :-($) (:I     |-O :@) <(-_-)> d[-_-]b ~:0 -@--@- \VVV/ \%%%/ :-# :'-) {:-) ;) ;-) O:-) O*-) |-O (:-D @>--;-- @-}--- =^.^= O.o \_/) (o.o) (___)0 ~( 8^(I)"""

regex = {}
regex['word'] = re.compile( "([A-Za-z0-9\-_]+)" );
regex['smileys'] = re.compile( "|".join( map(re.escape,smileys.split()) ) )
regex['mentions'] = re.compile( r"(@\w+)" )
regex['tags'] = re.compile( r"(#[A-Za-z0-9]+)" )
regex['email'] = re.compile( r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)" )
regex['url'] = re.compile( "(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)" )
regex['ellipses'] = re.compile( r"...$" )
regex['punct'] = re.compile( "|".join( [re.escape(c) for c in punctuation] ) )
regexLst = [ regex['word'], regex['smileys'], regex['mentions'], regex['tags'], 
				regex['email'], regex['url'], regex['ellipses'], regex['punct'] ]


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
		sentence = "RT @bool: This is@a_tweet@for12Testing#the#tokens#testing:'(with :)with:D#happy#face:PLOL"
		sentence = sentence.strip()
		tokens = []
		while len(sentence)!=0:
			patternFound = False
			for regexp in regexLst:
				m = regexp.match( sentence )
				if m is not None:
					print regexLst.index(regexp)
					patternFound = True
					tokens.append( m.group() );
					sentence = sentence[m.end():].strip()
					break;
			if patternFound == False:
				m = re.match( r"^(.*?) ", sentence )
				if m is None:
					tokens.append( sentence[0] )
					sentence = sentence[1:].strip()
					break;
				else:
					tokens.append( sentence[:m.end()-1] )
					sentence = sentence[m.end():].strip()
		print tokens
		return self.tokens