from bs4 import BeautifulSoup
import urllib.request
url= 'http://zevross.com/blog/2014/05/16/using-the-python-library-beautifulsoup-to-extract-data-from-a-webpage-applied-to-world-cup-rankings/'
request = urllib.request.Request(url)
page = urllib.request.urlopen(request)
soup = BeautifulSoup(page.read())
tr = soup.find("tr", {"class": "row2"}).contents
i=2
while i<=6:
    out = soup.find("td", {"class": "col"+str(i)+" sorttable_numeric"}).contents
    print("td[",i,"] = ", out)
    i+=1
