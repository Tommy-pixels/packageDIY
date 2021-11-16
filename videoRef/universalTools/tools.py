import re, os
import datetime

from selenium import webdriver
import pymysql
from selenium.webdriver.common.action_chains import ActionChains
import random, time
import requests
import shutil
# from .. import globalTools
import cv2
import numpy as np

'''
    返回毫秒级时间戳
'''
def getMilliSecond():
    return int(round(time.time() * 1000))

# 返回指定日期时间戳 时间格式 '%Y%m%d %H:%M:%S' 20210924 00：00：00 该方法用于哔哩哔哩时间的判断
def getSecondByDate(date):
    b = time.strptime(date, '%Y%m%d %H:%M:%S')
    return time.mktime(b)

class cleanCookiesAndHeadersByRow():
    def translateCookies(self, row):
        cookieList = row.split(";")
        cookies = {}
        for item in cookieList:
            key = item.split("=")[0]
            val = item.split("=")[1]
            cookies[str(key).strip()] = str(val).strip()
        return cookies
    def translateHeaders(self, row):
        headerList = row.split("\n")
        headers = {}
        for item in headerList:
            key = item.split(":")[0].strip()
            if(key == 'Referer'):
                val = item[9:]
            else:
                try:
                    val = str(item).split(":")[1]
                except Exception as e:
                    print(e)

            if(key!=''):
                headers[key] = str(val).strip()
        return headers

"""
:param  articleItem  Pipeline的Item
"""
class cleanArticleItem():
    def __init__(self, artivleItem):
        self.articleItem = artivleItem
        self.setCleanedArticleItem()

    def setCleanedArticleItem(self):
        temp = self.cleanArticleItem()
        self.cleaned_articleItem = temp
        return None

    def getCleanedArticleItem(self):
        return self.cleaned_articleItem

    def cleanFuncBasic(self, s):
        if(re.search(':',str(s)) or re.search('：',str(s))):
            sList = str(s).split("：") or str(s).split(":")
            result = "".join(sList[1].strip())
            return result
        else:
            print("传入的字符串没有冒号，不能分离")
            return None
    def translateTime(self, s):
        return datetime.datetime.strptime(str(s), "%Y-%m-%d %H:%M:%S")

    def cleanContent(self, lis):
        for item in lis:
            item = item.replace('\u3000','')
        strContent = "".join(lis).replace('\'','\"')
        return strContent
    # 返回图片名，无.jpg
    def cleanImgSrc2Name(self, s):
        return str(str(s).split('/')[-1]).split('.')[0]

    def cleanArticleItem(self):
        temp = {}
        temp['articleTitle'] = self.articleItem['articleTitle']
        temp['articleAbstract'] = self.articleItem['articleAbstract']
        temp['articleFrom'] = self.cleanFuncBasic(self.articleItem['articleFrom'])
        temp['articleAuthor'] = self.cleanFuncBasic(self.articleItem['articleAuthor'])
        temp['articleTime'] = self.translateTime(self.cleanFuncBasic(self.articleItem['articleTime']))
        temp['articleContent'] = self.cleanContent(self.articleItem['articleContent'])
        temp['articleImgSrc'] = self.articleItem['articleImgSrc']
        # 从图片路径提取图片名
        temp['articleImgName'] = self.cleanImgSrc2Name(self.articleItem['articleImgSrc'])
        return temp


