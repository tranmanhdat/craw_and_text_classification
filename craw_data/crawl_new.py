import requests
from bs4 import BeautifulSoup
import os
import time
import sys

# headers = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#             'Accept-Encoding': 'gzip, deflate, br',
#             'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
#             'Connection': 'keep-alive',
#             'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
#             'X-Requested-With': 'XMLHttpRequest'
# }
folder = ["thoi_su","the_gioi","phap_luat","kinh_doanh" ,"xe","nhip_song_tre", "van_hoa",
          "giai_tri", "giao_duc","khoa_hoc","suc_khoe"]
values = ["3","2","6","11","659","7","200017","10","13","661", "12"]
root = sys.argv[1]
number_page = sys.argv[2]
folder_index = int(sys.argv[3])
os.makedirs(root, exist_ok=True)
f_log = open(root+"/craw"+str(folder_index)+".log", "w+", encoding="UTF-8")
website = "https://tuoitre.vn/timeline/"
base_website = "https://tuoitre.vn"
init_start = time.time()
link = folder[folder_index]
value = values[folder_index]
start = time.time()
print("Crawling {}".format(link))
f_log.write("Crawling {}\n".format(link))
path_sub_folder = os.path.join(root, link)
os.makedirs(path_sub_folder, exist_ok=True)
i = 0
while i<int(number_page):
    start_page = time.time()
    # path_page = os.path.join(path_sub_folder, str(i))
    path_page = path_sub_folder
    page_link = website+value+ '/trang-'+str(i)+'.htm'
    while True:
        try:
            response = requests.get(page_link)
            break
        except:
            time.sleep(5)
            continue
    soup = BeautifulSoup(response.content, "html.parser")
    titles = soup.findAll('li', class_='news-item')
    links = [x.find('a').attrs["href"] for x in titles]
    for part_link in links:
        path_news = os.path.join(path_page, part_link[1:].split(".")[0])
        os.makedirs(path_news, exist_ok=True)
        if len(os.listdir(path_news)) >0:
            break
        full_link = base_website + part_link
        while True:
            try:
                response = requests.get(full_link)
            except:
                time.sleep(5)
                continue
        soup = BeautifulSoup(response.content, "html.parser")
        list_news_content = soup.findAll('div', class_='content fck')
        if len(list_news_content)==0:
            time.sleep(0.01)
            continue
        contents = list_news_content[0].findAll('p', class_=None)
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
init_end = time.time()
print("\n\nTotal crawl time {:.2f}".format(init_end-init_start))
f_log.write("\n\nTotal crawl time {:.2f}".format(init_end-init_start))
f_log.close()

# response = requests.get('https://tuoitre.vn/timeline/12/trang-102.htm')
# soup = BeautifulSoup(response.content, "html.parser")
# print(soup)
