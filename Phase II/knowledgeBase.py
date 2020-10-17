import nltk
import re
import time
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
import http.cookiejar as cookielib
from http.cookiejar import CookieJar
import datetime
import sqlite3
import yaml

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Chrome/61.0')]


conn = sqlite3.connect('knowledgeBase.db')
c = conn.cursor()

def loadDicts(dictionary_paths):
    i=0
    files = [open(path, 'r') for path in dictionary_paths]
    dictionaries = [yaml.load(dict_file) for dict_file in files]
    map(lambda x: x.close(), files)
    dictionary = {}
    for curr_dict in dictionaries:
        for key in curr_dict:
            if key not in dictionary:
                if curr_dict[key][0] == 'positive':
                    dictionary[key] = 10
                elif curr_dict[key][0] == 'negative':
                    dictionary[key] = -10
                elif curr_dict[key][0] == 'dec':
                    dictionary[key] = 0.5
                elif curr_dict[key][0] == 'inc':
                    dictionary[key] = 2.0
                elif curr_dict[key][0] == 'inv':
                    dictionary[key] = -1.0

    return dictionary

def updateBases(dictionary):
    for key in dictionary:
        currentTime = time.time()
        dateStamp = datetime.datetime.fromtimestamp(currentTime).strftime('%Y-%m-%d %H: %M: %S')
        if dictionary[key]<=2.0 and dictionary[key]>=-1.0:
            c.execute("UPDATE multiplierBase SET dateStamp=?, adverb=?, factor=?, isNeutral=? WHERE adverb=?",
                              (dateStamp, key, dictionary[key], 0, key));
        else:
            c.execute("UPDATE wordBase SET dateStamp=?, word=?, polarity=?, isNeutral=? WHERE word=?",
                              (dateStamp, key, dictionary[key], 0, key));
        conn.commit()


def IMDBcontent():
    try:
        page = 'http://www.imdb.com/?ref_=nv_home'
        sourceCode = opener.open(page).read().decode('utf-8')
        try:
            #links = re.findall(r'<a.*href=\"(.*?)\"',sourceCode)
            links = []
            try:
                for i in range(1,100): links.append(sourceCode.split('<div class="title"> <a href="')[i].split('">')[0])
            except :
                pass
            print(links)
            reviewLinks = []
            for link in links:
                try:
                    subpage = site+link
                    linkCode = opener.open(subpage).read().decode('utf-8')
                    tID = link[7:16]
                    print(tID)
                    for start in {0,10,20,30}:
                        reviewLink = 'http://www.imdb.com/title/'+tID+'/reviews?start='+str(start)
                        print(reviewLink)
                        reviewLinks.append(reviewLink)
                except Exception as e:
                    print('Failed in the 3rd loop')
                    print(str(e))
            print(reviewLinks)
            for link in reviewLinks:
                try:
                    for i in range(1,10):
                        fail = False
                        try:
                            linkCode = opener.open(link).read().decode('utf-8')
                            reviewStart = '<img width="102" height="12" alt="'
                            reviewEnd = '</p>\n\n<div class="yn"'
                            review = linkCode.split(reviewStart)[i].split(reviewEnd)[0]
                            review = '::rate::'+review+'::content::'
                            rating = review.split('::rate::')[1].split('/10')[0]
                            content = review.split('</div>\n<p>')[1].split('::content::')[0]
                            print(rating)
                            print(content)
                        except Exception as e:
                            print('Failed in 4th loop, ', str(e))
                            fail = True
                        if not fail:
                            ratingArray.append(rating)
                            contentArray.append(content)
                        
                except Exception as e:
                    print('Failed in 3rd b loop, ', str(e))
        except Exception as e:
            print('Failed in the 2nd loop')
            print (str(e))


    except Exception as e:
        print ('Failed in the 1st loop')
        print (str(e))

    i = 1
    for content in contentArray:
        print('Rating: '+str(i))
        print(ratingArray[i-1])
        if len(content)>0:
            print('Content: '+str(i),', Size: '+str(len(content)))
        else:
            print('Content: '+str(i),'None')
        print(content)
        i+=1


def buildWordBase(dictionary):
    for key in dictionary:
        currentTime = time.time()
        value = dictionary[key]
        dateStamp = datetime.datetime.fromtimestamp(currentTime).strftime('%Y-%m-%d %H: %M: %S')
        c.execute("INSERT INTO wordBase (dateStamp, word, polarity, isNeutral) VALUES (?, ?, ?, ?);",
                (dateStamp, key, value, 0))
        conn.commit()

def buildMultiplierBase(dictionary):
    for key in dictionary:
        currentTime = time.time()
        value = dictionary[key]
        dateStamp = datetime.datetime.fromtimestamp(currentTime).strftime('%Y-%m-%d %H: %M: %S')
        c.execute("INSERT INTO multiplierBase (dateStamp, adverb, factor, isNeutral) VALUES (?, ?, ?, ?);",
                (dateStamp, key, value, 0))
        conn.commit()

dict_paths = [ 'dicts/pos_dict.yml', 'dicts/newpos.yml', 'dicts/pos.yml', 'dicts/pos2.yml',
               'dicts/neg_dict.yml', 'dicts/newneg.yml', 'dicts/inc.yml', 'dicts/dec.yml', 'dicts/inv.yml']
#dictionary = loadDicts(multiplier_dict)
#buildMultiplierBase(dictionary)