# --------------------------- 爬取今日头条财经目录下所有图片的类 ----------------------------------
'''
    使用框架 selenium
    没有有url，获取文章的url
'''
class articleUrl_toutiao():
    # 代理服务器(产品官网 www.16yun.cn)
    proxyHost = "u7125.5.tp.16yun.cn"
    proxyPort = "6445"

    # 代理验证信息
    proxyUser = "16HMCXON"
    proxyPass = "387861"

    # def create_proxy_auth_extension(proxy_host, proxy_port,
    #                                 proxy_username, proxy_password,
    #                                 scheme='http', plugin_path=None):
    #
    #     # 代理服务器(产品官网 www.16yun.cn)
    #     proxyHost = "u7125.5.tp.16yun.cn"
    #     proxyPort = "6445"
    #
    #     # 代理验证信息
    #     proxyUser = "16HMCXON"
    #     proxyPass = "387861"
    #
    #     proxy_host = proxyHost
    #     proxy_port = proxyPort
    #     proxy_username = proxyUser
    #     proxy_password = proxyPass
    #
    #     if plugin_path is None:
    #         plugin_path = r'D:/{}_{}@t.16yun.zip'.format(proxy_username, proxy_password)
    #
    #     manifest_json = """
    #     {
    #         "version": "1.0.0",
    #         "manifest_version": 2,
    #         "name": "16YUN Proxy",
    #         "permissions": [
    #             "proxy",
    #             "tabs",
    #             "unlimitedStorage",
    #             "storage",
    #             "",
    #             "webRequest",
    #             "webRequestBlocking"
    #         ],
    #         "background": {
    #             "scripts": ["background.js"]
    #         },
    #         "minimum_chrome_version":"22.0.0"
    #     }
    #     """
    #
    #     background_js = string.Template(
    #         """
    #         var config = {
    #             mode: "fixed_servers",
    #             rules: {
    #                 singleProxy: {
    #                     scheme: "${scheme}",
    #                     host: "${host}",
    #                     port: parseInt(${port})
    #                 },
    #                 bypassList: ["foobar.com"]
    #             }
    #           };
    #
    #         chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    #
    #         function callbackFn(details) {
    #             return {
    #                 authCredentials: {
    #                     username: "${username}",
    #                     password: "${password}"
    #                 }
    #             };
    #         }
    #
    #         chrome.webRequest.onAuthRequired.addListener(
    #             callbackFn,
    #             {urls: [""]},
    #             ['blocking']
    #         );
    #         """
    #     ).substitute(
    #         host=proxy_host,
    #         port=proxy_port,
    #         username=proxy_username,
    #         password=proxy_password,
    #         scheme=scheme,
    #     )
    #
    #     with zipfile.ZipFile(plugin_path, 'w') as zp:
    #         zp.writestr("manifest.json", manifest_json)
    #         zp.writestr("background.js", background_js)
    #
    #     return plugin_path
    #
    # proxy_auth_plugin_path = create_proxy_auth_extension(
    #     proxy_host=proxyHost,
    #     proxy_port=proxyPort,
    #     proxy_username=proxyUser,
    #     proxy_password=proxyPass)
    #
    # option = webdriver.ChromeOptions()
    #
    # option.add_argument("--start-maximized")
    #
    # # 如报错 chrome-extensions
    # # option.add_argument("--disable-extensions")
    #
    # option.add_extension(proxy_auth_plugin_path)
    #
    # # 关闭webdriver的一些标志
    # # option.add_experimental_option('excludeSwitches', ['enable-automation'])
    #
    # driver = webdriver.Chrome(executable_path="E:\Projects\webDriver\\chrome\\chromedriver.exe", chrome_options=option)
    #
    # # 修改webdriver get属性
    # # script = '''
    # # Object.defineProperty(navigator, 'webdriver', {
    # # get: () => undefined
    # # })
    # # '''
    # # driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})
    # result = driver.get("http://httpbin.org/ip")
    # print(result)
    # pass

    def get_cookiesAndSignature(self):
        option = webdriver.ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_experimental_option('useAutomationExtension', False)
        browser = webdriver.Chrome(executable_path="E:\Projects\webDriver\\chrome\\chromedriver.exe", options=option)
        start_urls = "https://www.toutiao.com/"
        # 2.通过浏览器向服务器发送URL请求
        # browser.get("http://httpbin.org/ip")    # 查看本机ip，看代理是否起作用

        browser.get(start_urls)
        time.sleep(1)  # 等待
        # xhr重写
        js = """(function() {
                var proxied = window.XMLHttpRequest.prototype.open;
                let root = document.getElementById("root");
                let urlLinkNode = document.createElement("div");
                urlLinkNode.setAttribute("id", "urlLinkNode");
                root.appendChild(urlLinkNode);
                window.XMLHttpRequest.prototype.open = function() {
                    if(arguments[0]=='GET' && arguments[1].search("channel_id=3189399007")){
                        console.log(arguments);
                        let urlLinkNodeReal = document.getElementById("urlLinkNode")
                        urlLinkNodeReal.innerHTML = arguments[1];
                        return proxied.apply(this, [].slice.call(arguments));
                    }else{
                        return 0
                    }
                };
            })();"""
        browser.execute_script(js)

        # 定位
        caijing = browser.find_element_by_xpath("//div[@class='left-container']//ul[@class='feed-default-nav']/li[4]")
        time.sleep(2)
        caijing.click()

        # 获取最新signature
        signatureApi = browser.find_element_by_id("urlLinkNode").text
        signature = str(signatureApi).split("signature=")[1]
        # 获取cookie
        dictCookies = browser.get_cookies()
        cookies = {}
        for item in dictCookies:
            key = item['name']
            cookies[str(key)] = str(item['value'])
        browser.close()
        return {
            "cookies":cookies,
            "signature":signature
        }

    def open(self):
        pass

