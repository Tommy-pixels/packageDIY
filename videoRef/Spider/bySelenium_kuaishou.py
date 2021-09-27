from selenium import webdriver
from time import sleep
import pymysql, time, requests, openpyxl, pyautogui
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from ..Poster.Poster import VideoPoster
from ..Filter.Filter import videoFilter
from ..universalTools import tools
from ..DatabaserOperator import databaseOperator as dbOp



# 已有链接下载的方法
def downVideo(urlpath, name, dstDirPath):
    # 获取当前日期
    r = requests.get(urlpath, verify=False)
    video = r.content       #响应的二进制文件
    with open(dstDirPath + str(name) + '.mp4','wb') as f:     #二进制写入
        f.write(video)
    r.close()   # 关闭很重要，确保不要过多的连接

"""
处理快手视频的封面图片src
"""
class crawlFromKuaishou():
    def __init__(self, url="https://www.kuaishou.com/search/video?searchKey=%E8%82%A1"):
        self.filter = videoFilter()
        option = webdriver.ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_experimental_option('useAutomationExtension', False)
        self.browser = webdriver.Chrome(executable_path="E:\Projects\webDriver\\chrome\\chromedriver.exe",options=option)
        self.browser.get(url)
        self.url = url
        # 登陆验证的
        self.browser.add_cookie({
            "domain": ".kuaishou.com",
            "name": "userId",
            "value": "2560728971",
            "path": '/',
            "expires": None
        })
        # 滑块验证的
        self.browser.add_cookie({
            "domain": ".kuaishou.com",
            "name": "did",
            "value": "web_dd4765fe13d667c461fd6269a10ae0df",
            "path": '/',
            "expires": None
        })
        self.browser.add_cookie({
            "domain": ".www.kuaishou.com",
            "name": "kpf",
            "value": "PC_WEB",
            "path": '/',
            "expires": None
        })
        self.browser.add_cookie({
            "domain": ".www.kuaishou.com",
            "name": "kpn",
            "value": "KUAISHOU_VISION",
            "path": '/',
            "expires": None
        })
        self.browser.add_cookie({
            "domain": ".kuaishou.com",
            "name": "clientid",
            "value": "3",
            "path": '/',
            "expires": None
        })
        self.browser.add_cookie({
            "domain": ".kuaishou.com",
            "name": "client_key",
            "value": "65890b29",
            "path": '/',
            "expires": None
        })
        self.browser.add_cookie({
            "domain": ".kuaishou.com",
            "name": "kuaishou.server.web_ph",
            "value": "f026d92ae2b0265bf86ec666fa786f635d5b",
            "path": '/',
            "expires": None
        })
        self.browser.add_cookie({
            "domain": ".kuaishou.com",
            "name": "kuaishou.server.web_st",
            "value": "ChZrdWFpc2hvdS5zZXJ2ZXIud2ViLnN0EqABWHDql4qaYN0DtvJlDUI2vX9v2hDjf2eJUChEjJHM9YZiNRQRhDkcURY8NFHcPTyo3KaaN9tV-q9kFdDhaa6sLjoDSmhK5UjN2byF-eFVit8lfNtBhKzJ-dtvFTmsotI8eHddsdCisokwNMCBCXzdiwA7fmnM7SKqP3qEsXkJsOZJlJ1-CAUQSCJwVaVaU3SvYCeGb3Vi9BVfw0RtpgCzexoS8JByODRPv5hk-B95zTquvFHcIiCS6UA7jHPQUTMshtZGa63oO8ZPkqrI5c9ylvllsQswiCgFMAE",
            "path": '/',
            "expires": None
        })
        self.poster = VideoPoster(videoDirPath='E:\\test\\')
        print("请先登陆")

    # 获取clientCacheKey
    def getclientCacheKey(self, srcList):
        self.kuaishouSrcListOrigin = srcList
        clientCacheKeyList = []
        videoPageSrcList = []
        for src in self.kuaishouSrcListOrigin:
            if('clientCacheKey' in src):
                clientCacheKey = str(src).split("//")[1].split("clientCacheKey=")[1].split(".")[0]
                if(clientCacheKey not in clientCacheKeyList):
                    # 插入数据库操作
                    self.mySQLDataBaseInsertOp_clientCacheKey(clientCacheKey)
                    clientCacheKeyList.append(clientCacheKey)
            else:
                continue
        self.clientCacheKeyList = clientCacheKeyList
        for item in self.clientCacheKeyList:
            videoPageSrc = 'https://www.kuaishou.com/short-video/' + item
            videoPageSrcList.append(videoPageSrc)
        self.videoPageSrcList = videoPageSrcList
        return clientCacheKeyList

    def mySQLDataBaseInsertOp_clientCacheKey(self, clientCacheKey):
        # 设置数据库
        conn = pymysql.connect(
            host='localhost',
            user="root",
            passwd="root",
            db="articledatabase",
            autocommit=True
        )
        cursor = conn.cursor()
        sql = "INSERT INTO `articledatabase`.`tb_videopeiziclientcachekey` (`clientCacheKey`) VALUES (\'{}\');".format(
            clientCacheKey
        )
        # 执行Sql语句
        try:
            result = cursor.execute(sql)
            if (result == 1):
                # print("插入记录成功")
                pass
        except Exception as e:
            print(sql)
            print("插入记录失败： ", e)

    # 已经获取了clientCacheKey，下面这个方法已经不用了
    def crawlImgSrcBySelenium(self):
        # 1.创建Chrome浏览器对象，这会在电脑上在打开一个浏览器窗口
        # self.browser.get("https://www.kuaishou.com/search/video?searchKey=配资")
        # 2.通过浏览器向服务器发送URL请求
        # cookies = "kpf=PC_WEB; kpn=KUAISHOU_VISION; clientid=3; did=web_77c4eaa79392234fda0830a7abdcb2f7; client_key=65890b29"
        # cookieList = cookies.split(";")
        # for cookie in cookieList:
        #     self.browser.add_cookie({
        #         "domain": ".kuaishou.com",
        #         "name": cookie.split("=")[0],
        #         "value": cookie.split("=")[1],
        #         "path": '/',
        #         "expires": None
        #     })
        self.browser.get(self.url)

        sleep(3)
        element0 = self.browser.find_elements_by_xpath(
            "//div[@class='video-card-main']//div[@class='card-link']/div[@class='poster']/img[@class='poster-img']")
        print(len(element0))
        for item in element0:
            print(item.get_attribute('src'))

        # 下拉到底
        # js = "var q=document.documentElement.scrollTop=20000"
        self.browser.execute_script("""
            (function () {
            var y = 0;
            var step = 100;
            window.scroll(0, 0);
            function f() {
            if (y < document.body.scrollHeight) {
            y += step;
            window.scroll(0, y);
            setTimeout(f, 100);
            } else {
            window.scroll(0, 0);
                document.title += "scroll-done";
            }
            }
            setTimeout(f, 1000);
            })();
            """)
        print("下拉中...")
        time.sleep(2)
        # while (True):
        #     if ("scroll-done" in self.browser.title):
        #         break
        #     else:
        #         print("还没有拉到最底端...")
        #         sleep(3)
        n = 0
        while (n<=10):
            if ("scroll-done" in self.browser.title):
                break
            else:
                print("还没有拉到最底端...")
                sleep(3)
            n = n+1

        element1 = self.browser.find_elements_by_xpath("//div[@class='video-card-main']//div[@class='card-link']/div[@class='poster']/img[@class='poster-img']")
        clientCacheListOrigin = []
        for item in element1:
            clientCacheListOrigin.append(item.get_attribute('src'))
        # 处理爬取到的Src
        self.getclientCacheKey(clientCacheListOrigin)
        # 3.刷新浏览器
        self.browser.refresh()

    # 提取视频名字的方法
    def videoNameExtract(self, videoSrc):
        return str(videoSrc).split("?")[0].split("/")[-1]

    # 获取视频
    def getSingleVideoInfo(self, src):
        self.browser.get(src)
        sleep(3)
        # 获取视频信息
        publishTime = self.browser.find_element_by_xpath("//div[@class='short-video-info']//div[1]//div[@class='title-warp']//span[@class='photo-time']").text
        videoInfo = {}
        if(self.filter.checkIfCurDatePub_kuaishou(publishTime)):
            # 进入这里说明是当天发布的
            author = self.browser.find_element_by_xpath(
                "//div[@class='short-video-info']//div[1]//div[@class='title-warp']//span[@class='profile-user-name-title']").text
            videoTitle = self.browser.find_element_by_xpath("//div[@class='short-video-info-container-detail']/p").text
            videoSrc = self.browser.find_element_by_xpath("//video").get_attribute("src")
            videoName = self.videoNameExtract(videoSrc)
            videoInfo = {
                "author": author,
                "publishTime": publishTime,
                "videoTitle": videoTitle,
                "videoSrc": videoSrc,
                "videoName": videoName
            }
        return videoInfo

    def getVideoListInfo(self):
        videoInfoList = []
        for src in self.videoPageSrcList:
            videoInfo = self.getSingleVideoInfo(src)
            # 获取到视频信息， 开始下载并上传
            downVideo(urlpath=videoInfo['videoSrc'], name=videoInfo['videoName'], dstDirPath='E:\\test\\')
            videoInfoList.append(videoInfo)
            self.mySQLDataBaseInsertOp_videoInfo(videoInfo)
        self.videoInfoList = videoInfoList

    def getVideoListInfoByList(self,lis):
        for src in lis:
            videoInfo = self.getSingleVideoInfo(src)
            if(videoInfo):
                # 进入这里说明是视频是当天发布的，可以下载
                self.mySQLDataBaseInsertOp_videoInfo(videoInfo) # 视频信息放入数据库
                # 下载视频并上传
                downVideo(urlpath=videoInfo['videoSrc'], name=videoInfo['videoName'], dstDirPath='E:\\test\\')
                self.poster.post_videoSingle(videoInfo['videoName'] + '.mp4', title0=videoInfo["videoTitle"])


    def mySQLDataBaseInsertOp_videoInfo(self, videoInfoItem):
        # 设置数据库
        conn = pymysql.connect(
            host='localhost',
            user="root",
            passwd="root",
            db="articledatabase",
            autocommit=True
        )
        cursor = conn.cursor()
        sql = "INSERT INTO `articledatabase`.`tb_videopeizitest` (`title`, `author`, `time`, `videoSrc`, `videoName`) VALUES (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\');".format(
                videoInfoItem["videoTitle"],
                videoInfoItem["author"],
                videoInfoItem["publishTime"],
                videoInfoItem["videoSrc"],
                videoInfoItem["videoName"]
            )
        # 执行Sql语句
        try:
            result = cursor.execute(sql)
            if (result == 1):
               # print("插入记录成功")
               pass
        except Exception as e:
            print(sql)
            print("插入记录失败： ", e)

    def run(self):
        self.crawlImgSrcBySelenium()
        # # 从数据库获取clientCacheKey
        # conn = pymysql.connect(
        #     host='localhost',
        #     user="root",
        #     passwd="root",
        #     db="articledatabase",
        #     autocommit=True
        # )
        # cursor = conn.cursor()
        # sql = "SELECT `clientCacheKey` FROM `articledatabase`.`tb_videopeiziclientcachekey`"
        # # 执行Sql语句
        # try:
        #     cursor.execute(sql)
        #     result = cursor.fetchall()
        # except Exception as e:
        #     pass
        # videoPageSrcList = []
        # for clientCacheKeyItem in result:
        #     videoPageSrc = 'https://www.kuaishou.com/short-video/' + clientCacheKeyItem[0]
        #     videoPageSrcList.append(videoPageSrc)
        self.getVideoListInfoByList(self.videoPageSrcList)
