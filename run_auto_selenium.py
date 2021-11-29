from .globalTools import globalTools
from .videoRef.universalTools import tools
from .videoRef.Spider import bySelenium



# Selenium 爬取 爬取视频源 抖音
def run_douyin(proj_absPath, crawlUrl_list, oriDomain='douyin'):
    updateTime = tools.getCurDate()
    videoDirPath = proj_absPath + '\\assets\\videos\\' + updateTime + '\\' + oriDomain + '\\'
    coverSavedPath = proj_absPath + '\\assets\\videos\\' + updateTime + '\\cover_douyin.jpg'
    captchaPath = proj_absPath + '\\assets\\captcha\\' + updateTime + '\\' + oriDomain + '\\'
    # 判断配置里的目录是否存在，不存在则创建对应目录
    tools.checkACreateDir(videoDirPath)
    tools.checkACreateDir(captchaPath)

    # 抖音视频的爬取及上传
    spider_douyin = bySelenium.crawler_Douyin(captchaPath=captchaPath, videoDirPath=videoDirPath)
    for url in crawlUrl_list:
        lis = spider_douyin.enterIndexDouyin(move2BottomTimes=1, douyinUrlIndex=url)
        print("可上传的视频数量：", len(lis))
        print("可上传的视频：", lis)
        spider_douyin.getRealVideo(lis, videoDirPath, coverSavedPath)
    spider_douyin.browser0.close()
    spider_douyin.browser1.close()
    globalTools.finishTask()
