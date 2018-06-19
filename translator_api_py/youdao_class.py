import urllib.request
import json
import time
import hashlib
class YouDaoFanyi:
    def __init__(self):
        self.url = 'https://openapi.youdao.com/api/'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36",
        }
        self.appKey = '2de5d757cddcc6cb'  # 应用id
        self.appSecret = 'sbyMDDHj8FZF95twB6cBjzRSmaTrw5r0'  # 应用密钥
        self.langFrom = 'auto'   # 翻译前文字语言,auto为自动检查
        self.langTo = 'auto'     # 翻译后文字语言,auto为自动检查

    def getUrlEncodedData(self, queryText):
        '''
        将数据url编码
        :param queryText: 待翻译的文字
        :return: 返回url编码过的数据
        '''
        salt = str(int(round(time.time() * 1000)))  # 产生随机数 ,其实固定值也可以,不如"2"
        sign_str = self.appKey + queryText + salt + self.appSecret
        sign = hashlib.md5(sign_str.encode("utf8")).hexdigest()  
        # 要先对sign.str进行统一编码，否则报错：Unicode-objects must be encoded before hashing，参考：https://blog.csdn.net/haungrui/article/details/6959340
        payload = {
            'q': queryText,
            'from': self.langFrom,
            'to': self.langTo,
            'appKey': self.appKey,
            'salt': salt,
            'sign': sign
        }

        # 注意是get请求，不是请求
        data = urllib.parse.urlencode(payload)
        return (data)

    def parseHtml(self, html):
        '''
        解析页面，输出翻译结果
        :param html: 翻译返回的页面内容
        :return: None
        '''
        data = json.loads(html.decode('utf-8'))
        translationResult = data['translation']
        if isinstance(translationResult, list):
            translationResult = translationResult[0]
        return translationResult                    # 打印调用api的翻译结果
        
    def translate(self, queryText):
        data = self.getUrlEncodedData(queryText)  # 获取url编码过的数据
        target_url = self.url + '?' + data    # 构造目标url
        request = urllib.request.Request(target_url, headers=self.headers)  # 构造请求
        response = urllib.request.urlopen(request)  # 发送请求
        return self.parseHtml(response.read())    # 解析，显示翻译结果
    
    def sealfile (self, Printtext):
        file = open('result_youdao.txt','w')
        file.write(Printtext)


if __name__ == "__main__":
    fanyi = YouDaoFanyi()     # fanyi是YouDaoFanyi的一个对象
    with open('fanyi.txt') as f: # 默认模式为‘r’，只读模式
        contents = f.read() # 读取文件全部内容
        #contents.rstrip() # rstrip()函数用于删除字符串末的空白
        printtext = fanyi.translate(contents)
        fanyi.sealfile(printtext)


