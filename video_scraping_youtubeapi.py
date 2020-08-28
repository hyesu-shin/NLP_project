import requests
import json
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
import sys

# 셀레니움 작동을 위한 코드
delay = 0.5
driver = wd.Chrome("chromedriver.exe")
driver.implicitly_wait(delay)
driver.maximize_window()

# 스크롤링을 위한 코드
# YOUTUBE_IN_LINK = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&maxResults=100&order=relevance&pageToken={pageToken}&videoId={videoId}&key={key}'
YOUTUBE_VIDEO_LINK = 'https://www.googleapis.com/youtube/v3/videos?part=statistics&id={videoId}&key={key}'
YOUTUBE_VIDEO_LINK_FOR_TAG = 'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={videoId}&key={key}'
key = 'AIzaSyDHu-XQGkZwKC9NZ1RcGRxn6USgiuDiCNw'

# view_count = page_info['items']['viewCount']
# print(view_count)

# 검색 목록에서 url을 얻어오자 - 셀레니움
def get_scraping_data(search_query) :
    # 기본 바탕이 되는 url
    base_url = 'http://www.youtube.com/results?search_query='
    url = base_url + search_query

    driver.get(url)
    body = driver.find_element_by_tag_name('body')

    num_of_pagedowns = 5
    # 10번 밑으로 내리기
    while num_of_pagedowns :
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        num_of_pagedowns -= 1

    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')

    all_videos = soup.find_all(id='dismissable')

    title_list = []
    for video in all_videos :
        title = video.find(id='video-title')
        # 공백을 제거하고 글자수가 0보다 크면 append
        if title is not None :
            title_list.append(title.text)
        else : title_list.append(None)

    print(title_list)
    # print(len(title_list))

    # 크롤링 --- 재생 시간 조회
    video_time_list = []
    for video in all_videos :
        video_time = video.find('span', {'class' : 'style-scope ytd-thumbnail-overlay-time-status-renderer'})
        if video_time is not None :
            video_time_list.append(video_time.text.strip())
        else : video_time_list.append(None)

    # video_time_list의 텍스트 데이터를 숫자(초)로 바꾸기
    # def stime(text) :
    #     time_data = text.split(':')
    #     if len(time_data) == 1:
    #         return int(time_data[0])
    #     elif len(time_data) == 2:
    #         return int(time_data[0])*60 + int(time_data[1])
    #     else:
    #         return int(time_data[0])*3600 + int(time_data[1]*60 + int(time_data[2]))

    # video_time_seperate_list = []
    # for time_data in video_time_list :
    #     video_time_seperate_list.append(stime(time_data))

    # print(video_time_seperate_list)

    # # 크롤링 - 조회수 조회
    # view_num_list = []
    # view_num_regexp = re.compile(r'조회수')
    # for video in all_videos :
    #     view_num = video.find('span',{'class':'style-scope ytd-video-meta-block'})
    #     if view_num is not None :
    #         # if view_num_regexp.search(view_num.text) :
    #             # view_num.text에 '조회수' 문자열이 있으면 True
    #         view_num_list.append(view_num.text)
    #     else : view_num_list.append(None)
    # print(view_num_list)

    # def nview(text) :
    #     view = text.replace('조회수','')
    #     num = float(view[:-2])
    #     danwee = view[-2:]

    #     if danwee == '만회':
    #         return int(num*10000)
    #     else:
    #         return int(num*1000)
            
    # view_number_type_list = []
    # for view in view_num_list:
    #     if view is not None :
    #         view_number_type_list.append(nview(view))
    #     else : view_number_type_list.append(None)
    # print(view_number_type_list)

    # 크롤링 --- 영상 url
    video_url_list = []
    for video in all_videos :
        video_url = video.find('a',{'id':'thumbnail'})['href']
        if video_url is not None :
            video_url_list.append(str(video_url).replace('/watch?v=',''))
        else : video_url_list.append(None)
    print(video_url_list)

    comment_count_list = []
    like_count_list = []
    dislike_count_list = []
    view_count_list = []
    video_tag_list = []

    for videoId in video_url_list:
        video_info = requests.get(YOUTUBE_VIDEO_LINK.format(videoId = videoId, key = key))
        video_info = video_info.json()

        video_info_for_tag = requests.get(YOUTUBE_VIDEO_LINK_FOR_TAG.format(videoId=videoId, key=key))
        video_info_for_tag = video_info_for_tag.json()

        view_count = video_info['items'][0]['statistics']['viewCount']
        like_count = video_info['items'][0]['statistics']['likeCount']
        dislike_count = video_info['items'][0]['statistics']['dislikeCount']
        comment_count = video_info['items'][0]['statistics']
        tag = video_info_for_tag['items'][0]['snippet']['description']
        p = re.compile('commentCount.*')
        matched = p.findall(str(comment_count))

        if comment_count is not None :
            comment_count_list.append(matched)
        else : comment_count_list.append(None)

        if dislike_count is not None :
            dislike_count_list.append(dislike_count)
        else : dislike_count_list.append(None)

        if like_count is not None :
            like_count_list.append(like_count)
        else : like_count_list.append(None)

        if view_count is not None :
            view_count_list.append(view_count)
        else : view_count_list.append(None)

        if tag is not None :
            video_tag_list.append(tag)
        else : video_tag_list.append(None)
        
    video_info_list = []

    for i in range(len(title_list)) :
        video_one = []
        video_one.append(search_query)
        video_one.append(title_list[i])
        video_one.append(video_time_list[i])
        video_one.append(view_count_list[i])
        video_one.append(video_url_list[i])
        video_one.append(comment_count_list[i])
        video_one.append(like_count_list[i])
        video_one.append(dislike_count_list[i])
        video_one.append(video_tag_list[i])

        video_info_list.append(video_one)


    return video_info_list
        
# 결과값을 넣을 데이터 프레임
keyword_video_data = []
video_list = pd.DataFrame({
    'keyword' : [],
    'title' : [],
    'privious_time' : [],
    'view' : [],
    'video_url' : [],
    'comment' : [],
    'like_count' : [],
    'dislike_count' : [],
    'tag' : []
})

search_keywords = ['game']

for keyword in search_keywords :
    keyword_video_data = get_scraping_data(keyword)
    print(keyword_video_data)
    for row in keyword_video_data :
        video_list.loc[len(video_list)] = row
    keyword_video_data = []

print(video_list.head())
video_list.to_csv('video_list_test_game1.csv')