import nltk,yaml
from emo import split_emo
import datetime
import sqlite3
import features
from sentences import positive, negative


class Splitter(object):
    def __init__(self):
        self.nltk_splitter = nltk.data.load('tokenizers/punkt/english.pickle')
        self.nltk_tokenizer = nltk.tokenize.TreebankWordTokenizer()

    def split(self, text):
        """
        input format: a paragraph of text
        output format: a list of lists of words.
            e.g.: [['this', 'is', 'a', 'sentence'], ['this', 'is', 'another', 'one']]
        """
        sentences = self.nltk_splitter.tokenize(text)
        tokenized_sentences = [self.nltk_tokenizer.tokenize(sent) for sent in sentences]
        tokenized_sentences = split_emo(tokenized_sentences)
        return tokenized_sentences


class POSTagger(object):
    def __init__(self):
        pass
        
    def pos_tag(self, sentences):
        """
        input format: list of lists of words
            e.g.: [['this', 'is', 'a', 'sentence'], ['this', 'is', 'another', 'one']]
        output format: list of lists of tagged tokens. Each tagged tokens has a
        form, a lemma, and a list of tags
            e.g: [[('this', 'this', ['DT']), ('is', 'be', ['VB']), ('a', 'a', ['DT']), ('sentence', 'sentence', ['NN'])],
                    [('this', 'this', ['DT']), ('is', 'be', ['VB']), ('another', 'another', ['DT']), ('one', 'one', ['CARD'])]]
        """

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
        """
        the result is only one tagging of all the possible ones.
        The resulting tagging is determined by these two priority rules:
            - longest matches have higher priority
            - search is made from left to right
        """
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


splitter = Splitter()
postagger = POSTagger()
emoji = features.Emoticons()
dicttagger = DictionaryTagger()
posCount = 0
negCount = 0
i=1
print('Positive Sentences:')
for text in positive:
    emos = emoji.analyse(text)
    text = features.repairString(text)
    splitted_sentences = splitter.split(text)
    pos_tagged_sentences = postagger.pos_tag(splitted_sentences)
    dict_tagged_sentences = dicttagger.tag(pos_tagged_sentences)
    sentiments = sentiment_score(dict_tagged_sentences) + emos['positive'] - emos['negative']
    if sentiments>0:
        posCount+=1
    print('Score '+str(i)+': '+str(sentiments))
    i+=1

print('Negative Sentences:')
i=1
for text in negative:
    emos = emoji.analyse(text)
    text = features.repairString(text)
    splitted_sentences = splitter.split(text)
    pos_tagged_sentences = postagger.pos_tag(splitted_sentences)
    dict_tagged_sentences = dicttagger.tag(pos_tagged_sentences)
    sentiments = sentiment_score(dict_tagged_sentences) + emos['positive'] - emos['negative']
    if sentiments<0:
        negCount+=1
    print('Score '+str(i)+': '+str(sentiments))
    i+=1

print('Phase II Result:')
print('Accuracy for positive statements = '+str(100*posCount/len(positive)))
print('Accuracy for negative statements = '+str(100*negCount/len(negative)))
