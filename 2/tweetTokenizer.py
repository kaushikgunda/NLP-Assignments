# -*- coding: utf-8 -*-

from string import punctuation
import re, itertools
import unicodedata

smileys = """<3 :D :-D :) :-) :P :-P :-E >-) :( :-( :-< :P :-O :-* :-@ :'( :-$ :-\ :-# (((H))) :-X `:-) :^) :-& E-:-) <:-) :-> (-}{-) :-Q $_$ @@ :-! :-D :*) :@ :-@ :-0 :-----) %-( :-.) :-($) (:I     |-O :@) <(-_-)> d[-_-]b ~:0 -@--@- \VVV/ \%%%/ :-# :'-) {:-) ;) ;-) O:-) O*-) |-O (:-D @>--;-- @-}--- =^.^= O.o \_/) (o.o) (___)0 ~( 8^(I)"""

regex = {}
regex['word'] = re.compile( u"([A-Za-z0-9\-_\,]+(\'[A-Za-z][A-Za-z]?)?)\'?" );
regex['smileys'] = re.compile( "|".join( map(re.escape,smileys.split()) ) )
regex['abbre'] = re.compile( "([A-Z](\.[A-Z])+)" );
regex['unicodeEmoji'] = re.compile(u'(['
								    u'\U0001F300-\U0001F64F'
								    u'\U0001F680-\U0001F6FF'
								    u'\u2600-\u26FF\u2700-\u27BF])', 
								    re.UNICODE)
regex['mentions'] = re.compile( r"(@\w+:?)" )
regex['tags'] = re.compile( r"(#[A-Za-z0-9]+)" )
regex['email'] = re.compile( r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)?)" )
regex['url'] = re.compile( "(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)" )
regex['ellipses'] = re.compile( r"\.\.\.$" )
regex['punct'] = re.compile( "|".join( [re.escape(c) for c in punctuation] ) )
regexLst = [ 'email', 'url', 'abbre', 'word', 
				'smileys', 'unicodeEmoji',
				'mentions', 'tags', 'ellipses', 
				'punct' ]
unicodePunctPattern = { 0x2018:0x27, 0x2019:0x27, 0x201C:0x22, 0x201D:0x22 }


class Tokenizer(object):

	def __init__(self, ignoreList):
		super(Tokenizer, self).__init__()
		self.tokens = []
		self.ignoreList = ignoreList

	def tokenize( self, text ):
		self.text = text
		lines = self.text.split("\n")
		for line in lines:
			self.__tokenizeWord( line );
	
	def getTokens( self ):
		return self.tokens;

	def clearTokens( self ):
		self.tokens = []

	def __tokenizeWord( self, sentence ):
		sentence = sentence.strip()
		sentence = sentence.translate(unicodePunctPattern)
		while len(sentence)!=0:
			patternFound = False
			for regexpKey in regexLst:
				regexp = regex[regexpKey]
				m = regexp.match( sentence )
				if m is not None:
					patternFound = True
					if regexpKey not in self.ignoreList:
						self.tokens.append( m.group() );
					sentence = sentence[m.end():].strip()
					break;
			if patternFound == False:
				m = re.match( r"^(.*?) ", sentence )
				if m is None:
					self.tokens.append( sentence[0] )
					sentence = sentence[1:].strip()
					break;
				else:
					self.tokens.append( sentence[:m.end()-1] )
					sentence = sentence[m.end():].strip()