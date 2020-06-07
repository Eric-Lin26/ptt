import urllib.request as req
from bs4 import BeautifulSoup
import time

def pttNBA(url):
    today = time.strftime('%m/%d').lstrip('0') # 今天的日期
    request = req.Request(url, headers={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
    })
    with req.urlopen(request) as response:
        data = response.read().decode('utf-8')
    
    root = BeautifulSoup(data, 'html.parser')

    paging = root.find('div', 'btn-group btn-group-paging').find_all('a')[1]['href']
    # 換頁：先用find抓取div標籤, 屬性為btn-group btn-group-paging
    # 再用find_all抓取底下所有的a標籤, 且觀察到下頁的標籤為排列第二個
    # 故後面抓取[1], 並抓取[href]網址進行換頁, 但網址是相對位置(只有一半)
    # 所以後面還得加上https://www.ptt.cc/

    articles = []  # 將下面的for迴圈抓到的資料放入這
    rents = root.find_all('div', 'r-ent')

    for rent in rents:
        title = rent.find('div', 'title').text.strip()
            # 取得標題, 用text只取得標題文字, strip()去除空白
        count = rent.find('div', 'nrec').text.strip()
            # 取得推文數, 用text只取得標題文字, strip()去除空白
        date = rent.find('div', 'meta').find('div', 'date').text.strip()
            # 取得日期, 用text只取得標題文字, strip()去除空白
            # 但因日期包覆在meta屬性標籤下, 再使用一次find抓取date屬性中的日期
        article = date + ' ' + count + ':' + title
        if date == today: # 只抓取當天資料
            articles.append(article)

    if len(articles) != 0: # 判斷是否有資料
        for article in articles:
            print(article)
            time.sleep(5)
            pttNBA('https://www.ptt.cc/' + paging) # 跳回繼續執行函式
    else:
        return

pttNBA('https://www.ptt.cc/bbs/NBA/index.html')