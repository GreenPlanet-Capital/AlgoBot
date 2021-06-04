import requests
from bs4 import BeautifulSoup
import csv

ticker_list = []
alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
for j in alphabets:
    base_URL = "https://www.advfn.com/nyse/newyorkstockexchange.asp?companies="
    URL = str(base_URL) + str(j)
    r = requests.get(URL)
    
    soup = BeautifulSoup(r.content, 'html5lib')

    super_ts0 = soup.findAll('tr', attrs = {'class':'ts0'})
    for child_wrap_ts0 in super_ts0:
        for i,ticker in enumerate(child_wrap_ts0):
            if(i%2 != 0):
                ticker_list.append(ticker.a.text)

    super_ts1 = soup.findAll('tr', attrs = {'class':'ts1'})
    for child_wrap_ts1 in super_ts1:
        for i,ticker in enumerate(child_wrap_ts1):
            if(i%2 != 0):
                ticker_list.append(ticker.a.text)
    print(j)

print(len(ticker_list))

