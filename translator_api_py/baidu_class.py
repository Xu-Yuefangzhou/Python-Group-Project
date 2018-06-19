import http.client
import hashlib
from urllib import parse
import random

class BaiduFanyi:
     def __init__(self, ToLanguage, FromLanguage):
        self.httpClient = None
        self.myurl = '/api/trans/vip/translate'
        self.appid = '20180619000178058'
        self.secretKey = '1b8f0UumffJWowWndmdy'
        self.ToLanguage = ToLanguage 
        self.FromLanguage = FromLanguage  
        self.supported_languages = { # as defined here: http://msdn.microsoft.com/en-us/library/hh456380.aspx
            'zh' : '中文',
            'en' : '英语',
            'kor' : '韩语',
            'jp' : '日语',
            'spa' : '西班牙语',
            'fra': '法语',
            'th' : '泰语',
            'ara' : '阿拉伯语',
            'ru' : '俄语',
            'pt' : '葡萄牙语',
            'yue' : '粤语',
            'wyw' : '文言文',
            'auto' : '自动检测',
         }
     
     def print_supported_languages (self):
        """Display the list of supported language codes and the descriptions as a single string
        (used when a call to translate requests an unsupported code)"""
        codes = []
        for k,v in self.supported_languages.items():
            codes.append('\t'.join([k, '=', v]))
        return ('\n'.join(codes))
    
     def judge_from_languages (self):
        if self.FromLanguage not in self.supported_languages.keys():                  
            print ('Sorry, the API cannot translate from', self.FromLanguage)
            print ('Please use one of these instead:')
            return (0)
        else:
            return (1)
    
     def judge_to_languages (self):
        if self.ToLanguage not in self.supported_languages.keys():                  # 检验译语是否支持
            print ('Sorry, the API cannot translate to', self.ToLanguage)
            print ('Please use one of these instead:')
            return (0)
        else:
            return (1)
            
    
     def translate (self, queryText):
        salt = random.randint(32768, 65536)
        sign = self.appid+queryText+str(salt)+self.secretKey
        m1 = hashlib.md5()
        m1.update(sign.encode(encoding='utf-8'))
        sign = m1.hexdigest()
        myurl = self.myurl+'?appid='+self.appid+'&q='+parse.quote(queryText)+'&from='+self.FromLanguage+'&to='+self.ToLanguage+'&salt='+str(salt)+'&sign='+sign 
        file = open('result_baidu.txt','w')
        try:
            httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)
            response = httpClient.getresponse()
            string = response.read().decode('utf-8')
            string = eval(string)                           # eval() 函数用来执行一个字符串表达式，并返回表达式的值。
            for line in string['trans_result']:          # str['trans_result']里有百度api返回的结果
                file.write(line['dst']+'\n')
        except Exception as e:
            print(e)
        finally:
            if httpClient:
                httpClient.close()
        file.close()
    
    # Note: We convert result, which is JSON, to and from an object so we can pretty-print it.
    # We want to avoid escaping any Unicode characters that result contains. See:
    # https://stackoverflow.com/questions/18337407/saving-utf-8-texts-in-json-dumps-as-utf8-not-as-u-escape-sequence
         
if __name__ == "__main__":
    FromLanguage = input("请输入源语言: ").strip()
    ToLanguage = input("请输入目标语言: ").strip()
    fanyi = BaiduFanyi(ToLanguage, FromLanguage) 
    source = fanyi.judge_from_languages()
    if (source==0):
        print (fanyi.print_supported_languages())
    target = fanyi.judge_to_languages()
    if (target==0):
        print (fanyi.print_supported_languages())
   
    if (source==1 and target==1):
        with open('fanyi.txt') as f: # 默认模式为‘r’，只读模式
            contents = f.read() # 读取文件全部内容
            fanyi.translate(contents)
            
