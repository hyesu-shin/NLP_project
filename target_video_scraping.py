from requests_html import HTMLSession
from bs4 import BeautifulSoup

# input url 넣기
url = ""
session = HTMLSession()
result = session.get(url)
result.html.render(sleep=1)

soup = BeautifulSoup(result.html.html, "html.parser")

# video title
result["title"] = soup.find("h1").text.strip()

# get the video tags
result["tags"] = ', '.join([ meta.attrs.get("content") for meta in soup.find_all("meta", {"property": "og:video:tag"}) ])

# number of likes
text_yt_formatted_strings = soup.find_all("yt-formatted-string", {"id": "text", "class": "ytd-toggle-button-renderer"})
result["likes"] = text_yt_formatted_strings[0].text

# number of dislikes
result["dislikes"] = text_yt_formatted_strings[1].text


