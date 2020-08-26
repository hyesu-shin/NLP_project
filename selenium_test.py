from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import re
import pandas as pd

# 한번 스크롤 하고 멈출 시간 설정
SCROLL_PAUSE_TIME = 0.5

driver = wd.Chrome("../chromedriver.exe")
url = "https://www.youtube.com/channel/UCyn-K7rZLXjGl7VXGweIlcA/videos"
driver.get(url)

# body태그를 선택하여 body에 넣기
body = driver.find_element_by_tag_name('body')

while True :
    # 현재 화면의 길이를 리턴 받아 last_height에 넣기
    last_height = driver.execute_script('return document.documentElement.scrollHeight')

    for i in range(10) :
        # body 본문에 END키를 입력(스크롤 내림)
        body.send_keys(Keys.END)
        time.sleep(SCROLL_PAUSE_TIME)

    new_height = driver.execute_script('return document.documentElement.scrollHeight')

    if new_height == last_height :
        break;

# BeautifulSoup 이용하여 소스 정리
page = driver.page_source
soup = BeautifulSoup(page, 'html.parser')

# 크롤링 --- 제목 조회
all_videos = soup.find_all(id='dismissable')

title_list = []
for video in all_videos :
    title = video.find(id='video-title')
    # 공백을 제거하고 글자수가 0보다 크면 append
    if len(title.text.strip())>0 :
        title_list.append(title.text)

# print(title_list)
# print(len(title_list))

# 크롤링 --- 재생 시간 조회

video_time_list = []
for video in all_videos :
    video_time = video.find('span', {'class' : 'style-scope ytd-thumbnail-overlay-time-status-renderer'})
    video_time_list.append(video_time.text.strip())

# print(video_time_list)
# print(len(video_time_list))

# video_time_list의 텍스트 데이터를 숫자(초)로 바꾸기

def stime(text) :
    time = text.split(':')
    if len(time) == 1:
        return int(time[0])
    elif len(time) == 2:
        return int(time[0])*60 + int(time[1])
    else:
        return int(time[0])*3600 + int(time[1]*60 + int(time[2]))

video_time_seperate_list = []
for time in video_time_list :
    video_time_seperate_list.append(stime(time))

# print(video_time_seperate_list)

# 크롤링 - 조회수 조회

view_num_list = []
view_num_regexp = re.compile(r'조회수')
for video in all_videos :
    view_num = video.find('span',{'class':'style-scope ytd-grid-video-renderer'})
    if view_num_regexp.search(view_num.text) :
        # view_num.text에 '조회수' 문자열이 있으면 True
        view_num_list.append(view_num.text)

# 조회수를 숫자로 저장할 리스트
# 단위가 '만회'가 아닌 경우에는 '천회'로 가정
# 조회수를 숫자로 변경하여 view_number_type_list 리스트에 저장
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
    view_number_type_list.append(nview(view))

# 데이터 프레임 생성
dict_youtube = {
    'title' : title_list,
    'video_time' : video_time_seperate_list,
    'video_num' : view_number_type_list
}

youtube = pd.DataFrame(dict_youtube)
print(youtube.head())

