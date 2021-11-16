import os, time, re, requests
import hashlib, base64
from selenium import webdriver

# 获取当前根目录路径
def getCurOriPath():
    return os.path.abspath(os.path.dirname(__file__))

# 清洗掉开头空格和结尾的空格
def delSpace(paragraph):
    # return paragraph.replace("\r", "").replace("\n", "").replace("\t", "").replace("\xa0", "").replace("\u3000","")
    return paragraph.strip()

def finishTask():
    print("流程结束，单次任务结束（爬取、处理、上传数据， 对应数据库数据的清空以及posturldatabase数据库的更新）")

# 清空指定目录下所有文件
def clearDirFiles(dirPath):
    lis = os.listdir(dirPath)
    for i in lis:
        os.remove(dirPath + i)

# 删除指定文件
def delVideoSingle(filePath):
    os.remove(filePath)


# 获取当前日期
def getCurDate():
    return time.strftime("%Y%m%d", time.localtime())

# 返回指定日期时间戳 时间格式 '%Y%m%d %H:%M:%S' 20210924 00：00：00 该方法用于哔哩哔哩时间的判断
def getSecondByDate(date):
    b = time.strptime(date, '%Y%m%d %H:%M:%S')
    return time.mktime(b)

# 通过selenium获取指定信息的类
class GetParams_Selenium:
    def __init__(self, *driverPath):
        if(driverPath!=()):
            option = webdriver.ChromeOptions()
            option.add_experimental_option('excludeSwitches', ['enable-automation'])
            option.add_experimental_option('useAutomationExtension', False)
            self.browser = webdriver.Chrome(driverPath, options=option)


    def getCookies(self, *url, browser):
        '''
        类方法，以对象形式输出指定链接返回的cookies
        :param url: 待打开的链接
        :param browser: 浏览器引擎
        :return: cookies对象
        '''
        # 获取cookie
        dictCookies = browser.get_cookies()
        cookies = {}
        for item in dictCookies:
            key = item['name']
            cookies[str(key)] = str(item['value'])
        return cookies

    def del_all_cookies(self):
        self.browser.delete_all_cookies()

    def get_params(self, url, *browser):
        if(browser==()):
            self.browser.get(url)
            time.sleep(1)
            cookies = self.getCookies(url, self.browser)
            headers = {}
            return {
                'cookies': cookies,
                'headers': headers
            }
        else:
            browser.get(url)
            time.sleep(1)
            cookies = self.getCookies(url, browser)
            headers = {}
            return {
                'cookies': cookies,
                'headers': headers
            }


    def closeBrowser(self, *browser):
        '''
        关闭指定浏览器，若浏览器为None则关闭对象浏览器
        :param browser:
        :return: None
        '''
        if(browser==()):
            self.browser.close()
        else:
            browser.close()


# 字符串正则处理类
class Handler_String_ByRe:
    def extract_StrByRe(self, string, patternStr=r'[[](.*?)[]]'):
        '''
        正则匹配字符串获取指定内容(匹配[]包括这的内容)
        :param string: 待匹配的字符串
        :param patternStr: 正则表达式模式
        :return: 列表
        '''
        pattern = re.compile(patternStr, re.S)  # 最小匹配
        return re.findall(pattern, string)



class Handle_PackageInfo:
    '''
        处理报文信息 如 cookie和headers字符串和对象的转换
    '''
    def translate_Cookies_Row2Obj(self, cookiesRow):
        cookieList = cookiesRow.split(";")
        self.cookies = {}
        for cookieItem in cookieList:
            i = cookieItem.strip().split("=")
            k = i[0]
            v = i[1]
            self.cookies[k] = v
        return self.cookies

    def translate_Headers_Row2Obj(self, headersRow):
        headerList = headersRow.split('\n')
        self.headers = {}
        for headerItem in headerList:
            i = headerItem.strip().split(":")
            if (i != ['']):
                k = i[0]
                v = i[1]
                self.headers[k] = v
        return self.headers


# 加密类
class Encode:
    # 同一输出类型为str
    def bytes2str(self, b):
        return str(b, encoding='utf-8')

    def str2bytes(self, s):
        return bytes(s, encoding='utf-8')

    def encodeByMd5(self, s):
        return hashlib.md5(s.encode(encoding='utf-8')).hexdigest()

    # base64输出的为bytes类型 要转化为字符串
    def encodeByBase64(self, s):
        res = base64.encodebytes(s).strip()
        # 转换为字符串
        res = self.bytes2str(res)
        return res

    def encode0(self,s):
        return self.encodeByBase64(self.str2bytes(self.encodeByMd5(s)))

# 目录处理类
class Contraler_Dir:
    # 获取当前根目录路径
    def getCurOriPath(self):
        return os.path.abspath(os.path.dirname(__file__))

    # 判断目录是否存在，不存在则创建
    def checkACreateDir(self,dirPath):
        exist = os.path.exists(dirPath)
        if (not exist):
            os.makedirs(dirPath)
        else:
            pass
        pass

    # 清空指定目录下所有文件
    def clearDirFiles(self, dirPath):
        lis = os.listdir(dirPath)
        for i in lis:
            os.remove(dirPath + i)

# 时间处理类
class Contraler_Time:
    # 获取当前日期
    def getCurDate(self):
        return time.strftime("%Y%m%d", time.localtime())

    # 返回指定日期时间戳 时间格式 '%Y%m%d %H:%M:%S' 20210924 00：00：00 该方法用于哔哩哔哩时间的判断
    def getSecondByDate(self, date):
        b = time.strptime(date, '%Y%m%d %H:%M:%S')
        return time.mktime(b)

# 下载类
class Downloader:
    # 已有图片链接下载图片的方法
    def download_img(self, urlpath, imgname, dstDirPath):
        '''
        图片下载
        :param urlpath: 可下载的图片资源链接
        :param imgname: 保存图片为指定名字
        :param dstDirPath: 图片保存目录位置，注意：最后要有\\
        :return:
        '''
        r = requests.get(urlpath)
        img = r.content  # 响应的二进制文件
        with open(dstDirPath + str(imgname) + '.png', 'wb') as f:  # 二进制写入
            f.write(img)

    # 下载视频
