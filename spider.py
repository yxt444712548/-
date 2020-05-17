import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import re
import xlwt
findlink = re.compile(r'a href="(.*?)">')

findtitle = re.compile((r'<span class="title">(.*?)</span>'))

findimgsrc = re.compile(r'<img.*src="(.*?)"', re.S)

findrating = re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')

findjudge = re.compile(r'<span>(.*?)人评价</span>')

findinq = re.compile(r'<span class="inq">(.*?)</span>')

findbd = re.compile(r'<p class="">(.*?)</p>', re.S)


def main():
    baseurl = "https://movie.douban.com/top250?start="
    datalist = getData(baseurl)
    savepath = ".\\豆瓣电影Top250.xls"
    savedata(savepath, datalist)






def askURL(url):
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"}
    request = urllib.request.Request(url=url, headers=header, method='POST')
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        print(e.code, e.reason)
    return html


def getData(baseurl):
    datalist = []
    for i in range(10):
        url = baseurl + str(i*25)
        html = askURL(url)
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):
            data = []
            item = str(item)

            link = re.findall(findlink, item)[0]
            data.append(link)
            imgsrc = re.findall(findimgsrc, item)[0]
            data.append(imgsrc)
            title = re.findall(findtitle, item)
            if len(title) == 2:
                ctitle = title[0]
                etitle = title[1].replace("/", "")
            else:
                ctitle = title[0]
                etitle = ""
            data.append(ctitle)
            data.append(etitle)
            rating = re.findall(findrating, item)[0]
            data.append(rating)
            judge = re.findall(findjudge, item)[0]
            data.append(judge)
            inq = re.findall(findinq, item)[0]
            data.append(inq)
            bd = re.findall(findbd, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?', " ", bd)
            bd = re.sub('/', " ", bd)
            bd = re.sub('\xa0', " ", bd)
            data.append(bd.strip())

            datalist.append(data)

    return datalist

def savedata(savepath, datalist):
    print("saving..............")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet('豆瓣电影top250', cell_overwrite_ok=True)
    col = ("电影链接", "图片链接", "影片中文名", "影片外文名", "评分", "评价数", "概况", "相关信息")
    for i in range(8):
        sheet.write(0, i, col[i])
    for i in range(250):
        print("第%d条保存完毕"%(i+1))
        for j in range(8):
            sheet.write(i+1, j, datalist[i][j])
    book.save('豆瓣电影top250.xls')



main()






