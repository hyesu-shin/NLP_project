from bs4 import BeautifulSoup
import requests
import re
import json

##### 제이슨 파싱해서 뽑아본 내용 #####

headers = {
    'authority': 'www.youtube.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'x-client-data': 'CJS2yQEIpbbJAQjEtskBCKmdygEIhrXKAQiZtcoBCP+8ygEI9cfKAQjnyMoBCOnIygEItMvKAQiW1soBCLvXygE=',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'VISITOR_INFO1_LIVE=IFM-ttbSCGk; LOGIN_INFO=AFmmF2swRQIhAK4iDNl7RkopatsFOZ9wprSJi69WrZNHuElLoweNc_GwAiA4s_0vBLEODdNdAiuOZEbaO4UtccUwavzkWfJdS8sOVw:QUQ3MjNmeUFRX2ZUZklvd0ZYZUpJcDdVcVFpNmNpNUNmQ3FrVUJaMzdrV3NhWGpqNFVGVHVEbEpFVGtodTRIdmZtNTZIT3dWQUR2MVFZSlh5cm1RMTZFa1dqNHI5ZWJjX2h3aWlsbzJOZkhTdnIxbHZJVlBpN0ptR2lZeVVnbzhfcENCTmNSR1Mxc3V1Smtab0VBNm53V1E0Rm9MajRDQ05zbndWWHJHYkJtNFhYUUItSU1GcjJJeURqTmRQRmhGcmpmbS1tNGk2TjRL; PREF=al=en&f4=4000000&f5=20000; SID=0QcpSv5RKfUPbIoTSnIujWk-zFREkaNpdeUMtbm1ntHgih7Y-9U3TaIGIlW1y9HGb1GRNA.; __Secure-3PSID=0QcpSv5RKfUPbIoTSnIujWk-zFREkaNpdeUMtbm1ntHgih7YZBacOZNkp3MANVN3um-KnQ.; HSID=Addn-orBsQ0k6Atut; SSID=AsVtLXJMI9spmc740; APISID=x5AAOddm-jCXzwio/AXJgbaKuFangIfrS6; SAPISID=32D1ifbqkLiGzYxL/AC3zpYapUN1_4NRu1; __Secure-3PAPISID=32D1ifbqkLiGzYxL/AC3zpYapUN1_4NRu1; YSC=zS6uGd1bqjM; __Secure-3PSIDCC=AJi4QfHeHRzfmQKURSV95RwYCwjah5xm0gnrTXpe_2o__sGb7DxnHUVIpjHIksXZJAPM9df4XA; SIDCC=AJi4QfEpBao869M3-I-L8GwhFbA8JdJ8p1SKw-CqIRi2qPSwyQ6QJrArvHIX3XpHFD1JKnty8A',
}

params = (
    ('v', 'Gmu2sOUf4yw'),
)

response = requests.get('https://www.youtube.com/watch', headers=headers, params=params)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://www.youtube.com/watch?v=Gmu2sOUf4yw', headers=headers)

soup = BeautifulSoup(response.text, 'html.parser')

matched = re.search('["tooltip":].*?}', str(soup), re.I|re.S)
print(matched[0])


# 제목 가져오기
title = soup.find('meta', {'name' : 'title'})['content']

# description
description = soup.find('meta', {'name' : 'description'})['content']

# keywords
keywords = soup.find('meta', {'name' : 'keywords'})['content']

# views
views = soup.find('meta', {'itemprop':'interactionCount'})['content']


print(description)
print(keywords)