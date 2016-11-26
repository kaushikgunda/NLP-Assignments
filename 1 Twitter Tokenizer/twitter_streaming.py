from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json, sys, re

#Variables that contains the user credentials to access Twitter API 
access_token = "80055621-Zce91hHUCq8N781GFG5kVsU7DnaWs040cwPsWPDVl"
access_token_secret = "qzMI068onGJI4Zo2QDCbAGWHkGbPwzGcj0Koroa9gMUpW"
consumer_key = "xF7R9nJeIbWJ0etNGM0U95MOL"
consumer_secret = "JhvmRvKMLlm9Hws8bofuoi9pjqX46vuOBakeAnsjVYxhtgriYj"

# Output file
outFile = ""

class StdOutListener(StreamListener):
    def on_data(self, data):
        j =json.loads( data )
        if 'text' in j.keys():
            print j['text']
            outFile.write( j['text'].encode('utf-8').strip() )
            outFile.write( '\n' )

        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    outFile = open( sys.argv[1], 'w' )

    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    stream.filter(languages=["en"], track=['disney', 'avengers', 'animation', 'love', 'happy', 'amazing', 'fun' ])
