import requests
import logging
import re
import json
import multiprocessing
from bs4 import BeautifulSoup
from os import makedirs
from os.path import exists
from urllib.parse import urljoin

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
BASE_URL = 'http://www.csres.com'
# 网站设置了反爬机制，添加用户代理
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
        logging.error('get invalid status code %s while scraping %s', response.status_code, url)
    except requests.RequestException:
        logging.error('error occurred while scraping %s', url, exc_info=True)

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
        id = tr.select('font')[0].string.replace('\n', '').strip() if not tr.select('font')[0].string.isspace() else None
        name = tr.select('font')[1].string.replace('\n', '').strip() if not tr.select('font')[1].string.isspace() else None
        department = tr.select('font')[2].string.replace('\n', '').strip() if not tr.select('font')[2].string.isspace() else None
        published_at = tr.select('font')[3].string.replace('\n', '').strip() if not tr.select('font')[3].string.isspace() else None
        status = tr.select('font')[4].string.replace('\n', '').strip() if not tr.select('font')[4].string.isspace() else None
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
    # 以下需要重新根据页面逻辑写，但是目前网站上不去 12/09
    pattern = re.compile('<a.*?href="(.*?)".*?class="sh14lian">')
    items = re.findall(pattern, html)
    if not items:
        return []
    for item in items:
        detail_url = urljoin(BASE_URL, item)
        logging.info('get profession url %s', detail_url)
        yield detail_url

