import requests
import logging
import re
import json
from bs4 import BeautifulSoup
from os import makedirs
from os.path import exists
from urllib.parse import urljoin

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
BASE_URL = 'http://www.csres.com'
# 添加用户代理
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/ 537.36'
}

RESULTS_DIR = 'ans'
exists(RESULTS_DIR) or makedirs(RESULTS_DIR)

# 爬取网页，接收一个url，返回html
def scrape_page(url):
    logging.info('scraping %s...', url)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        elif response.status_code == 404:
          logging.warning('page not found (404) while scraping %s', url)
          return None
        else:
          logging.error('get invalid status code %s while scraping %s', response.status_code, url)
          return None
    except requests.RequestException:
        logging.error('error occurred while scraping %s', url, exc_info=True)
        return None

# 爬取各专业待爬页面，接收一个url，返回html
def scrape_url(url):
    url += '/sort/chsortdetail/P.html#P10/14'
    return scrape_page(url)

# 爬取各专业规范，接收一个url，返回html
def scrape_detail(url):
    return scrape_page(url)

# 解析html，得到各个专业待爬取页面url
def parse_url(html):
    pattern = re.compile('<a.*?href="(.*?)".*?class="sh14lian">')
    items = re.findall(pattern, html)
    if not items:
        return []
    for item in items:
        detail_url = urljoin(BASE_URL, item)
        logging.info('get profession url %s', detail_url)
        yield detail_url

# 解析html，返回规范数据[{id, name, department, published_at, status}]
def parse_detail(html):
    soup = BeautifulSoup(html, 'lxml')
    result = []

    for tr in soup.find(class_='heng').select('tr'):
        if tr.get('title') == None: continue
        # id = tr.select('font')[0].string.replace('\n', '').strip() if not tr.select('font')[0].string.isspace() else None
        # name = tr.select('font')[1].string.replace('\n', '').strip() if not tr.select('font')[1].string.isspace() else None
        # department = tr.select('font')[2].string.replace('\n', '').strip() if not tr.select('font')[2].string.isspace() else None
        # published_at = tr.select('font')[3].string.replace('\n', '').strip() if not tr.select('font')[3].string.isspace() else None
        # status = tr.select('font')[4].string.replace('\n', '').strip() if not tr.select('font')[4].string.isspace() else None
        id = (tr.select('font')[0].string or "").replace('\n', '').strip() or None
        name = (tr.select('font')[1].string or "").replace('\n', '').strip() or None
        department = (tr.select('font')[2].string or "").replace('\n', '').strip() or None
        published_at = (tr.select('font')[3].string or "").replace('\n', '').strip() or None
        status = (tr.select('font')[4].string or "").replace('\n', '').strip() or None
        result.append({
            'id': id,
            'name': name,
            'department': department,
            'published_at': published_at,
            'status': status,
        })
    return result
        
# 解析html，得到下一页待爬取url
def parse_index(html):
    pattern = re.compile('<a.*?href="(.*?)".*?class="lan">.*?下一页')
    items = re.findall(pattern, html)
    if not items:
        return []
    for item in items:
        detail_url = urljoin(BASE_URL, item)
        logging.info('get next url %s', detail_url)
        yield detail_url

# 自动爬取 输入分类 url 返回该分类下的所有结构化数据数组
def auto_scrape(url):
    data = []
    stack = [url]
    while stack:
        current_url = stack.pop()
        detail_html = scrape_detail(current_url)
        # 防止程序崩溃
        if(detail_html == None): break
        data.extend(parse_detail(detail_html))
        try:
            next_url = next(parse_index(current_url))
            stack.append(next_url)
        except StopIteration:
            logging.info('当前分类专业获取完毕')
    return data

# 保存到 ans 目录下的 data.json 文件
def save_data(data):
    with open('./ans/data.json', 'a', encoding='utf-8') as f:
      json.dump(data, f, ensure_ascii=False, indent=4)


def main():
    data = []
    # 得到待爬取专业汇总页面html
    html = scrape_url(BASE_URL)
    # 得到待爬取专业的url
    urls = parse_url(html)
    # 遍历每个大分类专业
    for url in urls:
        data.extend(auto_scrape(url))
    save_data(data)

if __name__ == '__main__':
    main()
