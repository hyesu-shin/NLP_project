from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd
import re

SCROLL_PAUSE_TIME = 0.5

driver = wd.Chrome("../chromedriver.exe")
url = "https://www.youtube.com/watch?v=9YlFFVisCBY"
driver.get(url)

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

page = driver.page_source
soup = BeautifulSoup(page, 'html.parser')

# 특정 url 제목, 좋아요, 싫어요 스크래핑
title = soup.find('yt-formatted-string',{'class':'style-scope ytd-video-primary-info-renderer'}).text
like = soup.find('yt-formatted-string',{'id':'text','class':'style-scope ytd-toggle-button-renderer style-text','aria-label':re.compile('좋아요')}).text
dislike = soup.find('yt-formatted-string',{'id':'text','class':'style-scope ytd-toggle-button-renderer style-text','aria-label':re.compile('싫어요')}).text

print(title)
print(like)
print(dislike)

# 특정 url 유튜브 댓글 스크래핑
all_comments = soup.find_all('ytd-comment-renderer',{'class':'style-scope ytd-comment-thread-renderer'})

comment_list = []
for comment in all_comments :

    if comment.find('yt-formatted-string',{'id':'content-text'},'span') :
        content = comment.find('yt-formatted-string',{'id':'content-text'},'span')
    else :
        content = comment.find('yt-formatted-string',{'id':'content-text'})

    if len(content.text.strip()) > 0 :
        comment_list.append(content.text)

# print(comment_list)
# print(len(comment_list))

user_list = []
for comment in all_comments :
    user = comment.find('a',{'id':'author-text'},'span')

    if len(user.text.strip()) > 0 :
        user_list.append(user.text.replace('\n','').replace(' ', ''))

like_list = []

for comment in all_comments :
    like = comment.find('span',{'id':'vote-count-left'})

    if len(like.text.strip()) > 0 :
        like_list.append(like.text.replace('\n','').replace(' ', ''))

dict_youtube_comment = {
    'user' : comment_list,
    'content' : user_list,
    'like' : like_list
}

youtube_comment = pd.DataFrame(dict_youtube_comment)
# print(youtube_comment)