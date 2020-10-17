#ss1 = [['RT', '@', 'iempress_1', ':', '\ud83d\udd36Postage', 'Stamp', 'on', 'LORD', 'RAM', 'released', 'by', 'PM', '#', 'Modi', '\ud83d\udd36It', 'depicts', 'different', 'aspects', 'of', 'Lord', 'RAM', "'s", 'life', '\ud83d\udd361st', 'of…']]

def isEmo(c):
    for i in range(33,127):
        if chr(i) == c:
            return False
    return True

def split_emo(sentences):
    for sentence in sentences:
        for word in sentence:
            counter = 0 
            if isEmo(word[0]) and isEmo(word[1]) and len(word)>2:
                word1 = word[:2]
                word2 = word[2:]
                n = sentence.index(word)
                del(sentence[n])
                sentence.insert(n,word1)
                sentence.insert(n+1,word2)
    return sentences

#ss1 = split_emo(ss1)
#print(ss1)
