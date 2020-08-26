import requests
import json
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd
import re

SCROLL_PAUSE_TIME = 1
# 각 동영상의 파라미터 값 받아와서 셀레니움으로 스크래핑 해 주는 함수
def get_scraping_data(video_params) :

    title_list = []
    like_list = []
    dislike_list = []
    video_comment_list = []

    driver_path = 'chromedriver.exe'
    driver = wd.Chrome(driver_path)

    base_url = "https://www.youtube.com/watch?v="

    for video in video_params :
        url = base_url + video
        driver.get(url)
        time.sleep(SCROLL_PAUSE_TIME)
        # body = driver.find_element_by_tag_name('body')
        # num_of_page_down = 3
        # while num_of_page_down != 0:
        #     # 현재 화면의 길이를 리턴 받아 last_height에 넣기
        #     last_height = driver.execute_script('return document.documentElement.scrollHeight')

        #     for i in range(2) :
        #         # body 본문에 END키를 입력(스크롤 내림)
        #         body.send_keys(Keys.END)
        #         time.sleep(SCROLL_PAUSE_TIME)
        #         num_of_page_down -= 1

        #     new_height = driver.execute_script('return document.documentElement.scrollHeight')

        #     if new_height == last_height :
        #         break;


        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        title = soup.find('yt-formatted-string',{'class':'style-scope ytd-video-primary-info-renderer'})
        if title is not None :
            title_list.append(title.text)
        else : title_list.append(0)

        like = soup.find('yt-formatted-string',{'id':'text','class':'style-scope ytd-toggle-button-renderer style-text','aria-label':re.compile('좋아요')})
        if like is not None :
            like_list.append(like.text)
        else : like_list.append(0)

        dislike = soup.find('yt-formatted-string',{'id':'text','class':'style-scope ytd-toggle-button-renderer style-text','aria-label':re.compile('싫어요')})
        if dislike is not None :
            dislike_list.append(dislike.text)
        else : dislike_list.append(0)

        # 댓글 받아오는 부분
        # all_comments = soup.find_all('ytd-comment-renderer',{'class':'style-scope ytd-comment-thread-renderer'})

        # comment_list = []
        # for comment in all_comments :

        #     if comment.find('yt-formatted-string',{'id':'content-text'},'span') :
        #         content = comment.find('yt-formatted-string',{'id':'content-text'},'span')
        #     else :
        #         content = comment.find('yt-formatted-string',{'id':'content-text'})

        #     if len(content.text.strip()) > 0 :
        #         comment_list.append(content.text)

        # # print(comment_list)
        # # print(len(comment_list))

        # user_list = []
        # for comment in all_comments :
        #     user = comment.find('a',{'id':'author-text'},'span')

        #     if len(user.text.strip()) > 0 :
        #         user_list.append(user.text.replace('\n','').replace(' ', ''))

        # like_list = []

        # for comment in all_comments :
        #     like = comment.find('span',{'id':'vote-count-left'})

        #     if len(like.text.strip()) > 0 :
        #         like_list.append(like.text.replace('\n','').replace(' ', ''))

        # dict_youtube_comment = {
        #     'user' : comment_list,
        #     'content' : user_list,
        #     'like' : like_list
        # }

        # video_comment_list.append(dict_youtube_comment)

    video_dict = {
        'title' : title_list,
        'like' : like_list,
        'dislike' : dislike_list
        # 'comments' :video_comment_list
    }

    video_dict_pd = pd.DataFrame(video_dict)

    return video_dict_pd


search_query = input('검색어를 입력하세요 : \n')

headers = {
    'x-youtube-client-name': '1',
    'x-youtube-client-version': '2.20200806.01.01'
}

video_headers = {
    'authority': 'www.youtube.com',
    'x-youtube-sts': '18484',
    'x-youtube-device': 'cbr=Chrome&cbrver=84.0.4147.105&ceng=WebKit&cengver=537.36&cos=Macintosh&cosver=10_15_5',
    'x-youtube-page-label': 'youtube.ytfe.desktop_20200805_1_RC1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'x-youtube-variants-checksum': 'a85f7843f63a8b7d2f0e800feae56a8e',
    'x-youtube-page-cl': '325146078',
    'x-spf-referer': 'https://www.youtube.com/results?search_query=%EA%B0%A4%EB%9F%AD%EC%8B%9C+%EB%85%B8%ED%8A%B8+20',
    'x-youtube-utc-offset': '540',
    'x-youtube-client-name': '1',
    'x-spf-previous': 'https://www.youtube.com/results?search_query=%EA%B0%A4%EB%9F%AD%EC%8B%9C+%EB%85%B8%ED%8A%B8+20',
    'x-youtube-client-version': '2.20200806.01.01',
    'dpr': '2',
    'x-youtube-time-zone': 'Asia/Seoul',
    'x-youtube-ad-signals': 'dt=1597134462858&flash=0&frm&u_tz=540&u_his=7&u_java&u_h=1050&u_w=1680&u_ah=1027&u_aw=1680&u_cd=30&u_nplug=3&u_nmime=4&bc=31&bih=948&biw=629&brdim=0%2C23%2C0%2C23%2C1680%2C23%2C1680%2C1027%2C644%2C948&vis=1&wgl=true&ca_type=image',
    'accept': '*/*',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.youtube.com/results?search_query=%EA%B0%A4%EB%9F%AD%EC%8B%9C+%EB%85%B8%ED%8A%B8+20',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': 'VISITOR_INFO1_LIVE=JBcPohHFkb8; GPS=1; YSC=uVMfLNJ5nV8; PREF=f4=4000000; ST-1gdf4lt=csn=e1cyX_POJZWU4wKH5ZKYAQ&itct=CIsBENwwGAEiEwil0Ym73pLrAhXTEVgKHcD9DGQyBnNlYXJjaFIT6rCk65-t7IucIOuFuO2KuCAyMJoBAxD0JA%3D%3D',
}


params = (
    ('search_query', search_query),
    ('pbj', '1'),
)

response = requests.get('https://www.youtube.com/results',
                        headers=headers, params=params)
result = json.loads(response.text)

contents = result[1]['response']['contents']['twoColumnSearchResultsRenderer']['primaryContents'][
    'sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']

# videoId는 검색한 영상의 리스트 목록
videoId = []

for content in contents:
    keys = list(content.keys())

    if 'videoRenderer' in keys:
        videoId.append(content['videoRenderer']['videoId'])

a = ['ESKfHHtiSjs']
print(get_scraping_data(videoId))
