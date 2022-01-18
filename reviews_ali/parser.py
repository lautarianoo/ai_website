from os.path import basename

import requests
import codecs
from bs4 import BeautifulSoup as BS
from random import randint
import re
from re import sub
from decimal import Decimal
import io
from datetime import datetime
import pandas as pd

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Accept': 'text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8'},

    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64;) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112',
    'Accept': 'text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8'},

    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Accept': 'text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8'}
]

count = 0
request = requests.get('https://yandex.ru/turbo/tekhnotop.ru/s/top-100-neveroyatno-poleznyh-tovarov-s-aliehpress/', headers=headers[randint(0, 2)])
if request.status_code == 200:
    soup = BS(request.content, 'html.parser')
    links = soup.find_all('a', attrs={'class': 'su-button-style-default'})
    for link in links:
        count += 1
        url = link.get('href')
        request2 = requests.get(url, headers=headers[randint(0, 2)])
        if request2.status_code == 200:
            soup2 = BS(request2.content, 'html.parser')

            price = soup2.find('div', attrs={'class': 'product-main-wrap'})
            a =1
