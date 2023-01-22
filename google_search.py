import re
import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings() # 忽略https证书告警

# desktop user-agent
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"

site = ".cn" #设置地区
# query为搜索内容
query = f"inurl:php?id=8 and site:{site}"

# num为一次搜索的数量 #大于100后无效，只能爬取100个值，请自行优化
num = 150
query = query.replace(' ', '+')
URL = f"https://google.com/search?q={query}&num={num}"

headers = {"user-agent": USER_AGENT}
resp = requests.get(URL, headers=headers, verify=False)

results = []

if resp.status_code == 200:
    soup = BeautifulSoup(resp.content, "html.parser")
    for g in soup.find_all('div'): # <div>
        anchors = g.find_all('a')  # < a href="">

        if anchors:
            for i in range(len(anchors)):
                try:
                    link = anchors[i].attrs['href'] # 提取字典内容
                    # 正则过滤URL，删除掉一些乱码
                    if re.match('/', link) is None and re.match('(. *)google.com', link) is None and link != '#' and link.find('search?q') == -1:
                        if any(i.split(".site")[0] == link.split(".site")[0] for i in results):
                            link = ""
                        results.append(link)
                except Exception as e:
                    print("错误==>" + str(e))

# 写入文件
with open("urls.txt", "w") as f:
    for i in results:
        if i != "":
            f.write(i + "\n")

