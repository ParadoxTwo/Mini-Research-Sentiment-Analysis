from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener
import time, urllib, re
from textblob import TextBlob
from sentiment_analyser import Splitter, POSTagger, DictionaryTagger, value_of
from sentiment_analyser import sentence_score, sentiment_score
import features

ckey = 'McfEpmGoArTag1y0YEgLmAw9B'
csecret = 'nhh8YrANBIS1CcjM6T1XZr9dDuBOFBK69fyR3vIISlNKQUzmTF'
atoken = '580508392-TGvre1m0EqXppjxZoiNoB7B4bfDBxG61m4rOwIdo'
asecret = 'ZWLk0U1KilShIZHeJnYGshMhxI11JLHL9WurC9IsNck0m'

def get_sentiment(tweet):
        analysis = TextBlob(tweet)
        return analysis.sentiment.polarity


class listener(StreamListener):
    def __init__(self):
        self.limit = 20
        self.count = 0
        self.positive_score = 0.0
        self.p_count = 0.0
        self.n_count = 0.0
        self.neutral = 0.0
        self.negative_score = 0.0

    def on_data(self, data):
        self.count+=1
        if self.count>self.limit:
            print('\n\n==================')
            print('ANALYSIS COMPLETE: ')
            print('==================\n')
            print('Average sentiment score on the Modi: '+str((self.positive_score+self.negative_score)/self.limit))
            print('Percentage of people who gave +ve tweets: '+str((100*self.p_count/self.limit)))
            print('Percentage of people who gave -ve tweets: '+str((100*self.n_count/self.limit)))
            print('Percentage of people who gave neutral tweets: '+str((100*self.neutral/self.limit)))
            exit(0)
        tweet = data.split(',"text":"')[1].split('","')[0]
        text = str(tweet)
        splitter = Splitter()
        postagger = POSTagger()
        emoji = features.Emoticons()
        emos = emoji.analyse(text)
        text = features.repairString(text)
        splitted_sentences = splitter.split(text)
        pos_tagged_sentences = postagger.pos_tag(splitted_sentences)
        dicttagger = DictionaryTagger()
        dict_tagged_sentences = dicttagger.tag(pos_tagged_sentences)
        senti = sentiment_score(dict_tagged_sentences) + emos['positive'] - emos['negative']
        if senti>0:
            self.positive_score+=senti
            self.p_count+=1
        elif senti<0:
            self.negative_score+=senti
            self.n_count+=1
        else:
            self.neutral+=1
        date = data.split('{"created_at":"')[1].split('","id":')[0]
        favorites = int(data.split(',"favorite_count":')[1].split(',"entities":')[0])
        followers = int(data.split(',"followers_count":')[1].split(',"friends_count":')[0])
        if followers!=0:
            interest_level = 100*favorites/followers
        else:
            interest_level = 0
        retweets = data.split(',"retweet_count":')[1].split(',"favorite_count":')[0]
        try:
            file = open('tDB.csv','a')
            file.write(text)
            file.write('\n')
            file.write(str(senti))
            file.write('\n')
            file.close()
            print('Tweet: ', text, '\nDate: ', date, '\nFavorites: ', favorites, '\nRetweets: ', retweets, '\nSentiment Rating: ', senti, '\nInterest Level: ', "%.2f"%interest_level,'%')
        except BaseException as e:
            print('Failed '+str(e))
            time.sleep(5)
            return False
        return True

    def on_error(self, status):
        print(status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
l = listener()
twitterStream = Stream(auth, l)
twitterStream.filter(track=['Modi'])
