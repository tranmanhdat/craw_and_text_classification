import requests
from bs4 import BeautifulSoup
import os
import time
import sys


root = sys.argv[1]
number_page =sys.argv[2]
os.makedirs(root, exist_ok=True)
f_log = open(root+"/craw.log", "w+", encoding="UTF-8")
website = "https://tuoitre.vn/"
response = requests.get(website)
# print(response)
# print(response.content)
soup = BeautifulSoup(response.content, "html.parser")
# print(soup)
titles = soup.findAll('li', class_='menu-li1')
links = [link.find('a').attrs["href"] for link in titles]
# print(links)
sub_links = []
scroll_links = []
for link in links:
    if link in ['/media.htm', '/gia-that.htm', '/ban-doc-lam-bao.htm']:
        continue
    if not link.__contains__("https"):
        link = website + link[1:]
        sub_links.append(link)
    else:
        scroll_links.append(link)
init_start = time.time()
for link in scroll_links:
    start = time.time()
    print("Crawling {}".format(link))
    f_log.write("Crawling {}\n".format(link))
    path_sub_folder = os.path.join(root, link.split(".")[0].split("/")[-1])
    os.makedirs(path_sub_folder, exist_ok=True)
    for i in range(1,int(number_page)):
        start_page = time.time()
        # path_page = os.path.join(path_sub_folder, str(i))
        path_page = path_sub_folder
        page_link = link + '/timeline/home-page-'+str(i)+'.htm'
        # print(link)
        response = requests.get(page_link)
        # print(response)
        # print(response.content)
        soup = BeautifulSoup(response.content, "html.parser")
        # print(soup)
        list_news_tag = soup.findAll('a', class_='img')
        # print(list_news_tag)
        # titles = list_news_tag[0].findAll('li', class_='news-item')
        links = [x.attrs["href"] for x in list_news_tag]
        for part_link in links:
            path_news = os.path.join(path_page, part_link[1:].split(".")[0])
            os.makedirs(path_news, exist_ok=True)
            full_link = link + part_link
            response = requests.get(full_link)
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
    end = time.time()
    print("\tTotal time crawl {} : {:.2f}".format(link[1:], end-start))
    f_log.write("\tTotal time crawl {} : {:.2f}\n".format(link[1:], end-start))
init_end = time.time()
print("\n\nTotal crawl time {:.2f}".format(init_end-init_start))
f_log.write("\n\nTotal crawl time {:.2f}".format(init_end-init_start))
f_log.close()