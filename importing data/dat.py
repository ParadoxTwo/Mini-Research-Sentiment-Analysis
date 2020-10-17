token = 'EAACEdEose0cBAD8QuyHVF0hQkGt0ZCCgpZAurBJfdfnYPEHzX2r8qk6MwvoZAathlqS3E8sE3ZASHSOSCLVzqighBy9iPWFVWRqwHVCNf0wBzTBYs6DW6lNf5hsA3ak2P9f6ukoHKSJ13FtjYZA2xyBXZAoLlvEOKwpsN8BrHSae538JJoB2xCCEFZCqHbQH7v0e0mcPaYGZBupyULOQaAZAKFVFcRNVeTuM0dVsXunI7LQZDZD'
me = 'https://graph.facebook.com/v2.10/me?access_token='+token
friends = 'https://graph.facebook.com/v2.10/me/friends?access_token='+token
search = 'https://graph.facebook.com/v2.10/search?q=mark zuckerberg&type=user&access_token='+token
import requests
me1 = requests.get(me)
print(me1.text)
me2 = requests.get(friends)
print(me2.text)
s = requests.get(search)
print(s.text)
