from .globalTools import globalTools
from .videoRef.universalTools import tools
from .videoRef.Spider import bySelenium



# Selenium 爬取 爬取视频源 抖音
def run_douyin(proj_absPath, crawlUrl_list, oriDomain='douyin'):
    updateTime = tools.getCurDate()
    videoDirPath = proj_absPath + '\\assets\\videos\\' + updateTime + '\\' + oriDomain + '\\'
    coverSavedPath = proj_absPath + '\\assets\\videos\\' + updateTime + '\\cover_douyin.jpg'
    # 判断配置里的目录是否存在，不存在则创建对应目录
    tools.checkACreateDir(videoDirPath)
    # 抖音视频的爬取及上传
    spider_douyin = bySelenium.crawlFromDouyin()
    for url in crawlUrl_list:
        lis = spider_douyin.enterIndexDouyin(move2BottomTimes=1, douyinUrlIndex=url)
        postResult = spider_douyin.getRealVideo(lis, videoDirPath, coverSavedPath)
    globalTools.finishTask()