'''
    使用框架 selenium
    已有url，下载url下的图片
'''
class ImgsDownloadByUrl():
    def __init__(self):
        self.conn = pymysql.connect(
            host='localhost',
            user="root",
            passwd="root",
            db="articledatabase",
            autocommit=True
        )
        self.cursor = self.conn.cursor()
        self.gerUrlFromMysql()

    def gerUrlFromMysql(self):
        sql = "SELECT * FROM `articledatabase`.`tb_imgstoutiaocaijing`;"
        self.cursor.execute(sql)
        urlList = self.cursor.fetchall()
        self.urlList = urlList
        self.closeMysql()
        return urlList

    # def download(self):
    #     option = webdriver.ChromeOptions()
    #     option.add_experimental_option('excludeSwitches', ['enable-automation'])
    #     option.add_experimental_option('useAutomationExtension', False)
    #     browser = webdriver.Chrome(executable_path="E:\Projects\webDriver\\chrome\\chromedriver.exe", options=option)
    #     self.urlList = self.urlList[5781:]
    #     # 2.通过浏览器向服务器发送URL请求
    #     for item in self.urlList:
    #         browser.get(item[1])
    #         time.sleep(0.5)  # 等待
    #         # 定位
    #         img = browser.find_element_by_xpath("//img")
    #         actions = ActionChains(browser)
    #         # 找到图片后右键单击图片
    #         actions.move_to_element(img)  # 定位到元素
    #         pyautogui.hotkey("ctrl", "s")
    #         time.sleep(0.5)  # 等待一秒
    #         # 输入视频名字
    #         pyautogui.typewrite(str(item[0]) + '.jpg')
    #         pyautogui.hotkey('enter')
    #         sleep(1)
    #     browser.close()

    def file_path(self, request, response=None, info=None, *, item=None):
        # 提取图片名
        imgName = str(str(request.url).split('/')[-1]).split('?')[0]
        return f'toutiaoImgs/{imgName}.jpg'

    def closeMysql(self):
        self.cursor.close()
        self.conn.close()


# --------------------------- 随机时间休眠 ----------------------------------
# 随机时间
def randomSleep():
    sleepTime = random.randint(0,50)
    time.sleep(sleepTime)
    pass

# --------------------------- 东方财富 cookie 和 signature 自动获取 -----------
class ArticleTool_DongFangCaiFu():
    def get_cookies_auto(self):
        option = webdriver.ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_experimental_option('useAutomationExtension', False)
        browser = webdriver.Chrome(executable_path="E:\Projects\webDriver\\chrome\\chromedriver.exe", options=option)
        start_urls = "https://www.eastmoney.com/"
        # 2.通过浏览器向服务器发送URL请求
        # browser.get("http://httpbin.org/ip")    # 查看本机ip，看代理是否起作用
        browser.get(start_urls)
        time.sleep(1)  # 等待
        # 获取cookie
        dictCookies = browser.get_cookies()
        cookies = {}
        for item in dictCookies:
            key = item['name']
            cookies[str(key)] = str(item['value'])
        browser.close()
        return cookies

# 已有图片链接下载图片的方法
def downimg(urlpath, imgname, dstDirPath):
    # 获取当前日期
    r = requests.get(urlpath)
    img = r.content       #响应的二进制文件
    with open(dstDirPath + str(imgname) + '.png','wb') as f:     #二进制写入
        f.write(img)


# 图片重命名
def reName(imgSrc, imgDst):
    os.rename(imgSrc, imgDst)


# 获取accessToken的方法
def getAccessToken(AK, SK):
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(AK, SK)
    response = requests.get(host)
    if response:
        return response.json()['access_token']


# 复制文件
def copyFile(src, dst):
    shutil.copyfile(src, dst)


def checkIfAllNumber(str):
    # 验证字符串是否全部为数字
    p = re.compile('^[0-9]*$')
    result = p.match(str)
    if(result):
        # 说明全部位数字，返回1
        return 1
    else:
        return 0

# 判断目录是否存在，不存在则创建
def checkACreateDir(dirPath):
    exist = os.path.exists(dirPath)
    if(not exist):
        os.makedirs(dirPath)
    else:
        pass
    pass

# 获取当前日期
def getCurDate():
    return time.strftime("%Y%m%d", time.localtime())

# 列表去重
def cleanRepeated(lis):
    result = []
    for item in lis:
        if(item not in result):
            result.append(item)
    return result



# 针对哔哩哔哩网站
def getCidBySelenium(browser, url):
    browser.get(url)
    time.sleep(1)
    js = 'return cid'  # js语句
    cid = browser.execute_script(js)  # 执行js的方法
    return cid

# 下载视频
def downVideo(urlpath, name, dstDirPath, headers_):
    # 获取当前日期
    r = requests.get(urlpath, verify=False, headers=headers_)
    video = r.content       #响应的二进制文件
    with open(dstDirPath + str(name) + '.mp4','wb') as f:     #二进制写入
        f.write(video)
    r.close()   # 关闭很重要，确保不要过多的连接

def cleanTitle(title):
    return title.replace('&quot;', '').replace(' ', '')
