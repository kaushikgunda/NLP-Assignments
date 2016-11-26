# -*- coding: utf-8 -*-

import tweetTokenizer as t
o = t.Tokenizer( ignoreList= [ 'email', 'url', 'ellipses', 'punct', 'unicodeEmoji' ] )
s = "I don’t Whats' should'ntI do, Boom-boom be happy with lies or be sad with the truth 😔😩🤔"
# s = "What should I do, be happy with lies or be s😔d with the truth 😔😩🤔"
# s = "This is@a_tweet@for12Testing#the#tokens#testing:'(with :)with:D#happy#face:PLOL"
# s = "This is@a_tweet@for12Testing#the#tokens#testing:'(with :)with:D#happy#face:PLOL http://go.co.in/asdaaSD23/43sedf_sad asfda@sdgs.v.in"
# s = "Ignorance abc@gma.co.This is to cope man, ignorance is bliss, ignorance is love and I need that shit R.I.P"
# s = "I don’t know why we’re not leading by a lot."
# s = "Fuck:(!!!!!"
s = "RT @tyleroakley: NEW VIDEO: \"How To Pray The Gay Away\": https://t.co/If3kS0gc3j (RT for a DM full of love!! Sending a bunch today!!) https:…"
print s
s = s.decode('utf8')
print s
o.tokenize(s)
print o.getTokens();