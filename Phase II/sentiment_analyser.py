import nltk,yaml
from emo import split_emo
import datetime
import sqlite3
import features

class Splitter(object):
    def __init__(self):
        self.nltk_splitter = nltk.data.load('tokenizers/punkt/english.pickle')
        self.nltk_tokenizer = nltk.tokenize.TreebankWordTokenizer()

    def split(self, text):
        sentences = self.nltk_splitter.tokenize(text)
        tokenized_sentences = [self.nltk_tokenizer.tokenize(sent) for sent in sentences]
        tokenized_sentences = split_emo(tokenized_sentences)
        return tokenized_sentences


class POSTagger(object):
    def __init__(self):
        pass
        
    def pos_tag(self, sentences):

        pos = [nltk.pos_tag(sentence) for sentence in sentences]
        #adapt format
        pos = [[(word, word, [postag]) for (word, postag) in sentence] for sentence in pos]
        return pos


class DictionaryTagger(object):
    def __init__(self):
        self.dictionary = {}
        self.max_key_size = 0
        conn = sqlite3.connect('knowledgeBase.db')
        c = conn.cursor()
        row = c.execute("SELECT * FROM wordBase;")
        for eachRow in row:
            if eachRow[1] in self.dictionary:
                pass
            else:
                self.max_key_size = max(self.max_key_size, len(eachRow[1]))
                if int(eachRow[3])==1:
                    self.dictionary[eachRow[1]] = ['neutral']
                elif int(eachRow[2])>0:
                    self.dictionary[eachRow[1]] = ['positive']
                elif int(eachRow[2])<0:
                    self.dictionary[eachRow[1]] = ['negative']
                    
        row = c.execute("SELECT * FROM multiplierBase;")
        for eachRow in row:
            if eachRow[1] in self.dictionary:
                pass
            else:
                self.max_key_size = max(self.max_key_size, len(eachRow[1]))
                if int(eachRow[3])==1:
                    self.dictionary[eachRow[1]] = ['neutral']
                elif int(eachRow[2])>1:
                    self.dictionary[eachRow[1]] = ['inc']
                elif int(eachRow[2])<1 and int(eachRow[2])>0:
                    self.dictionary[eachRow[1]] = ['dec']
                elif int(eachRow[2])<0:
                    self.dictionary[eachRow[1]] = ['inv']
        

    def tag(self, postagged_sentences):
        return [self.tag_sentence(sentence) for sentence in postagged_sentences]

    def tag_sentence(self, sentence, tag_with_lemmas=False):
        tag_sentence = []
        N = len(sentence)
        if self.max_key_size == 0:
            self.max_key_size = N
        i = 0
        while (i < N):
            j = min(i + self.max_key_size, N) #avoid overflow
            tagged = False
            while (j > i):
                
                expression_form = ' '.join([word[0] for word in sentence[i:j]]).lower()
                expression_lemma = ' '.join([word[1] for word in sentence[i:j]]).lower()
                if tag_with_lemmas:
                    literal = expression_lemma
                else:
                    literal = expression_form
                if literal in self.dictionary:
                    is_single_token = j - i == 1
                    original_position = i
                    i = j
                    taggings = [tag for tag in self.dictionary[literal]]
                    tagged_expression = (expression_form, expression_lemma, taggings)
                    if is_single_token:
                        original_token_tagging = sentence[original_position][2]
                        tagged_expression[2].extend(original_token_tagging)
                    tag_sentence.append(tagged_expression)
                    tagged = True
                else:
                    j = j - 1
            if not tagged:
                tag_sentence.append(sentence[i])
                i += 1
        return tag_sentence


def value_of(sentiment):
    if sentiment == 'positive': return 1
    if sentiment == 'negative': return -1
    return 0

def sentence_score(sentence_tokens, previous_token, acum_score):    
    if not sentence_tokens:
        return acum_score
    else:
        current_token = sentence_tokens[0]
        tags = current_token[2]
        token_score = sum([value_of(tag) for tag in tags])
        if previous_token is not None:
            previous_tags = previous_token[2]
            prev_token_score = sum([value_of(tag) for tag in previous_token[2]])
            if 'inc' in previous_tags:
                token_score *= 2.0
            elif 'dec' in previous_tags:
                token_score /= 2.0
            elif 'inv' in previous_tags:
                token_score *= -1.0
        return sentence_score(sentence_tokens[1:], current_token, acum_score + token_score)

    
def sentiment_score(review):
    return sum([sentence_score(sentence, None, 0.0) for sentence in review])

##text = """What can I say about this place. :-(  The staff of the restaurant is nice and the eggplant is not bad. Apart from that, very uninspired food, lack of atmosphere and too expensive. :) I am a staunch vegetarian and was sorely dissapointed with the veggie options on the menu. Will be the last time I visit, I recommend others to avoid."""
##text = """He killed him! Killed him. Great! :'( Wtf are you doing?"""
##splitter = Splitter()
##postagger = POSTagger()
##emoji = features.Emoticons()
##emos = emoji.analyse(text)
##text = features.repairString(text)
##print(emos)
##splitted_sentences = splitter.split(text)
##
##print(splitted_sentences)
##print('\n\n')
##pos_tagged_sentences = postagger.pos_tag(splitted_sentences)
##
##print(pos_tagged_sentences)
##
##
##dicttagger = DictionaryTagger([ 'dicts/pos_dict.yml', 'dicts/newpos.yml', 'dicts/pos.yml', 'dicts/pos2.yml', 'dicts/neg_dict.yml', 'dicts/newneg.yml', 'dicts/inc.yml', 'dicts/dec.yml', 'dicts/inv.yml'])
##
##dict_tagged_sentences = dicttagger.tag(pos_tagged_sentences)
##
##print(dict_tagged_sentences)
##sentiments = sentiment_score(dict_tagged_sentences) + emos['positive'] - emos['negative']
##print(sentiments)
