from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json

url = 'https://www.youtube.com/@freecodecamp'
driver = webdriver.Chrome('chromedriver')
driver.get(url+'/videos')
time.sleep(5)
src = driver.page_source
soup = BeautifulSoup(src, 'html.parser')
urls = []

def scroll_screen():
    global urls
    urls = find_all_video_url()
    while len(urls) < total_video:
        scroll_height = 2000
        document_height_before = driver.execute_script("return document.documentElement.scrollHeight")
        driver.execute_script(f"window.scrollTo(0, {document_height_before+ scroll_height});")
        time.sleep(1.5)
        urls = find_all_video_url()
        print(len(urls))

def find_all_video_url():
    src = driver.page_source
    soup = BeautifulSoup(src, 'html.parser')
    videos = soup.find_all('a', {'id': 'thumbnail', 'class': 'ytd-thumbnail'}, href=True)
    urls = []
    for i in videos:
        urls.append('https://www.youtube.com'+i['href'])
    return urls

def find_video_content(urls,visited):
    driver.get(urls[visited])
    src = driver.page_source
    soup = BeautifulSoup(src, 'html.parser')
    video_url = soup.find("link", itemprop="url")['href']
    video_name = soup.find("meta", itemprop="name")['content']
    video_description = soup.find("meta", itemprop="description")['content']
    video_views = soup.find("meta", itemprop="interactionCount")['content']
    video_content = {
        "video_url": video_url,
        "video_name": video_name,
        "video_description": video_description,
        "video_views": video_views,
    }
    return video_content

contents = []
total_video = 45
visited = 0

scroll_screen()
while visited < total_video:
    video_content = find_video_content(urls, visited)
    contents.append(video_content)
    visited += 1

json_object = json.dumps(contents, indent=4)

with open("scrapData.json", "w") as outfile:
    outfile.write(json_object)