def amazonContent(aSearch, keyword):
    try:
        page = aSearch+keyword
        print('begin...')
        sourceCode = opener.open(page).read().decode('utf-8')
        try:
            #links = re.findall(r'<a.*href=\"(.*?)\"',sourceCode)
            links = []
            opening = '<div class="a-row a-spacing-none"><a class="a-link-normal a-text-normal" href="'
            closing = '"><span class="a-size-small a-color-secondary"></span><span class="a-size-base a-color-price s-price a-text-bold"><span class="currencyINR">'
            closing = '"><span class="a-price" data-a-size="l" data-a-color="base"><span class="a-offscreen">'
            try:
                for i in range(1,100): links.append(sourceCode.split(opening)[i].split(closing)[0])
            except :
                pass
            print(links)
            reviewLinks = []
            for link in links:
                try:
                    linkCode = opener.open(link).read().decode('utf-8')
                    opening = '<a id="acrCustomerReviewLink" class="a-link-normal" href="'
                    closing = '">'
                    reviewLink = site+linkCode.split(opening)[1].split(closing)[0]
                    print(reviewLink)
                    reviewLinks.append(reviewLink)
                except Exception as e:
                    print('Failed in the 3rd loop')
                    print(str(e))
            print(reviewLinks)
            for link in reviewLinks:
                try:
                    linkCode = opener.open(link).read().decode('utf-8')
                    for i in range(1,3):
                        opening = '<div class="a-row a-spacing-top-mini"><span class="a-size-base">'
                        closing = '</span></div></div><div\n    class="a-expander-header a-expander-partial-collapse-header readMore">'
                        rClosing = '.0 out of 5 stars'
                        rating = linkCode.split('review-rating"><span class="a-icon-alt">')[i].split(closing)[0]
                        rating = '::start::'+rating+'::end::'
                        testR = rating.split(opening)[1].split('::end::')[0]
                        rating = rating.split('::start::')[1].split(rClosing)[0]
                        print(testR)
                        print(rating)
                        if int(rating)>3 or int(rating)<3:
                            ratingArray.append(rating)
                            contentArray.append(testR)
                except Exception as e:
                    print('Failed in 3rd b loop: ', str(e))
        except Exception as e:
            print('Failed in the 2nd loop')
            print (str(e))


    except Exception as e:
        print ('Failed in the 1st loop')
        print (str(e))
    i = 1
    for content in contentArray:
        print('Rating: '+str(i))
        print(ratingArray[i-1])
        if len(content)>0:
            print('Content: '+str(i),', Size: '+str(len(content)))
        else:
            print('Content: '+str(i),'None')
        print(content)
        i+=1



def buildBase(polarity, content):
    content = content.lower()
    tokenized = nltk.word_tokenize(content)
    postagged = nltk.pos_tag(tokenized)
    for word in postagged:
        polarity2 = polarity
        if word[1][:2] == 'JJ':
            row = c.execute("SELECT * FROM wordBase;")
            exists = False
            currentTime = time.time()
            dateStamp = datetime.datetime.fromtimestamp(currentTime).strftime('%Y-%m-%d %H: %M: %S')
            for eachRow in row:
                if word[0].lower() == eachRow[1]:
                    print(eachRow)
                    print(word[0])
                    exists = True
                    pol = c.execute("SELECT polarity FROM wordBase WHERE word=?", (word[0],))
                    for eachPol in pol:
                        print(eachPol)
                        polarity2+=eachPol[0]
                    c.execute("UPDATE wordBase SET dateStamp=?, word=?, polarity=?, isNeutral=? WHERE word=?",
                              (dateStamp, eachRow[1], polarity2, eachRow[3], word[0].lower()));
            if not exists:
                c.execute("INSERT INTO wordBase (dateStamp, word, polarity, isNeutral) VALUES (?, ?, ?, ?);",
                (dateStamp, word[0], polarity2, 0))
            print(polarity2)
            conn.commit()
        elif word[1] == 'RB':
            row = c.execute("SELECT * FROM multiplierBase;")
            if polarity>0:
                polarity2 = 2.0
            elif polarity<0:
                polarity2 = 0.5
            exists = False
            currentTime = time.time()
            dateStamp = datetime.datetime.fromtimestamp(currentTime).strftime('%Y-%m-%d %H: %M: %S')
            for eachRow in row:
                if word[0].lower() == eachRow[1]:
                    print(eachRow)
                    print(word[0])
                    exists = True
                    pol = c.execute("SELECT factor FROM multiplierBase WHERE adverb=?", (word[0],))
                    for eachPol in pol:
                        print(eachPol)
                        polarity2*=eachPol[0]
                    c.execute("UPDATE multiplierBase SET dateStamp=?, adverb=?, factor=?, isNeutral=? WHERE adverb=?",
                              (dateStamp, eachRow[1], polarity2, eachRow[3], word[0].lower()));
            if not exists:
                c.execute("INSERT INTO multiplierBase (dateStamp, adverb, factor, isNeutral) VALUES (?, ?, ?, ?);",
                (dateStamp, word[0], polarity2, 0))
            print(polarity2)
            conn.commit()

def processContent():
    try:
        i = 1
        dictionary = loadDicts(dict_paths)
        for content in contentArray:
            if len(content)>0 and len(content)<2000:
                if int(ratingArray[i-1])>6:
                    buildBase(1, content)
                elif int(ratingArray[i-1])<5:
                    buildBase(-1, content)
            i+=1
        updateBases(dictionary)
    except Exception as e: 
        print ('Error: ',e)


contentArray = []
ratingArray = []
#IMDBcontent()
site = 'https://www.amazon.in'
aSearch = 'https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords='
keyword = 'phones'
amazonContent(aSearch, keyword)
#processContent()
