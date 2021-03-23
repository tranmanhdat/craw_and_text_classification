import requests
from bs4 import BeautifulSoup
import os
import time
import sys

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
}

root = sys.argv[1]
number_page =sys.argv[2]
os.makedirs(root, exist_ok=True)
f_log = open(root+"/craw.log", "w+", encoding="UTF-8")
link = "https://congnghe.tuoitre.vn/"
init_start = time.time()
start = time.time()
print("Crawling {}".format(link))
f_log.write("Crawling {}\n".format(link))
path_sub_folder = os.path.join(root, link.split(".")[0].split("/")[-1])
os.makedirs(path_sub_folder, exist_ok=True)
i = 0
while i<int(number_page):
    start_page = time.time()
    # path_page = os.path.join(path_sub_folder, str(i))
    path_page = path_sub_folder
    page_link = link + '/timeline/200029/trang-'+str(i)+'.htm'
    # print(link)
    response = requests.get(page_link, headers=headers)
    # print(response)
    # print(response.content)
    soup = BeautifulSoup(response.content, "html.parser")
    # print(soup)
    list_news_tag = soup.findAll('a', class_='img214x133 pos-rlt')
    # print(list_news_tag)
    # titles = list_news_tag[0].findAll('li', class_='news-item')
    links = [x.attrs["href"] for x in list_news_tag]
    for part_link in links:
        path_news = os.path.join(path_page, part_link[1:].split(".")[0])
        os.makedirs(path_news, exist_ok=True)
        if len(os.listdir(path_news))>0:
            print("\t\t\tPass crawled!")
            i = i + 100
        full_link = link + part_link
        response = requests.get(full_link, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        list_news_tag = soup.findAll('div', class_='content fck')
        if len(list_news_tag)==0:
            continue
        contents = list_news_tag[0].findAll('p', class_=None)
        id = 0
        for content in contents:
            path_file = os.path.join(path_news, str(id)+".txt")
            with open(path_file, "w+", encoding="UTF-8") as f_write:
                f_write.write(content.text)
            id = id + 1
    end_page = time.time()
    print("\tCrawled page {} in {:.2f}s".format(i, end_page-start_page))
    f_log.write("\tCrawled page {} in {:.2f}s\n".format(i, end_page-start_page))
    i = i + 1
end = time.time()
print("\tTotal time crawl {} : {:.2f}".format(link[1:], end-start))
f_log.write("\tTotal time crawl {} : {:.2f}\n".format(link[1:], end-start))

init_end = time.time()
print("\n\nTotal crawl time {:.2f}".format(init_end-init_start))
f_log.write("\n\nTotal crawl time {:.2f}".format(init_end-init_start))
f_log.close()