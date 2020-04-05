import requests
import json

def getHTML(url):
     try:
         r = requests.get(url,timeout=30)
         r.raise_for_status()
         r.encoding = 'utf-8'
         return r.text
     except:
         return ""
def getVLCURL(html):
    # 获取stream
    streamBeg = html.find("\"stream\":")
    streamEnd = html.find("};", streamBeg)
    stream = html[streamBeg + 10  : streamEnd - 8]
    # print(streamBeg)
    # print(streamEnd)
    # print(stream)
    stream_json = json.loads(stream)
    # data是个列表
    data = stream_json['data']

    data_json = data[0]
    gameStreamInfoList = data_json['gameStreamInfoList']

    # gameStreamInfoList同样是个列表
    # print(type(gameStreamInfoList))
    # print(gameStreamInfoList)

    # 需要sFlvUrl  sStreamName  sFlvUrlSuffix sFlvAntiCode
    gameStreamInfoList_json = gameStreamInfoList[0]

    sFlvUrl = gameStreamInfoList_json['sFlvUrl']
    # print(sFlvUrl)
    # print(type(sFlvUrl))
    sStreamName = gameStreamInfoList_json['sStreamName']
    sFlvUrlSuffix = gameStreamInfoList_json['sFlvUrlSuffix']
    sFlvAntiCode = gameStreamInfoList_json['sFlvAntiCode']

    vlcURL = sFlvUrl + '/' + sStreamName + '.' + sFlvUrlSuffix + '?' + sFlvAntiCode
    # 将字符串中的下划线替换为空格
    vlcURL = vlcURL.replace('_', ' ')
    return vlcURL




    



if __name__ == "__main__":
    url = "https://www.huya.com/"
    roomID = input("请输入房间名称： ")
    url += roomID
    html = getHTML(url)
    print(getVLCURL(html))




# # json字符串转换为字典类型
# json_str2 = '{"programers":[ {"firstName":"Breet","lastName":"MMM","email":"XXX"},'\
#             '{"firstName":"Breet","lastName":"MMM","email":"XXX"}], ' \
#             '"author": [{"firstName": "su", "lastName": "yang", "email": "XXX"},'\
#             '{"firstName": "Breet", "lastName": "MMM", "email": "XXX"}]}'

# print(type(json_str2))

# data2 = json.loads(json_str2)

# print(type(data2))
