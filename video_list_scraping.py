import requests
import json
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd
import re

def get_scraping_data(search_query) :
    # 기본 바탕이 되는 url
    base_url = 'http://www.youtube.com/results?search_query='
    url = base_url + search_query
    delay = 0.5

    driver = wd.Chrome("chromedriver.exe")
    driver.implicitly_wait(delay)
    driver.maximize_window()

    driver.get(url)
    body = driver.find_element_by_tag_name('body')

    num_of_pagedowns = 3
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

    # print(title_list)
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

    # 크롤링 - 조회수 조회
    view_num_list = []
    view_num_regexp = re.compile(r'조회수')
    for video in all_videos :
        view_num = video.find('span',{'class':'style-scope ytd-video-meta-block'})
        if view_num is not None :
            if view_num_regexp.search(view_num.text) :
                # view_num.text에 '조회수' 문자열이 있으면 True
                view_num_list.append(view_num.text)
        else : view_num_list.append(None)
        

    def nview(text) :
        view = text.replace('조회수','')
        num = float(view[:-2])
        danwee = view[-2:]

        if danwee == '만회':
            return int(num*10000)
        else:
            int(num*1000)
            
    view_number_type_list = []
    for view in view_num_list:
        if view is not None :
            view_number_type_list.append(nview(view))
        else : view_number_type_list.append(None)

    # 크롤링 --- 영상 url
    video_url_list = []
    for video in all_videos :
        video_url = 'http://www.youtube.com' + video.find('a',{'id':'thumbnail'})['href']
        if video_url is not None :
            video_url_list.append(video_url)
        else : video_url_list.append(None)

    # 크롤링 --- 영상 썸네일
    # video_thum_list = []
    # for video in all_videos :
    #     video_thum = video.find('a',{'id':'thumbnail'}).find('img')['src']
    #     if video_thum is not None :
    #         video_thum_list.append(video_thum)
    #     else : video_thum_list.append(None)
    
    # 영상 목록 페이지에서 가져온 각 영상의 url에 접근하여 영상의 좋아요, 싫어요, 댓글 수 가져오기

    # url에 접근하기
    comment_num_list = []
    like_num_list = []
    unlike_num_list = []
    video_tag_list = []
    for url in video_url_list :
        driver.get(url)
        body = driver.find_element_by_tag_name('body')

        # 브라우저 로딩시간 기다리기
        time.sleep(1)
        num_of_pagedowns = 2
        while num_of_pagedowns :
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
            num_of_pagedowns -= 1

        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')
        
        # 크롤링 --- 댓글 개수
        comment_num = soup.find('h2',{'id':'count'}).find('yt-formatted-string')
        if comment_num is not None :
            comment_num_list.append(comment_num.text)
        else : comment_num_list.append(None)

        # 크롤링 --- 좋아요 개수
        like_num = soup.find('yt-formatted-string',{'id':'text','class':'style-scope ytd-toggle-button-renderer style-text','aria-label':re.compile('좋아요')})
        if like_num is not None :
            like_num_list.append(like_num.text+'개')
        else : like_num_list.append(None)

        # 크롤링 --- 싫어요 개수
        unlike_num = soup.find('yt-formatted-string',{'id':'text','class':'style-scope ytd-toggle-button-renderer style-text','aria-label':re.compile('싫어요')})
        if unlike_num is not None :
            unlike_num_list.append(unlike_num.text+'개')
        else : unlike_num_list.append(None)

        # 크롤링 --- 태그
        video_tag = soup.find('yt-formatted-string',{'class':'super-title style-scope ytd-video-primary-info-renderer'},'a')
        if video_tag is not None :
            video_tag_list.append(video_tag.text)
        else : video_tag_list.append(None)


    # 리스트 길이 확인을 위한 코드
    print(comment_num_list)
    print(like_num_list)
    print(unlike_num_list)
    print(video_tag_list)
    print(len(title_list))
    print(len(video_time_list))
    print(len(view_num_list))
    print(len(view_number_type_list))
    print(len(video_url_list))
    print(len(comment_num_list))

    
    # 결과값을 넣을 데이터 프레임
    video_list = pd.DataFrame({
        'title' : title_list,
        'privious_time' : video_time_list,
        'view' : view_num_list,
        'video_url' : video_url_list,
        'comment' : comment_num_list,
        'like_num' : like_num_list,
        'unlike_num' : unlike_num_list,
        'tag' : video_tag_list
    })

    video_list.to_csv('video_list_test.csv')
    video_list

    return video_list
    

search_query = input('검색어를 입력하세요 : \n')
get_scraping_data(search_query)

