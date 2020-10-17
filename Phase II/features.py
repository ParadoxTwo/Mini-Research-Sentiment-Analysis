import re
import json


class Emoticons:
    def analyse(self, string):
        
        self.string = re.sub(
            r'\W+:\)\(\'\{\}\-\@\>\<\=\;\[\]\!',
            ' ',
            string)
        self.string = self.string.replace('.', '')
        self.string = self.string.replace('?', '')
        self.words = self.string.split(" ")
        if self.words[-1] == '': 
            del self.words[-1]
        positiveEmoz = [
            ':)',
            ':-)',
            ':D',
            ':-D',
            ':P',
            ':p',
            ':-P',
            ';)',
            ';-)',
            ';D',
            ';-D',
            ':o)',
            ':]',
            ':3',
            ':c)',
            ':>',
            '=]',
            '8)',
            'B)',
            'BD',
            '<3',
            '=)',
            ':}',
            '8D',
            'xD',
            'XD',
            'X-D',
            '=D',
            '=3',
            ':-))',
            ':\')',
            'lol',
            'lol!']
        negativeEmoz = [
            ':(',
            ':-(',
            ':(',
            ':-(',
            ':-<',
            ':-[',
            ':[',
            ':{',
            ':-||',
            ':@',
            ':\'-(',
            ':\'(',
            'QQ',
            'D:',
            'D:<',
            'D8',
            'D;',
            'DX',
            '</3',
            '<\\3',
            ':|',
            'v.v',
            '>.<',
            'D=']
        positiveCount = 0
        negativeCount = 0
        for i in self.words:
            if i in positiveEmoz:
                positiveCount += 1
            if i in negativeEmoz:
                negativeCount += 1
        positiveEmoz, negativeEmoz = 0, 0
        if positiveCount + negativeCount == 0:
            return {'positive': 0, 'negative': 0}
        return {'positive': positiveCount, 'negative': negativeCount}


def repairString(string):
    data = {
        'm': 'am',
        'u': 'you',
        'ua': 'your',
        'yrs': 'years',
        'ur': 'your',
        'urs': 'yours',
        'tc': 'take care',
        'gn': 'good night',
        'gm': 'good morning',
        'ryt': 'right',
        'nite': 'night',
        'wat': 'what',
        'abt': 'about',
        'k': 'okay',
        'knw': 'know',
        'nt': 'not',
        'w8': 'wait',
        'f9': 'fine',
        'wbu': 'what about you',
        'kk': 'okay',
        'ok': 'okay',
        'na': 'no',
        'don\'t': 'do not',
        'won\'t': 'will not',
        'gonna': 'going to',
        'juz': 'just',
        'jus': 'just',
        'fk': 'fuck',
        'wtf': 'what the fuck',
        'shud': 'should',
        'coz': 'because',
        'cos': 'because',
        'ttyl': 'talk to you later',
        'ty': 'thank you',
        'hlo': 'hello',
        'helo': 'hello',
        'hola': 'hello',
        '&#x27;': '\'',
        'wut': 'what',
        'gtfo': 'get the fuck out',
        'whr': 'where',
        'y': 'why',
        'ohk': 'okay'}
    string = string.split(" ")
    for i in string:
        if i.lower() in data:
            index = string.index(i)
            string[index] = data[i.lower()]
    return " ".join(string)
