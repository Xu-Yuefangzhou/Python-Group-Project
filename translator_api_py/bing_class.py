import http.client, urllib.parse, uuid, json
class BingFanyi:
     def __init__(self, ToLanguage):
        self.host = 'api.cognitive.microsofttranslator.com'
        self.path = '/translate?api-version=3.0'
        self.subscriptionKey = 'fc278423ccf7460a9c6da38a049dcd5c' 
        self.headers = {
            'Ocp-Apim-Subscription-Key': self.subscriptionKey,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }
        self.ToLanguage = ToLanguage  
        self.supported_languages = { # as defined here: http://msdn.microsoft.com/en-us/library/hh456380.aspx
            'ar' : ' Arabic',
            'bg' : 'Bulgarian',
            'ca' : 'Catalan',
            'zh-CHS' : 'Chinese (Simplified)',
            'zh-CHT' : 'Chinese (Simplified)',
            'zh-Hans': 'Chinese (Simplified)',
            'cs' : 'Czech',
            'da' : 'Danish',
            'nl' : 'Dutch',
            'en' : 'English',
            'et' : 'Estonian',
            'fi' : 'Finnish',
            'fr' : 'French',
            'de' : 'German',
            'el' : 'Greek',
            'ht' : 'Haitian Creole',
            'he' : 'Hebrew',
            'hi' : 'Hindi',
            'hu' : 'Hungarian',
            'id' : 'Indonesian',
            'it' : 'Italian',
            'ja' : 'Japanese',
            'ko' : 'Korean',
            'lv' : 'Latvian',
            'lt' : 'Lithuanian',
            'mww' : 'Hmong Daw',
            'no' : 'Norwegian',
            'pl' : 'Polish',
            'pt' : 'Portuguese',
            'ro' : 'Romanian',
            'ru' : 'Russian',
            'sk' : 'Slovak',
            'sl' : 'Slovenian',
            'es' : 'Spanish',
            'sv' : 'Swedish',
            'th' : 'Thai',
            'tr' : 'Turkish',
            'uk' : 'Ukrainian',
            'vi' : 'Vietnamese',
         }
     
     def print_supported_languages (self):
        """Display the list of supported language codes and the descriptions as a single string
        (used when a call to translate requests an unsupported code)"""
        codes = []
        for k,v in self.supported_languages.items():
            codes.append('\t'.join([k, '=', v]))
        return ('\n'.join(codes))
    
     def judge_to_languages (self):
        if self.ToLanguage not in self.supported_languages.keys():                  # 检验译语是否支持
            print ('Sorry, the API cannot translate to', self.ToLanguage)
            print ('Please use one of these instead:')
            #print (print_supported_languages(self))
            return (0)
        else:
            return (1)
            
    
     def translate (self, queryText):
        requestBody = [{
            'Text' : queryText,
        }]
        queryText = json.dumps(requestBody, ensure_ascii=False).encode('utf-8')
        conn = http.client.HTTPSConnection(self.host)
        conn.request ("POST", self.path + "&to=" + self.ToLanguage, queryText, self.headers)
        response = conn.getresponse ()
        result = response.read () 
        output = json.dumps(json.loads(result.decode('utf-8')), indent=4, ensure_ascii=False)
        d=eval(output)
        translationResult = d[0]['translations'][0]['text']
        if isinstance(translationResult, str):
            return translationResult
        
     def sealfile (self, printtext):
         file = open('result_bing.txt','w')
         #for line in string['trans_result']:          # str['trans_result']里有百度api返回的结果
         file.write(printtext)
    
    # Note: We convert result, which is JSON, to and from an object so we can pretty-print it.
    # We want to avoid escaping any Unicode characters that result contains. See:
    # https://stackoverflow.com/questions/18337407/saving-utf-8-texts-in-json-dumps-as-utf8-not-as-u-escape-sequence
         
if __name__ == "__main__":
    ToLanguage = 'zh-CHT'
    fanyi = BingFanyi(ToLanguage) 
    to = fanyi.judge_to_languages()
    if (to==0):
        print (fanyi.print_supported_languages())
    if (to==1):
        with open('fanyi.txt') as f: # 默认模式为‘r’，只读模式
            contents = f.read() # 读取文件全部内容
            #contents.rstrip() # rstrip()函数用于删除字符串末的空白
            printtext = fanyi.translate(contents)
            fanyi.sealfile(printtext)