# -*- coding: utf-8 -*-

import tweetTokenizer as t
o = t.Tokenizer()
s = "Whats' should'ntI do, Boom-boom be happy with lies or be sad with the truth 😔😩🤔"
s = "What should I do, be happy with lies or be s😔d with the truth 😔😩🤔"
s = "This is@a_tweet@for12Testing#the#tokens#testing:'(with :)with:D#happy#face:PLOL"
s = "This is@a_tweet@for12Testing#the#tokens#testing:'(with :)with:D#happy#face:PLOL http://go.co.in/asdaaSD23/43sedf_sad asfda@sdgs.v.in"
s = "Fuck:(!!!!!"
print s
s = s.decode('utf8')
print s
o.tokenize(s)
print o.getTokens();