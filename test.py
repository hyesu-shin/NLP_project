import requests
from bs4 import BeautifulSoup

url = "https://www.youtube.com/watch?v=9YlFFVisCBY"
result = requests.get(url)

soup = BeautifulSoup(result.text, "html.parser")

# all_comments = soup.select('div#body > div#main')

# print(all_comments)
# comment_list = []
# for comment in all_comments :
#     content = comment.find(id='content')

#     if len(content.text.strip()) > 0 :
#         comment_list.appned(content)

# print(comment_list)
# print(len(comment_list))
youtube_user_IDs = soup.select('div#header-author > a > span')
youtube_comments = soup.select('yt-formatted-string#content-text')

str_youtube_userIDs = []
str_youtube_comments = []
for i in range(len(youtube_user_IDs)):
    str_tmp = str(youtube_user_IDs[i].text)
    # print(str_tmp) str_tmp = str_tmp.replace('\n', '')
    str_tmp = str_tmp.replace('\t', '')
    str_tmp = str_tmp.replace(' ','')
    str_youtube_userIDs.append(str_tmp)
    str_tmp = str(youtube_comments[i].text)
    str_tmp = str_tmp.replace('\n', '')
    str_tmp = str_tmp.replace('\t', '')
    str_tmp = str_tmp.replace(' ', '')
    str_youtube_comments.append(str_tmp)

for i in range(len(str_youtube_userIDs)):
    print(str_youtube_userIDs[i], str_youtube_comments[i])