def main():
    # 得到待爬取专业汇总页面html
    html = scrape_url(BASE_URL)
    # 得到待爬取专业的url
    urls = parse_url(html)
    # 遍历每个专业
    for url in urls:
        # 得到规范数据
        detail_html = scrape_detail(url)
        # 在这里存储？
        # 得到下一页url
        next_url = parse_index(detail_html)
        # 如果下一页不空，则继续爬取
        while(next_url):
          # 得到规范数据
          detail_html = scrape_detail(next_url)
          # 在这里存储？
          # 得到下一页url
          next_url = parse_index(detail_html)
    
    test = '''<html><head> 
<title>国家标准专业分类目录【P 工程建设】-工标网</title>
<link rel="shortcut icon" href="/images/gb.ico">
<meta http-equiv="Content-Type" content="text/html; charset=gbk">
<link href="/css/style.css" rel="stylesheet" type="text/css">
<meta name="description" content="中标分类 工程建设总目录">
<meta name="keywords" content="工程建设相关标准 工程建设标准 行业标准">
<script src="https://pagead2.googlesyndication.com/pagead/managed/js/adsense/m202412030101/show_ads_impl_fy2021.js"></script><script src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script><script language="javascript" src="/css/comm.js"></script>
<style data-id="immersive-translate-input-injected-css">.immersive-translate-input {
  position: absolute;
  top: 0;
  right: 0;
  left: 0;
  bottom: 0;
  z-index: 2147483647;
  display: flex;
  justify-content: center;
  align-items: center;
}
.immersive-translate-attach-loading::after {
  content: " ";

  --loading-color: #f78fb6;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  display: block;
  margin: 12px auto;
  position: relative;
  color: white;
  left: -100px;
  box-sizing: border-box;
  animation: immersiveTranslateShadowRolling 1.5s linear infinite;

  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-2000%, -50%);
  z-index: 100;
}

.immersive-translate-loading-spinner {
  vertical-align: middle !important;
  width: 10px !important;
  height: 10px !important;
  display: inline-block !important;
  margin: 0 4px !important;
  border: 2px rgba(221, 244, 255, 0.6) solid !important;
  border-top: 2px rgba(0, 0, 0, 0.375) solid !important;
  border-left: 2px rgba(0, 0, 0, 0.375) solid !important;
  border-radius: 50% !important;
  padding: 0 !important;
  -webkit-animation: immersive-translate-loading-animation 0.6s infinite linear !important;
  animation: immersive-translate-loading-animation 0.6s infinite linear !important;
}

@-webkit-keyframes immersive-translate-loading-animation {
  from {
    -webkit-transform: rotate(0deg);
  }

  to {
    -webkit-transform: rotate(359deg);
  }
}

@keyframes immersive-translate-loading-animation {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(359deg);
  }
}

.immersive-translate-input-loading {
  --loading-color: #f78fb6;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  display: block;
  margin: 12px auto;
  position: relative;
  color: white;
  left: -100px;
  box-sizing: border-box;
  animation: immersiveTranslateShadowRolling 1.5s linear infinite;
}

@keyframes immersiveTranslateShadowRolling {
  0% {
    box-shadow: 0px 0 rgba(255, 255, 255, 0), 0px 0 rgba(255, 255, 255, 0),
      0px 0 rgba(255, 255, 255, 0), 0px 0 rgba(255, 255, 255, 0);
  }

  12% {
    box-shadow: 100px 0 var(--loading-color), 0px 0 rgba(255, 255, 255, 0),
      0px 0 rgba(255, 255, 255, 0), 0px 0 rgba(255, 255, 255, 0);
  }

  25% {
    box-shadow: 110px 0 var(--loading-color), 100px 0 var(--loading-color),
      0px 0 rgba(255, 255, 255, 0), 0px 0 rgba(255, 255, 255, 0);
  }

  36% {
    box-shadow: 120px 0 var(--loading-color), 110px 0 var(--loading-color),
      100px 0 var(--loading-color), 0px 0 rgba(255, 255, 255, 0);
  }

  50% {
    box-shadow: 130px 0 var(--loading-color), 120px 0 var(--loading-color),
      110px 0 var(--loading-color), 100px 0 var(--loading-color);
  }

  62% {
    box-shadow: 200px 0 rgba(255, 255, 255, 0), 130px 0 var(--loading-color),
      120px 0 var(--loading-color), 110px 0 var(--loading-color);
  }

  75% {
    box-shadow: 200px 0 rgba(255, 255, 255, 0), 200px 0 rgba(255, 255, 255, 0),
      130px 0 var(--loading-color), 120px 0 var(--loading-color);
  }

  87% {
    box-shadow: 200px 0 rgba(255, 255, 255, 0), 200px 0 rgba(255, 255, 255, 0),
      200px 0 rgba(255, 255, 255, 0), 130px 0 var(--loading-color);
  }

  100% {
    box-shadow: 200px 0 rgba(255, 255, 255, 0), 200px 0 rgba(255, 255, 255, 0),
      200px 0 rgba(255, 255, 255, 0), 200px 0 rgba(255, 255, 255, 0);
  }
}

.immersive-translate-toast {
  display: flex;
  position: fixed;
  z-index: 2147483647;
  left: 0;
  right: 0;
  top: 1%;
  width: fit-content;
  padding: 12px 20px;
  margin: auto;
  overflow: auto;
  background: #fef6f9;
  box-shadow: 0px 4px 10px 0px rgba(0, 10, 30, 0.06);
  font-size: 15px;
  border-radius: 8px;
  color: #333;
}

.immersive-translate-toast-content {
  display: flex;
  flex-direction: row;
  align-items: center;
}

.immersive-translate-toast-hidden {
  margin: 0 20px 0 72px;
  text-decoration: underline;
  cursor: pointer;
}

.immersive-translate-toast-close {
  color: #666666;
  font-size: 20px;
  font-weight: bold;
  padding: 0 10px;
  cursor: pointer;
}

@media screen and (max-width: 768px) {
  .immersive-translate-toast {
    top: 0;
    padding: 12px 0px 0 10px;
  }
  .immersive-translate-toast-content {
    flex-direction: column;
    text-align: center;
  }
  .immersive-translate-toast-hidden {
    margin: 10px auto;
  }
}

.immersive-translate-modal {
  display: none;
  position: fixed;
  z-index: 2147483647;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgb(0, 0, 0);
  background-color: rgba(0, 0, 0, 0.4);
  font-size: 15px;
}

.immersive-translate-modal-content {
  background-color: #fefefe;
  margin: 10% auto;
  padding: 40px 24px 24px;
  border: 1px solid #888;
  border-radius: 10px;
  width: 80%;
  max-width: 270px;
  font-family: system-ui, -apple-system, "Segoe UI", "Roboto", "Ubuntu",
    "Cantarell", "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji",
    "Segoe UI Symbol", "Noto Color Emoji";
  position: relative;
}

@media screen and (max-width: 768px) {
  .immersive-translate-modal-content {
    margin: 50% auto !important;
  }
}

.immersive-translate-modal .immersive-translate-modal-content-in-input {
  max-width: 500px;
}
.immersive-translate-modal-content-in-input .immersive-translate-modal-body {
  text-align: left;
  max-height: unset;
}

.immersive-translate-modal-title {
  text-align: center;
  font-size: 16px;
  font-weight: 700;
  color: #333333;
}

.immersive-translate-modal-body {
  text-align: center;
  font-size: 14px;
  font-weight: 400;
  color: #333333;
  word-break: break-all;
  margin-top: 24px;
}

@media screen and (max-width: 768px) {
  .immersive-translate-modal-body {
    max-height: 250px;
    overflow-y: auto;
  }
}

.immersive-translate-close {
  color: #666666;
  position: absolute;
  right: 16px;
  top: 16px;
  font-size: 20px;
  font-weight: bold;
}

.immersive-translate-close:hover,
.immersive-translate-close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

.immersive-translate-modal-footer {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  margin-top: 24px;
}

.immersive-translate-btn {
  width: fit-content;
  color: #fff;
  background-color: #ea4c89;
  border: none;
  font-size: 16px;
  margin: 0 8px;
  padding: 9px 30px;
  border-radius: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.immersive-translate-btn:hover {
  background-color: #f082ac;
}
.immersive-translate-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.immersive-translate-btn:disabled:hover {
  background-color: #ea4c89;
}

.immersive-translate-cancel-btn {
  /* gray color */
  background-color: rgb(89, 107, 120);
}

.immersive-translate-cancel-btn:hover {
  background-color: hsl(205, 20%, 32%);
}

.immersive-translate-action-btn {
  background-color: transparent;
  color: #ea4c89;
  border: 1px solid #ea4c89;
}

.immersive-translate-btn svg {
  margin-right: 5px;
}

.immersive-translate-link {
  cursor: pointer;
  user-select: none;
  -webkit-user-drag: none;
  text-decoration: none;
  color: #007bff;
  -webkit-tap-highlight-color: rgba(0, 0, 0, 0.1);
}

.immersive-translate-primary-link {
  cursor: pointer;
  user-select: none;
  -webkit-user-drag: none;
  text-decoration: none;
  color: #ea4c89;
  -webkit-tap-highlight-color: rgba(0, 0, 0, 0.1);
}

.immersive-translate-modal input[type="radio"] {
  margin: 0 6px;
  cursor: pointer;
}

.immersive-translate-modal label {
  cursor: pointer;
}

.immersive-translate-close-action {
  position: absolute;
  top: 2px;
  right: 0px;
  cursor: pointer;
}

.imt-image-status {
  background-color: rgba(0, 0, 0, 0.5) !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
  border-radius: 16px !important;
}
.imt-image-status img,
.imt-image-status svg,
.imt-img-loading {
  width: 28px !important;
  height: 28px !important;
  margin: 0 0 8px 0 !important;
  min-height: 28px !important;
  min-width: 28px !important;
  position: relative !important;
}
.imt-img-loading {
  background-image: url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADgAAAA4CAMAAACfWMssAAAAtFBMVEUAAAD////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////oK74hAAAAPHRSTlMABBMIDyQXHwyBfFdDMSw+OjXCb+5RG51IvV/k0rOqlGRM6KKMhdvNyZBz9MaupmxpWyj437iYd/yJVNZeuUC7AAACt0lEQVRIx53T2XKiUBCA4QYOiyCbiAsuuGBcYtxiYtT3f6/pbqoYHVFO5r+iivpo6DpAWYpqeoFfr9f90DsYAuRSWkFnPO50OgR9PwiCUFcl2GEcx+N/YBh6pvKaefHlUgZd1zVe0NbYcQjGBfzrPE8Xz8aF+71D8gG6DHFPpc4a7xFiCDuhaWgKgGIJQ3d5IMGDrpS4S5KgpIm+en9f6PlAhKby4JwEIxlYJV9h5k5nee9GoxHJ2IDSNB0dwdad1NAxDJ/uXDHYmebdk4PdbkS58CIVHdYSUHTYYRWOJblWSyu2lmy3KNFVJNBhxcuGW4YBVCbYGRZwIooipHsNqjM4FbgOQqQqSKQQU9V8xmi1QlgHqQQ6DDBvRUVCDirs+EzGDGOQTCATgtYTnbCVLgsVgRE0T1QE0qHCFAht2z6dLvJQs3Lo2FQoDxWNUiBhaP4eRgwNkI+dAjVOA/kUrIDwf3CG8NfNOE0eiFotSuo+rBiq8tD9oY4Qzc6YJw99hl1wzpQvD7ef2M8QgnOGJfJw+EltQc+oX2yn907QB22WZcvlUpd143dqQu+8pCJZuGE4xCuPXJqqcs5sNpsI93Rmzym1k4Npk+oD1SH3/a3LOK/JpUBpWfqNySxWzCfNCUITuDG5dtuphrUJ1myeIE9bIsPiKrfqTai5WZxbhtNphYx6GEIHihyGFTI69lje/rxajdh0s0msZ0zYxyPLhYCb1CyHm9Qsd2H37Y3lugVwL9kNh8Ot8cha6fUNQ8nuXi5z9/ExsAO4zQrb/ev1yrCB7lGyQzgYDGuxq1toDN/JGvN+HyWNHKB7zEoK+PX11e12G431erGYzwmytAWU56fkMHY5JJnDRR2eZji3AwtIcrEV8Cojat/BdQ7XOwGV1e1hDjGGjXbdArm8uJZtCH5MbcctVX8A1WpqumJHwckAAAAASUVORK5CYII=");
  background-size: 28px 28px;
  animation: image-loading-rotate 1s linear infinite !important;
}

.imt-image-status span {
  color: var(--bg-2, #fff) !important;
  font-size: 14px !important;
  line-height: 14px !important;
  font-weight: 500 !important;
  font-family: "PingFang SC", Arial, sans-serif !important;
}

@keyframes image-loading-rotate {
  from {
    transform: rotate(360deg);
  }
  to {
    transform: rotate(0deg);
  }
}
</style><meta http-equiv="origin-trial" content="AlK2UR5SkAlj8jjdEc9p3F3xuFYlF6LYjAML3EOqw1g26eCwWPjdmecULvBH5MVPoqKYrOfPhYVL71xAXI1IBQoAAAB8eyJvcmlnaW4iOiJodHRwczovL2RvdWJsZWNsaWNrLm5ldDo0NDMiLCJmZWF0dXJlIjoiV2ViVmlld1hSZXF1ZXN0ZWRXaXRoRGVwcmVjYXRpb24iLCJleHBpcnkiOjE3NTgwNjcxOTksImlzU3ViZG9tYWluIjp0cnVlfQ=="><meta http-equiv="origin-trial" content="Amm8/NmvvQfhwCib6I7ZsmUxiSCfOxWxHayJwyU1r3gRIItzr7bNQid6O8ZYaE1GSQTa69WwhPC9flq/oYkRBwsAAACCeyJvcmlnaW4iOiJodHRwczovL2dvb2dsZXN5bmRpY2F0aW9uLmNvbTo0NDMiLCJmZWF0dXJlIjoiV2ViVmlld1hSZXF1ZXN0ZWRXaXRoRGVwcmVjYXRpb24iLCJleHBpcnkiOjE3NTgwNjcxOTksImlzU3ViZG9tYWluIjp0cnVlfQ=="><meta http-equiv="origin-trial" content="A9wSqI5i0iwGdf6L1CERNdmsTPgVu44ewj8QxTBYgsv1LCPUVF7YmWOvTappqB1139jAymxUW/RO8zmMqo4zlAAAAACNeyJvcmlnaW4iOiJodHRwczovL2RvdWJsZWNsaWNrLm5ldDo0NDMiLCJmZWF0dXJlIjoiRmxlZGdlQmlkZGluZ0FuZEF1Y3Rpb25TZXJ2ZXIiLCJleHBpcnkiOjE3MzY4MTI4MDAsImlzU3ViZG9tYWluIjp0cnVlLCJpc1RoaXJkUGFydHkiOnRydWV9"><meta http-equiv="origin-trial" content="A+d7vJfYtay4OUbdtRPZA3y7bKQLsxaMEPmxgfhBGqKXNrdkCQeJlUwqa6EBbSfjwFtJWTrWIioXeMW+y8bWAgQAAACTeyJvcmlnaW4iOiJodHRwczovL2dvb2dsZXN5bmRpY2F0aW9uLmNvbTo0NDMiLCJmZWF0dXJlIjoiRmxlZGdlQmlkZGluZ0FuZEF1Y3Rpb25TZXJ2ZXIiLCJleHBpcnkiOjE3MzY4MTI4MDAsImlzU3ViZG9tYWluIjp0cnVlLCJpc1RoaXJkUGFydHkiOnRydWV9"></head>

<body><table width="100%" border="0" cellspacing="0" cellpadding="0" align="center">
  <form method="get" action="/s.jsp" name="form_Search" onsubmit="return dofind()"></form>
   <tbody><tr> 
      <td align="center">

<table width="100%" border="0" cellpadding="0" cellspacing="0">
  <tbody><tr>
    <td width="215" align="left" valign="top">&nbsp;<a href="/"></a><a href="/"><img src="/images/ny_logo.gif" alt="工标网 回首页" border="0"></a></td>
<td width="550" align="left"><table width="510" border="0" cellspacing="0" cellpadding="0">
<tbody><tr>
					  <td width="68%"><a href="/sort/index.jsp" class="slan13">标准分类</a>&nbsp; <a href="/new/index.jsp" class="slan13">最新标准</a><sup><span style="font-size: 11pt"><font color="red">New!</font></span></sup>&nbsp; <a href="/notice/index.jsp" class="slan13">标准公告</a> <a href="/info/index.jsp" class="slan13">标准动态</a>&nbsp; <a href="/bbs/index.jsp" class="slan13">标准论坛</a></td>
				  </tr>
				  <tr>
					<td><input name="keyword" type="text" size="49" value="">
         					 <input name="submit12" type="submit" value="标准搜索">&nbsp;<a href="/advanced/index.jsp" class="slan13">高级查询</a></td>
		  </tr>
				</tbody></table>
   </td>
       <td width="681" align="right"><table width="250" border="0" cellspacing="0" cellpadding="0">
			  <tbody><tr>
				<td align="center"><a href="/sys/help.htm" target="_blank" class="slan13">帮助</a> |  <a href="/user/logon.jsp" class="slan13">登录</a> | <a href="/user/register.jsp" class="slan13">注册</a></td>
			  </tr>
			  <tr>
				<td align="center"><img src="/images/adci.gif" alt="查标准上工标网 免费查询标准最新替代作废信息" width="228" height="21"></td>
	     </tr>
			</tbody></table>
  </td>
  </tr>
</tbody></table>
<table width="100%" border="0" cellpadding="0" cellspacing="0">
  <tbody><tr>
    <td height="27" valign="top" background="/images/ny_bg.gif" bgcolor="#a1b3d4"><table cellspacing="0" cellpadding="0" width="100%" border="0">
        <tbody>
        <tr valign="center">
          <td width="75%" height="27" align="left" valign="center" class="crumbTrail"><span class="bai12xi">&nbsp;您的位置:<a href="/" class="bai12xiL">工标网</a> &gt;&gt; <a href="/sort" class="bai12xiL">标准分类</a> &gt;&gt; <a href="/sort/chsort.jsp" class="bai12xiL">中标分类</a> &gt;&gt; P 工程建设</span></td>
          <td width="25%" height="22" align="right" valign="center" class="helpLink">
            <span class="bai12cu"><a href="javascript:window.external.AddFavorite('http://www.csres.com','工业标准咨询网')" class="bai12" title="收藏本站，下次需要查标准时候就来工标网">收藏本站</a></span> &nbsp;<a href="/service/web.htm" target="_blank" title="点击联系在线客服，有什么问题我们帮您解决！！" class="bai12">联系客服</a>&nbsp;</td>
        </tr></tbody></table></td>
  </tr>
</tbody></table>
		
</td>
    </tr>
    <tr> 
      <td align="center">
	  <table width="99%" border="0" cellpadding="8" cellspacing="0">
  <tbody><tr>
    <td width="100%" align="center" valign="top"><table width="97%" border="0">
      <tbody><tr>
        <td>&nbsp;</td>
      </tr>
   
      <tr>
        <td height="32" class="ny_bg" colspan="3"><a name="P00/09"> <font style="font-size:14px; color:04048D"><strong>P00/09&nbsp;工程建设综合</strong></font></a></td>
      </tr>
	  
      <tr>
        <td height="32"><a name="P00"></a><a href="/sort/Chtype/P00_1.html" class="sh14lian">P00&nbsp;标准化、质量管理<font color="red">[18]</font></a></td>
		
        <td height="32"><a name="P01"></a><a href="/sort/Chtype/P01_1.html" class="sh14lian">P01&nbsp;技术管理<font color="red">[109]</font></a></td>
		
        <td height="32"><a name="P02"></a><a href="/sort/Chtype/P02_1.html" class="sh14lian">P02&nbsp;经济管理<font color="red">[30]</font></a></td>
      </tr>
	  
      <tr>
        <td height="32"><a name="P04"></a><a href="/sort/Chtype/P04_1.html" class="sh14lian">P04&nbsp;基础标准与通用方法<font color="red">[57]</font></a></td>
		
        <td height="32"><a name="P07"></a><a href="/sort/Chtype/P07_1.html" class="sh14lian">P07&nbsp;电子计算机应用<font color="red">[12]</font></a></td>
		
        <td height="32"><a name="P09"></a><a href="/sort/Chtype/P09_1.html" class="sh14lian">P09&nbsp;卫生、安全、劳动保护<font color="red">[50]</font></a></td>
      </tr>
  
      <tr>
        <td height="32" class="ny_bg" colspan="3"><a name="P10/14"> <font style="font-size:14px; color:04048D"><strong>P10/14&nbsp;工程勘察与岩土工程</strong></font></a></td>
      </tr>
	  
      <tr>
        <td height="32"><a name="P10"></a><a href="/sort/Chtype/P10_1.html" class="sh14lian">P10&nbsp;工程勘察与岩土工程综合<font color="red">[26]</font></a></td>
		
        <td height="32"><a name="P11"></a><a href="/sort/Chtype/P11_1.html" class="sh14lian">P11&nbsp;工程测量<font color="red">[13]</font></a></td>
		
        <td height="32"><a name="P12"></a><a href="/sort/Chtype/P12_1.html" class="sh14lian">P12&nbsp;工程水文<font color="red">[24]</font></a></td>
      </tr>
	  
      <tr>
        <td height="32"><a name="P13"></a><a href="/sort/Chtype/P13_1.html" class="sh14lian">P13&nbsp;工程地址、水文地质勘察与岩土工程<font color="red">[190]</font></a></td>
		
        <td height="32"><a name="P14"></a><a href="/sort/Chtype/P14_1.html" class="sh14lian">P14&nbsp;工程物探与遥感勘探<font color="red">[9]</font></a></td>
		
        <td height="32"><a name="P14"></a><a href="/sort/Chtype/_1.html" class="sh14lian">&nbsp;</a></td>
      </tr>
  
      <tr>
        <td height="32" class="ny_bg" colspan="3"><a name="P15/19"> <font style="font-size:14px; color:04048D"><strong>P15/19&nbsp;工程抗震、工程防火、人防工程</strong></font></a></td>
      </tr>
	  
      <tr>
        <td height="32"><a name="P15"></a><a href="/sort/Chtype/P15_1.html" class="sh14lian">P15&nbsp;工程抗震<font color="red">[90]</font></a></td>
		
        <td height="32"><a name="P16"></a><a href="/sort/Chtype/P16_1.html" class="sh14lian">P16&nbsp;工程防火<font color="red">[68]</font></a></td>
		
        <td height="32"><a name="P18"></a><a href="/sort/Chtype/P18_1.html" class="sh14lian">P18&nbsp;人防工程<font color="red">[17]</font></a></td>
      </tr>
  
      <tr>
        <td height="32" class="ny_bg" colspan="3"><a name="P20/29"> <font style="font-size:14px; color:04048D"><strong>P20/29&nbsp;工程结构</strong></font></a></td>
      </tr>
	  
      <tr>
        <td height="32"><a name="P20"></a><a href="/sort/Chtype/P20_1.html" class="sh14lian">P20&nbsp;工程结构综合<font color="red">[31]</font></a></td>
		
        <td height="32"><a name="P21"></a><a href="/sort/Chtype/P21_1.html" class="sh14lian">P21&nbsp;土石方、隧道工程<font color="red">[20]</font></a></td>
		
        <td height="32"><a name="P22"></a><a href="/sort/Chtype/P22_1.html" class="sh14lian">P22&nbsp;地基、基础工程<font color="red">[64]</font></a></td>
      </tr>
	  
      <tr>
        <td height="32"><a name="P23"></a><a href="/sort/Chtype/P23_1.html" class="sh14lian">P23&nbsp;木结构工程<font color="red">[7]</font></a></td>
		
        <td height="32"><a name="P24"></a><a href="/sort/Chtype/P24_1.html" class="sh14lian">P24&nbsp;砌体结构工程<font color="red">[36]</font></a></td>
		
        <td height="32"><a name="P25"></a><a href="/sort/Chtype/P25_1.html" class="sh14lian">P25&nbsp;混凝土结构工程<font color="red">[133]</font></a></td>
      </tr>
	  
      <tr>
        <td height="32"><a name="P26"></a><a href="/sort/Chtype/P26_1.html" class="sh14lian">P26&nbsp;金属结构工程<font color="red">[55]</font></a></td>
		
        <td height="32"><a name="P27"></a><a href="/sort/Chtype/P27_1.html" class="sh14lian">P27&nbsp;组合结构工程<font color="red">[10]</font></a></td>
		
        <td height="32"><a name="P28"></a><a href="/sort/Chtype/P28_1.html" class="sh14lian">P28&nbsp;桥涵工程<font color="red">[105]</font></a></td>
      </tr>
  
      <tr>
        <td height="32" class="ny_bg" colspan="3"><a name="P30/39"> <font style="font-size:14px; color:04048D"><strong>P30/39&nbsp;工业与民用建筑工程</strong></font></a></td>
      </tr>
	  
      <tr>
        <td height="32"><a name="P30"></a><a href="/sort/Chtype/P30_1.html" class="sh14lian">P30&nbsp;工业与名用建筑工程综合<font color="red">[48]</font></a></td>
		
        <td height="32"><a name="P31"></a><a href="/sort/Chtype/P31_1.html" class="sh14lian">P31&nbsp;建筑物理<font color="red">[61]</font></a></td>
		
        <td height="32"><a name="P32"></a><a href="/sort/Chtype/P32_1.html" class="sh14lian">P32&nbsp;建筑构造与装饰工程<font color="red">[160]</font></a></td>
      </tr>
	  
      <tr>
        <td height="32"><a name="P33"></a><a href="/sort/Chtype/P33_1.html" class="sh14lian">P33&nbsp;居住与公共建筑工程<font color="red">[148]</font></a></td>
		
        <td height="32"><a name="P34"></a><a href="/sort/Chtype/P34_1.html" class="sh14lian">P34&nbsp;工业建筑工程<font color="red">[113]</font></a></td>
		
        <td height="32"><a name="P35"></a><a href="/sort/Chtype/P35_1.html" class="sh14lian">P35&nbsp;农林牧渔业建筑工程<font color="red">[11]</font></a></td>
      </tr>
	  
      <tr>
        <td height="32"><a name="P36"></a><a href="/sort/Chtype/P36_1.html" class="sh14lian">P36&nbsp;建筑维修工程<font color="red">[16]</font></a></td>
		
        <td height="32"><a name="P36"></a><a href="/sort/Chtype/_1.html" class="sh14lian">&nbsp;</a></td>
		
        <td height="32"><a name="P36"></a><a href="/sort/Chtype/_1.html" class="sh14lian">&nbsp;</a></td>
      </tr>
  
      <tr>
        <td height="32" class="ny_bg" colspan="3"><a name="P40/44"> <font style="font-size:14px; color:04048D"><strong>P40/44&nbsp;给水、排水工程</strong></font></a></td>
      </tr>
	  
      <tr>
        <td height="32"><a name="P40"></a><a href="/sort/Chtype/P40_1.html" class="sh14lian">P40&nbsp;给水、排水工程综合<font color="red">[121]</font></a></td>
		
        <td height="32"><a name="P41"></a><a href="/sort/Chtype/P41_1.html" class="sh14lian">P41&nbsp;室外给水、排水工程<font color="red">[86]</font></a></td>
		
        <td height="32"><a name="P42"></a><a href="/sort/Chtype/P42_1.html" class="sh14lian">P42&nbsp;建筑给水、排水工程<font color="red">[51]</font></a></td>
      </tr>
  
      <tr>
        <td height="32" class="ny_bg" colspan="3"><a name="P45/49"> <font style="font-size:14px; color:04048D"><strong>P45/49&nbsp;供热、供气、空调及制冷工程</strong></font></a></td>
      </tr>
	  
      <tr>
        <td height="32"><a name="P45"></a><a href="/sort/Chtype/P45_1.html" class="sh14lian">P45&nbsp;供热、供气、空调及制冷工程综合<font color="red">[31]</font></a></td>
		
        <td height="32"><a name="P46"></a><a href="/sort/Chtype/P46_1.html" class="sh14lian">P46&nbsp;供热、采暖工程<font color="red">[28]</font></a></td>
		
        <td height="32"><a name="P47"></a><a href="/sort/Chtype/P47_1.html" class="sh14lian">P47&nbsp;供气工程<font color="red">[53]</font></a></td>
      </tr>
	  
      <tr>
        <td height="32"><a name="P48"></a><a href="/sort/Chtype/P48_1.html" class="sh14lian">P48&nbsp;通风、空调工程<font color="red">[30]</font></a></td>
		
        <td height="32"><a name="P49"></a><a href="/sort/Chtype/P49_1.html" class="sh14lian">P49&nbsp;制冷工程<font color="red">[3]</font></a></td>
		
        <td height="32"><a name="P49"></a><a href="/sort/Chtype/_1.html" class="sh14lian">&nbsp;</a></td>
      </tr>
  
      <tr>
        <td height="32" class="ny_bg" colspan="3"><a name="P50/54"> <font style="font-size:14px; color:04048D"><strong>P50/54&nbsp;城乡规划与市政工程</strong></font></a></td>
      </tr>
	  
      <tr>
        <td height="32"><a name="P50"></a><a href="/sort/Chtype/P50_1.html" class="sh14lian">P50&nbsp;城乡规划<font color="red">[27]</font></a></td>
		
        <td height="32"><a name="P51"></a><a href="/sort/Chtype/P51_1.html" class="sh14lian">P51&nbsp;城市交通工程<font color="red">[47]</font></a></td>
		
        <td height="32"><a name="P52"></a><a href="/sort/Chtype/P52_1.html" class="sh14lian">P52&nbsp;索道工程<font color="red">[20]</font></a></td>
      </tr>
	  
      <tr>
        <td height="32"><a name="P53"></a><a href="/sort/Chtype/P53_1.html" class="sh14lian">P53&nbsp;园林绿化与市容卫生<font color="red">[61]</font></a></td>
		
        <td height="32"><a name="P53"></a><a href="/sort/Chtype/_1.html" class="sh14lian">&nbsp;</a></td>
		
        <td height="32"><a name="P53"></a><a href="/sort/Chtype/_1.html" class="sh14lian">&nbsp;</a></td>
      </tr>
  
      <tr>
        <td height="32" class="ny_bg" colspan="3"><a name="P55/59"> <font style="font-size:14px; color:04048D"><strong>P55/59&nbsp;水利、水电工程</strong></font></a></td>
      </tr>
	  
      <tr>
        <td height="32"><a name="P55"></a><a href="/sort/Chtype/P55_1.html" class="sh14lian">P55&nbsp;水利、水电工程综合<font color="red">[159]</font></a></td>
		
        <td height="32"><a name="P56"></a><a href="/sort/Chtype/P56_1.html" class="sh14lian">P56&nbsp;流域规划与江河整治工程<font color="red">[15]</font></a></td>
		
        <td height="32"><a name="P57"></a><a href="/sort/Chtype/P57_1.html" class="sh14lian">P57&nbsp;灌溉排水与水土保持工程<font color="red">[52]</font></a></td>
      </tr>
	  
      <tr>
        <td height="32"><a name="P58"></a><a href="/sort/Chtype/P58_1.html" class="sh14lian">P58&nbsp;防洪、排涝工程<font color="red">[13]</font></a></td>
		
        <td height="32"><a name="P59"></a><a href="/sort/Chtype/P59_1.html" class="sh14lian">P59&nbsp;水电工程<font color="red">[222]</font></a></td>
		
        <td height="32"><a name="P59"></a><a href="/sort/Chtype/_1.html" class="sh14lian">&nbsp;</a></td>
      </tr>
  
      <tr>
        <td height="32" class="ny_bg" colspan="3"><a name="P60/64"> <font style="font-size:14px; color:04048D"><strong>P60/64&nbsp;电力、核工业工程</strong></font></a></td>
      </tr>
	  
      <tr>
        <td height="32"><a name="P60"></a><a href="/sort/Chtype/P60_1.html" class="sh14lian">P60&nbsp;电力工程综合<font color="red">[41]</font></a></td>
		
        <td height="32"><a name="P61"></a><a href="/sort/Chtype/P61_1.html" class="sh14lian">P61&nbsp;发电站工程<font color="red">[121]</font></a></td>
		
        <td height="32"><a name="P62"></a><a href="/sort/Chtype/P62_1.html" class="sh14lian">P62&nbsp;输、变电工程<font color="red">[76]</font></a></td>
      </tr>
	  
      <tr>
        <td height="32"><a name="P63"></a><a href="/sort/Chtype/P63_1.html" class="sh14lian">P63&nbsp;供、配电工程<font color="red">[45]</font></a></td>
		
        <td height="32"><a name="P64"></a><a href="/sort/Chtype/P64_1.html" class="sh14lian">P64&nbsp;核工业工程<font color="red">[4]</font></a></td>
		
        <td height="32"><a name="P64"></a><a href="/sort/Chtype/_1.html" class="sh14lian">&nbsp;</a></td>
      </tr>
  
      <tr>
        <td height="32" class="ny_bg" colspan="3"><a name="P65/69"> <font style="font-size:14px; color:04048D"><strong>P65/69&nbsp;交通运输工程</strong></font></a></td>
      </tr>
	  
      <tr>
        <td height="32"><a name="P65"></a><a href="/sort/Chtype/P65_1.html" class="sh14lian">P65&nbsp;铁路工程<font color="red">[123]</font></a></td>
		
        <td height="32"><a name="P66"></a><a href="/sort/Chtype/P66_1.html" class="sh14lian">P66&nbsp;公路工程<font color="red">[194]</font></a></td>
		
        <td height="32"><a name="P67"></a><a href="/sort/Chtype/P67_1.html" class="sh14lian">P67&nbsp;港口与航道工程<font color="red">[124]</font></a></td>
      </tr>
	  
      <tr>
        <td height="32"><a name="P68"></a><a href="/sort/Chtype/P68_1.html" class="sh14lian">P68&nbsp;航空、航天工程<font color="red">[2]</font></a></td>
		
        <td height="32"><a name="P68"></a><a href="/sort/Chtype/_1.html" class="sh14lian">&nbsp;</a></td>
		
        <td height="32"><a name="P68"></a><a href="/sort/Chtype/_1.html" class="sh14lian">&nbsp;</a></td>
      </tr>
  
      <tr>
        <td height="32" class="ny_bg" colspan="3"><a name="P70/79"> <font style="font-size:14px; color:04048D"><strong>P70/79&nbsp;原材料工业及通信、广播工程</strong></font></a></td>
      </tr>
	  
      <tr>
        <td height="32"><a name="P70"></a><a href="/sort/Chtype/P70_1.html" class="sh14lian">P70&nbsp;矿山、煤炭工程<font color="red">[41]</font></a></td>
		
        <td height="32"><a name="P71"></a><a href="/sort/Chtype/P71_1.html" class="sh14lian">P71&nbsp;石油工程<font color="red">[103]</font></a></td>
		
        <td height="32"><a name="P72"></a><a href="/sort/Chtype/P72_1.html" class="sh14lian">P72&nbsp;石化、化工工程<font color="red">[358]</font></a></td>
      </tr>
	  
      <tr>
        <td height="32"><a name="P73"></a><a href="/sort/Chtype/P73_1.html" class="sh14lian">P73&nbsp;冶金工业工程<font color="red">[11]</font></a></td>
		
        <td height="32"><a name="P74"></a><a href="/sort/Chtype/P74_1.html" class="sh14lian">P74&nbsp;建筑材料工业工程<font color="red">[3]</font></a></td>
		
        <td height="32"><a name="P75"></a><a href="/sort/Chtype/P75_1.html" class="sh14lian">P75&nbsp;林产工业工程<font color="red">[0]</font></a></td>
      </tr>
	  
      <tr>
        <td height="32"><a name="P76"></a><a href="/sort/Chtype/P76_1.html" class="sh14lian">P76&nbsp;通信工程<font color="red">[98]</font></a></td>
		
        <td height="32"><a name="P77"></a><a href="/sort/Chtype/P77_1.html" class="sh14lian">P77&nbsp;广播、电影、电视工程<font color="red">[82]</font></a></td>
		
        <td height="32"><a name="P77"></a><a href="/sort/Chtype/_1.html" class="sh14lian">&nbsp;</a></td>
      </tr>
  
      <tr>
        <td height="32" class="ny_bg" colspan="3"><a name="P80/84"> <font style="font-size:14px; color:04048D"><strong>P80/84&nbsp;机电制造业工程</strong></font></a></td>
      </tr>
	  
      <tr>
        <td height="32"><a name="P80"></a><a href="/sort/Chtype/P80_1.html" class="sh14lian">P80&nbsp;机械、仪表制造业工程<font color="red">[3]</font></a></td>
		
        <td height="32"><a name="P82"></a><a href="/sort/Chtype/P82_1.html" class="sh14lian">P82&nbsp;电子制造业工程<font color="red">[2]</font></a></td>
		
        <td height="32"><a name="P83"></a><a href="/sort/Chtype/P83_1.html" class="sh14lian">P83&nbsp;船舶工业工程<font color="red">[3]</font></a></td>
      </tr>
	  
      <tr>
        <td height="32"><a name="P84"></a><a href="/sort/Chtype/P84_1.html" class="sh14lian">P84&nbsp;炸药与火工品工业工程<font color="red">[2]</font></a></td>
		
        <td height="32"><a name="PP81"></a><a href="/sort/Chtype/PP81_1.html" class="sh14lian">PP81&nbsp;电工制造业工程<font color="red">[0]</font></a></td>
		
        <td height="32"><a name="PP81"></a><a href="/sort/Chtype/_1.html" class="sh14lian">&nbsp;</a></td>
      </tr>
  
      <tr>
        <td height="32" class="ny_bg" colspan="3"><a name="P85/89"> <font style="font-size:14px; color:04048D"><strong>P85/89&nbsp;农林业及轻纺工业工程</strong></font></a></td>
      </tr>
	  
      <tr>
        <td height="32"><a name="P85"></a><a href="/sort/Chtype/P85_1.html" class="sh14lian">P85&nbsp;农牧、农垦工程<font color="red">[10]</font></a></td>
		
        <td height="32"><a name="P86"></a><a href="/sort/Chtype/P86_1.html" class="sh14lian">P86&nbsp;林业工程<font color="red">[3]</font></a></td>
		
        <td height="32"><a name="P87"></a><a href="/sort/Chtype/P87_1.html" class="sh14lian">P87&nbsp;水产与渔业工程<font color="red">[1]</font></a></td>
      </tr>
	  
      <tr>
        <td height="32"><a name="P88"></a><a href="/sort/Chtype/P88_1.html" class="sh14lian">P88&nbsp;轻工业工程<font color="red">[9]</font></a></td>
		
        <td height="32"><a name="P89"></a><a href="/sort/Chtype/P89_1.html" class="sh14lian">P89&nbsp;纺织工业工程<font color="red">[13]</font></a></td>
		
        <td height="32"><a name="P89"></a><a href="/sort/Chtype/_1.html" class="sh14lian">&nbsp;</a></td>
      </tr>
  
      <tr>
        <td height="32" class="ny_bg" colspan="3"><a name="P90/94"> <font style="font-size:14px; color:04048D"><strong>P90/94&nbsp;工业设备安装工程</strong></font></a></td>
      </tr>
	  
      <tr>
        <td height="32"><a name="P90"></a><a href="/sort/Chtype/P90_1.html" class="sh14lian">P90&nbsp;工业设备安装工程综合<font color="red">[12]</font></a></td>
		
        <td height="32"><a name="P91"></a><a href="/sort/Chtype/P91_1.html" class="sh14lian">P91&nbsp;电气设备安装工程<font color="red">[73]</font></a></td>
		
        <td height="32"><a name="P92"></a><a href="/sort/Chtype/P92_1.html" class="sh14lian">P92&nbsp;电信设备安装工程<font color="red">[24]</font></a></td>
      </tr>
	  
      <tr>
        <td height="32"><a name="P93"></a><a href="/sort/Chtype/P93_1.html" class="sh14lian">P93&nbsp;机械设备安装工程<font color="red">[77]</font></a></td>
		
        <td height="32"><a name="P94"></a><a href="/sort/Chtype/P94_1.html" class="sh14lian">P94&nbsp;金属设备与工艺管道安装工程<font color="red">[102]</font></a></td>
		
        <td height="32"><a name="P94"></a><a href="/sort/Chtype/_1.html" class="sh14lian">&nbsp;</a></td>
      </tr>
  
      <tr>
        <td height="32" class="ny_bg" colspan="3"><a name="P95/99"> <font style="font-size:14px; color:04048D"><strong>P95/99&nbsp;施工机械设备</strong></font></a></td>
      </tr>
	  
      <tr>
        <td height="32"><a name="P95"></a><a href="/sort/Chtype/P95_1.html" class="sh14lian">P95&nbsp;施工机械设备综合<font color="red">[73]</font></a></td>
		
        <td height="32"><a name="P96"></a><a href="/sort/Chtype/P96_1.html" class="sh14lian">P96&nbsp;作业设备与仪器仪表<font color="red">[97]</font></a></td>
		
        <td height="32"><a name="P97"></a><a href="/sort/Chtype/P97_1.html" class="sh14lian">P97&nbsp;建筑工程施工机械<font color="red">[747]</font></a></td>
      </tr>
	  
      <tr>
        <td height="32"><a name="P98"></a><a href="/sort/Chtype/P98_1.html" class="sh14lian">P98&nbsp;水利工程施工机械设备<font color="red">[3]</font></a></td>
		
        <td height="32"><a name="P98"></a><a href="/sort/Chtype/_1.html" class="sh14lian">&nbsp;</a></td>
		
        <td height="32"><a name="P98"></a><a href="/sort/Chtype/_1.html" class="sh14lian">&nbsp;</a></td>
      </tr>
	      
      <tr>
        <td colspan="2">&nbsp;</td>
      </tr>
    </tbody></table>
    </td><td width="210" align="right" valign="top">
 
<table width="100%" border="0" cellpadding="0" cellspacing="0">
      <tbody><tr>
        <td width="100%" class="4kuang"><table width="100%" border="0" cellspacing="0" cellpadding="0">
          <tbody><tr>
            <td><a href="/service/web.htm" target="_blank"><img src="/images/ny_y_kf1.gif" alt="点击和客服交流" border="0"></a></td>
          </tr>
 		  <tr>
            <td height="1" align="center"><img src="/images/xuxian.gif"></td>
          </tr>
         <tr>
            <td height="35"><table width="100%" border="0" cellspacing="0" cellpadding="0">
              <tbody><tr>
                <td width="7%"><img src="/images/ny_y_dh.gif" alt="未开通400地区或小灵通请直接拨打0898-3159 5809" width="63" height="29"></td>
                <td valign="center"><font color="#CC00FF"><strong>0898-3137-2222/13876321121</strong></font></td>
          </tr>
            </tbody></table></td>
  </tr>
        		  <tr>
            <td height="1" align="center"><img src="/images/xuxian.gif"></td>
          </tr>
   <tr>
            <td height="35"><table width="100%" border="0">
              <tbody><tr>
                <td width="7%"><img src="/images/ny_y_qq.gif" alt="客服QQ" width="55" height="29"></td>
                <td width="93%"><a target="blank" href="http://wpa.qq.com/msgrd?V=1&amp;Uin=1197428036&amp;Site=工标网&amp;Menu=yes">1197428036</a> <a target="blank" href="http://wpa.qq.com/msgrd?V=1&amp;Uin=992023608&amp;Site=工标网&amp;Menu=yes">992023608</a>
				
				</td>
              </tr>
            </tbody></table></td>
          </tr>
		  <tr>
            <td height="1" align="center"><img src="/images/xuxian.gif"></td>
          </tr>
          <tr>
            <td height="35"><table width="100%" border="0" cellspacing="0" cellpadding="0">
              <tbody><tr>
                <td width="7%"><img src="/images/ny_y_fax.gif" alt="传真" width="63" height="29"></td>
                <td valign="center">0898-6581 5245</td>
              </tr>
            </tbody></table></td>
          </tr>
 		  <tr>
            <td height="1" align="center"><img src="/images/xuxian.gif"></td>
          </tr>
        
          <tr>
            <td height="35"><table width="100%" border="0">
              <tbody><tr>
                <td width="7%"><img src="/images/ny_y_msn.gif" alt="MSN" width="56" height="29"></td>
                <td>13876321121</td>
              </tr>
            </tbody></table></td>
          </tr>
          
		  <tr>
            <td height="1" align="center"><img src="/images/xuxian.gif"></td>
          </tr>
         
		  
		  <tr>
            <td height="1" align="center"><img src="/images/xuxian.gif"></td>
          </tr>
         <tr>
            <td height="35" align="center" valign="middle"><a href="/service/web.htm" target="_blank"><img src="/images/v4_02.gif" alt="在线和客服咨询" width="139" height="28" border="0"></a></td>
          </tr>
		  
		  <tr>
            <td height="1" align="center"><img src="/images/xuxian.gif"></td>
          </tr>
         <tr>
            <td height="35">温馨提示：付款前请先与本网客服确认标准的实效和库存。</td>
          </tr>
		  
		  
</tbody></table></td>
      </tr>
</tbody></table>      
      <table width="100%" border="0" cellpadding="0" cellspacing="0">
        <tbody><tr>
          <td align="center">&nbsp;</td>
        </tr>
        <tr>
          <td align="center">&nbsp;</td>
        </tr>
      </tbody></table>
      <table width="100%" border="0" cellpadding="0" cellspacing="0">
        <tbody><tr>
          <td align="center" class="4kuang" bgcolor="#EFEFEF" height="26"><span class="lanxian">相关供应商</span></td>
        </tr>
        <tr>
          <td class="4kuang" align="center"><script type="text/javascript"><!--
											google_ad_client = "pub-0022378689113359";
											google_alternate_color = "FFFFFF";
											google_ad_width = 160;
											google_ad_height = 480;
											google_ad_format = "160x600_as";
											google_ad_type = "text_image";
											google_ad_channel ="";
											google_color_border = "FFFFFF";
											google_color_bg = "FFFFFF";
											google_color_link = "0000FF";
											google_color_text = "000000";
											google_color_url = "008000";
											//--></script>
											<script type="text/javascript" src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
											</script><ins class="adsbygoogle adsbygoogle-noablate" data-ad-channel="" data-ad-client="pub-0022378689113359" data-ad-format="160x600_as" data-ad-height="480" data-ad-type="text_image" data-ad-width="160" data-alternate-color="FFFFFF" data-color-bg="FFFFFF" data-color-border="FFFFFF" data-color-link="0000FF" data-color-text="000000" data-color-url="008000" data-adsbygoogle-status="done" style="display: inline-block; width: 160px; height: 480px;" data-ad-status="unfilled"><div id="aswift_0_host" style="border: none; height: 480px; width: 160px; margin: 0px; padding: 0px; position: relative; visibility: visible; background-color: transparent; display: inline-block;"><iframe id="aswift_0" name="aswift_0" browsingtopics="true" style="left:0;position:absolute;top:0;border:0;width:160px;height:480px;" sandbox="allow-forms allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts allow-top-navigation-by-user-activation" width="160" height="480" frameborder="0" marginwidth="0" marginheight="0" vspace="0" hspace="0" allowtransparency="true" scrolling="no" allow="attribution-reporting; run-ad-auction" src="https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-0022378689113359&amp;output=html&amp;h=480&amp;adk=4037846013&amp;adf=4259392547&amp;w=160&amp;lmt=1733717839&amp;ad_type=text_image&amp;format=160x600_as&amp;color_bg=FFFFFF&amp;color_border=FFFFFF&amp;color_link=0000FF&amp;color_text=000000&amp;color_url=008000&amp;url=http%3A%2F%2Fwww.csres.com%2Fsort%2Fchsortdetail%2FP.html%23P10%2F14&amp;alt_color=FFFFFF&amp;wgl=1&amp;dt=1733717838383&amp;bpp=511&amp;bdt=456&amp;idt=714&amp;shv=r20241120&amp;mjsv=m202412030101&amp;ptt=5&amp;saldr=sd&amp;abxe=1&amp;cookie_enabled=1&amp;eoidce=1&amp;correlator=484241102163&amp;frm=20&amp;pv=2&amp;u_tz=480&amp;u_his=1&amp;u_h=1080&amp;u_w=1920&amp;u_ah=1040&amp;u_aw=1920&amp;u_cd=24&amp;u_sd=1&amp;adx=1701&amp;ady=475&amp;biw=1903&amp;bih=953&amp;scr_x=0&amp;scr_y=244&amp;eid=31088580%2C31089332%2C95331833%2C95347444%2C95335245%2C95345967&amp;oid=2&amp;pvsid=1587212680129571&amp;tmod=1878792983&amp;uas=0&amp;nvt=1&amp;fc=896&amp;brdim=0%2C40%2C0%2C40%2C1920%2C40%2C1920%2C1040%2C1920%2C953&amp;vis=1&amp;rsz=d%7C%7CeE%7Cn&amp;abl=XS&amp;pfx=0&amp;fu=0&amp;bc=23&amp;bz=1&amp;psd=W251bGwsbnVsbCxudWxsLDNd&amp;nt=1&amp;ifi=1&amp;uci=a!1&amp;fsb=1&amp;dtd=727" data-google-container-id="a!1" tabindex="0" title="Advertisement" aria-label="Advertisement" data-load-complete="true"></iframe></div></ins>    </td>
        </tr>
      </tbody></table>
      <table width="100%" border="0" cellpadding="0" cellspacing="0">
        <tbody><tr>
          <td align="center">&nbsp;</td>
        </tr>
      </tbody></table>
      
</td>
  </tr>
</tbody></table>
	  </td>
    </tr>
    <tr> 

      <td height="19"><table width="100%" border="0" cellpadding="0" cellspacing="0" class="xuxiaxian">
        <tbody><tr>
          <td height="10">&nbsp;</td>
        </tr>
      </tbody></table></td>
    </tr>
    <tr> 
      <td align="center">&nbsp;</td>
    </tr>
    <tr> 
      <td>
 

<table width="100%" cellpadding="0" cellspacing="0" align="center">
  <tbody>
    <tr>
      <td align="middle" valign="middle" class="hong14">购书咨询:0898-3137-2222/13876321121</td>
    </tr>
    
    <tr> 
      <td align="middle" valign="middle"><font color="#666666"><strong>QQ:</strong></font><a target="blank" href="http://wpa.qq.com/msgrd?V=1&amp;Uin=1197428036&amp;Site=工标网&amp;Menu=yes">1197428036</a>&nbsp;<a target="blank" href="http://wpa.qq.com/msgrd?V=1&amp;Uin=992023608&amp;Site=工标网&amp;Menu=yes">992023608</a>      <a href="https://tb.53kf.com/code/client/9007981/1" target="_blank" title="点击联系在线客服，有什么问题我们帮您解决！！"><span style="font-size:12px; color:#0000CC; text-decoration:underline">有问题？ 联系在线客服</span></a>
</td>
    </tr>
    <tr> 
      <td align="middle" valign="center">版权所有2005-2021 海南讯海科技有限公司 经营许可证编号：<a href="https://beian.miit.gov.cn/" target="_blank">琼ICP备09001676号-1</a></td>
    </tr>
    <tr>
      <td align="middle" valign="center"><a href="/pay/" target="_blank"><font color="red">付款方式</font></a> | <a href="/sys/contact.html" target="_blank">联系我们</a> | <a href="/sys/aboutus.htm" target="_blank">关于我们 </a>| <a href="/sys/partners.jsp" target="_blank">合作伙伴</a> | <a href="javascript:window.external.AddFavorite('http://www.csres.com','工标网')"> 收藏本站</a> | <a href="/sys/terms.html" target="_blank">使用条款</a></td>
    </tr>
  </tbody>
</table>


</td>
    </tr>
<input type="hidden" name="pageNum" value="1">
 
  </tbody></table>






<ins class="adsbygoogle adsbygoogle-noablate" data-adsbygoogle-status="done" style="display: none !important;" data-ad-status="unfilled"><div id="aswift_1_host" style="border: none; height: 0px; width: 0px; margin: 0px; padding: 0px; position: relative; visibility: visible; background-color: transparent; display: inline-block;"><iframe id="aswift_1" name="aswift_1" browsingtopics="true" style="left:0;position:absolute;top:0;border:0;width:undefinedpx;height:undefinedpx;" sandbox="allow-forms allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts allow-top-navigation-by-user-activation" frameborder="0" marginwidth="0" marginheight="0" vspace="0" hspace="0" allowtransparency="true" scrolling="no" allow="attribution-reporting; run-ad-auction" src="https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-0022378689113359&amp;output=html&amp;adk=1812271804&amp;adf=3025194257&amp;abgtt=1&amp;lmt=1733717839&amp;plat=3%3A16%2C4%3A16%2C9%3A32776%2C16%3A8388608%2C17%3A32%2C24%3A32%2C25%3A32%2C30%3A1081344%2C32%3A32%2C41%3A32%2C42%3A32&amp;format=0x0&amp;url=http%3A%2F%2Fwww.csres.com%2Fsort%2Fchsortdetail%2FP.html%23P10%2F14&amp;pra=7&amp;wgl=1&amp;aihb=0&amp;asro=0&amp;ailel=1~2~4~6~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&amp;aiael=1~2~3~4~6~7~8~9~10~11~12~13~14~15~16~17~18~19~20~21~24~29~30~34&amp;aicel=33~38&amp;aifxl=29_18~30_19&amp;aiixl=29_5~30_6&amp;aiict=1&amp;aiapm=0.3221&amp;aiapmi=0.33938&amp;aiombap=1&amp;aief=1&amp;dt=1733717838894&amp;bpp=9&amp;bdt=966&amp;idt=222&amp;shv=r20241120&amp;mjsv=m202412030101&amp;ptt=9&amp;saldr=aa&amp;abxe=1&amp;cookie_enabled=1&amp;eoidce=1&amp;prev_fmts=160x600_as&amp;nras=1&amp;correlator=484241102163&amp;frm=20&amp;pv=1&amp;u_tz=480&amp;u_his=1&amp;u_h=1080&amp;u_w=1920&amp;u_ah=1040&amp;u_aw=1920&amp;u_cd=24&amp;u_sd=1&amp;adx=-12245933&amp;ady=-12245933&amp;biw=1903&amp;bih=953&amp;scr_x=0&amp;scr_y=244&amp;eid=31088580%2C31089332%2C95331833%2C95347444%2C95335245%2C95345967&amp;oid=2&amp;pvsid=1587212680129571&amp;tmod=1878792983&amp;uas=0&amp;nvt=1&amp;fsapi=1&amp;fc=896&amp;brdim=0%2C40%2C0%2C40%2C1920%2C40%2C1920%2C1040%2C1920%2C953&amp;vis=1&amp;rsz=%7C%7Cs%7C&amp;abl=NS&amp;fu=32768&amp;bc=23&amp;bz=1&amp;psd=W251bGwsbnVsbCxudWxsLDNd&amp;nt=1&amp;ifi=2&amp;uci=a!2&amp;fsb=1&amp;dtd=230" data-google-container-id="a!2" tabindex="0" title="Advertisement" aria-label="Advertisement" data-load-complete="true"></iframe></div></ins><iframe src="https://www.google.com/recaptcha/api2/aframe" width="0" height="0" style="display: none;"></iframe></body><div id="immersive-translate-popup" style="all: initial"></div><iframe id="google_esf" name="google_esf" src="https://googleads.g.doubleclick.net/pagead/html/r20241120/r20190131/zrt_lookup_fy2021.html" style="display: none;"></iframe></html>'''
    
if __name__ == '__main__':
    main()