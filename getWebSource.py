import requests
import json
import os

def loadRecommend():
    # 判断文件是否存在不存在则创建
    if os.path.isfile("recommend.txt"):
        # 如果存在
        # 加载推荐列表
        str1 = "猜你想看\n"
        with open("recommend.txt", 'r') as f:
            str1 += f.read()
        return str1
    else :
        # 如果不存在
        print("欢迎使用，系统已帮您创建推荐文件！\n")
        with open("recommend.txt", "a") as f:
            print("已创建recommend.txt")
        return ""



def getHTML(url):
    # 获取网站源码

     try:
         r = requests.get(url,timeout=30)
         r.raise_for_status()
         r.encoding = 'utf-8'
         return r.text
     except:
         return ""
def getVLCURL(html):
    # 根据源码，获取URL

    vlcURL = ''

    # 获取stream
    streamBeg = html.find("\"stream\":")
    streamEnd = html.find("};", streamBeg)
    stream = html[streamBeg + 10  : streamEnd - 8]
    
    try:
        stream_json = json.loads(stream)
        # data是个列表
        data = stream_json['data']

        data_json = data[0]
        gameStreamInfoList = data_json['gameStreamInfoList']

        # gameStreamInfoList同样是个列表

        # 需要sFlvUrl  sStreamName  sFlvUrlSuffix sFlvAntiCode
        gameStreamInfoList_json = gameStreamInfoList[0]

        sFlvUrl = gameStreamInfoList_json['sFlvUrl']
        # print(sFlvUrl)
        # print(type(sFlvUrl))
        sStreamName = gameStreamInfoList_json['sStreamName']
        sFlvUrlSuffix = gameStreamInfoList_json['sFlvUrlSuffix']
        sFlvAntiCode = gameStreamInfoList_json['sFlvAntiCode']

        sFlvAntiCode = sFlvAntiCode.replace('amp;','')
        vlcURL = sFlvUrl + '/' + sStreamName + '.' + sFlvUrlSuffix + '?' + sFlvAntiCode
        # 将字符串中的下划线替换为空格
        vlcURL = vlcURL.replace('_', ' ')
    except json.decoder.JSONDecodeError:
        print("房间号错误！！")
    except TypeError:
        print("房间未开播！！")
    # BL 蓝光
    # HD 高清
    # Fluency 流畅
    # &ratio=2500  &ratio=500
    BL_vlcURL = vlcURL
    HD_vlcURL = vlcURL + "&ratio=2500"
    F_vlcURL = vlcURL + "&ratio=500"
    URLList = [BL_vlcURL, HD_vlcURL, F_vlcURL]
    # 依次返回蓝光，高清，流畅
    return URLList
    
def updateRecommend(html, roomID):
    # 获取直播关键字
    keyWordsBeg = html.find("<meta name=\"Keywords\" content=")
    keyWordsEnd = html.find("\"/>", keyWordsBeg)
    keyWords = html[keyWordsBeg + 31 : keyWordsEnd]
    # print(keyWords)

    # 判断是否有重复，重复则不再在写入
    str1 = loadRecommend()
    if str1.find(roomID) != -1:
        print("推荐列表已更新")
    else:
        with open("recommend.txt", "a") as f:
            content = "ID:" + roomID + "——————" + keyWords + "\n"
            f.write(content)
        print("推荐列表已更新")
    




    



if __name__ == "__main__":
    # 加载推荐房间
    recommend = loadRecommend()
    print(recommend)

    url = "https://www.huya.com/"
    roomID = input("请输入房间名称： ")
    url += roomID
    # 获取网页源码
    html = getHTML(url)

    # 获取播放链接
    URLList = getVLCURL(html)

    # 更新推荐列表
    updateRecommend(html, roomID)

    # 打印播放链接
    print("蓝光画质：" + URLList[0])
    print("\n")
    print("高清画质：" + URLList[1])
    print("\n")
    print("流畅画质：" + URLList[2])
    print("\n")





