import requests
import json

headers = {
    'authority': 'www.youtube.com',
    'x-youtube-device': 'cbr=Chrome&cbrver=84.0.4147.135&ceng=WebKit&cengver=537.36&cos=Windows&cosver=10.0',
    'x-youtube-page-label': 'youtube.ytfe.desktop_20200825_2_RC1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    'x-youtube-variants-checksum': 'c2cd0e78f6e12ec78e265ca4cfe4c726',
    'content-type': 'application/x-www-form-urlencoded',
    'x-youtube-page-cl': '328441518',
    'x-spf-referer': 'https://www.youtube.com/watch?v=Gmu2sOUf4yw',
    'x-youtube-utc-offset': '540',
    'x-youtube-client-name': '1',
    'x-spf-previous': 'https://www.youtube.com/watch?v=Gmu2sOUf4yw',
    'x-youtube-client-version': '2.20200826.02.01',
    'x-youtube-identity-token': 'QUFFLUhqbTVlUDR6N3ExNGlaLXJDclRWTE15ek8wbDd3UXw=',
    'x-youtube-time-zone': 'Asia/Seoul',
    'x-youtube-ad-signals': 'dt=1598548819649&flash=0&frm&u_tz=540&u_his=13&u_java&u_h=864&u_w=1536&u_ah=864&u_aw=1474&u_cd=24&u_nplug=3&u_nmime=4&bc=31&bih=794&biw=1131&brdim=0%2C0%2C0%2C0%2C1474%2C0%2C1474%2C864%2C1148%2C794&vis=1&wgl=true&ca_type=image&bid=ANyPxKr15SN_Ubfw1KNc6UlNzBKNLAJdgOVh1AaSy1LkLV8DBOgFVOfOFZvFGpOeUdaHW7v9HGYXOuDRJsKgbxOyUKCkNtHJ8g',
    'accept': '*/*',
    'origin': 'https://www.youtube.com',
    'x-client-data': 'CJS2yQEIpbbJAQjEtskBCKmdygEIhrXKAQiZtcoBCP+8ygEI9cfKAQjnyMoBCOnIygEItMvKAQiW1soBCLvXygE=',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.youtube.com/watch?v=Gmu2sOUf4yw',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'VISITOR_INFO1_LIVE=IFM-ttbSCGk; LOGIN_INFO=AFmmF2swRQIhAK4iDNl7RkopatsFOZ9wprSJi69WrZNHuElLoweNc_GwAiA4s_0vBLEODdNdAiuOZEbaO4UtccUwavzkWfJdS8sOVw:QUQ3MjNmeUFRX2ZUZklvd0ZYZUpJcDdVcVFpNmNpNUNmQ3FrVUJaMzdrV3NhWGpqNFVGVHVEbEpFVGtodTRIdmZtNTZIT3dWQUR2MVFZSlh5cm1RMTZFa1dqNHI5ZWJjX2h3aWlsbzJOZkhTdnIxbHZJVlBpN0ptR2lZeVVnbzhfcENCTmNSR1Mxc3V1Smtab0VBNm53V1E0Rm9MajRDQ05zbndWWHJHYkJtNFhYUUItSU1GcjJJeURqTmRQRmhGcmpmbS1tNGk2TjRL; PREF=al=en&f4=4000000&f5=20000; SID=0QcpSv5RKfUPbIoTSnIujWk-zFREkaNpdeUMtbm1ntHgih7Y-9U3TaIGIlW1y9HGb1GRNA.; __Secure-3PSID=0QcpSv5RKfUPbIoTSnIujWk-zFREkaNpdeUMtbm1ntHgih7YZBacOZNkp3MANVN3um-KnQ.; HSID=Addn-orBsQ0k6Atut; SSID=AsVtLXJMI9spmc740; APISID=x5AAOddm-jCXzwio/AXJgbaKuFangIfrS6; SAPISID=32D1ifbqkLiGzYxL/AC3zpYapUN1_4NRu1; __Secure-3PAPISID=32D1ifbqkLiGzYxL/AC3zpYapUN1_4NRu1; YSC=zS6uGd1bqjM; SIDCC=AJi4QfHoNUJZzfubIUji4SqW3p8XyCYEVyliI9xzI2dX47JViOpBalUdR-kKhBNut_wj4TFOOg; __Secure-3PSIDCC=AJi4QfF43cP86PrIUBBO2eSU-fgKV2wRKVRM0J6No_4ghpUzcTkc-NRrTO4y4YeoGc6ykBX7EA',
}

params = (
    ('action_get_comments', '1'),
    ('pbj', '1'),
    ('ctoken', 'EiYSC0dtdTJzT1VmNHl3wAEAyAEA4AECogINKP___________wFAABgG'),
    ('continuation', 'EiYSC0dtdTJzT1VmNHl3wAEAyAEA4AECogINKP___________wFAABgG'),
    ('itct', 'CNMBEMm3AiITCInvl7Tyu-sCFQl1YAodylgKyA=='),
)

data = {
  'session_token': 'QUFFLUhqblZzc0oxS2FPVGJDeTNXVlJFQmc3cGs1Szl5d3xBQ3Jtc0ttQ08tc0dOTmZXR003cU5ndGo2MlZ2WkNlTDFCbUk0b0VhNlYwUXdxVnFvS1hQZDRkbzhVYW9iazRaWW96S19XczctYjRLazZaNzBfSFktdVFLcEtFT1Nld1NiVXQ3cTk5dEg1RmVwM2IyTmdodXNRMDRzcFhUM0xhS0Y2NTJDeUktZk9mdV80RW1naXdBVjFHX2RCMnZrcUpPYkE='
}

response = requests.post('https://www.youtube.com/comment_service_ajax', headers=headers, params=params, data=data)

result = json.loads(response.text)
comment_count = result['response']['continuationContents']['itemSectionContinuation']['header']['commentsHeaderRenderer']['countText']['runs'][0]
print(comment_count)
#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.post('https://www.youtube.com/comment_service_ajax?action_get_comments=1&pbj=1&ctoken=EiYSC0dtdTJzT1VmNHl3wAEAyAEA4AECogINKP___________wFAABgG&continuation=EiYSC0dtdTJzT1VmNHl3wAEAyAEA4AECogINKP___________wFAABgG&itct=CNMBEMm3AiITCInvl7Tyu-sCFQl1YAodylgKyA%3D%3D', headers=headers, data=data)
