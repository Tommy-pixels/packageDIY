'''
    自动化引擎
        视频 筛选 并上传
'''
from .globalTools import globalTools
from .videoRef.universalTools import tools
from .videoRef.Spider import bySelenium
from .videoRef.DatabaserOperator import databaseOperator as dbOp
from .videoRef.Poster.Poster import VideoPoster
from .videoRef.Filter.Filter import videoFilter
from fake_useragent import UserAgent

def run_bilibili(setting):
    dbOperator = dbOp.dbOperator('bilibilidatabase')    # 获取未上传的数据
    posted_dbOp = dbOp.dbOperator(databaseName='postedurldatabase')     # 连接上传过的的数据的数据库
    poster = VideoPoster(videoDirPath='E:\\test\\')
    filter_video = videoFilter()
    # 获取最新爬取下来待上传的视频信息列表
    sql = "SELECT title, avValue, videoUrl, pubdate FROM `bilibilidatabase`.`tb_videoInfo`;"
    videoInfoList = dbOperator.getAllDataFromDB(sql)    # 未上传的数据

    i = 1

    # 获取上传过的视频title列表
    titlePostedList = posted_dbOp.getAllDataFromDB("SELECT `title` FROM `postedurldatabase`.`tb_video_posted`;")
    titlePostedList_ = []
    for one in titlePostedList:
        titlePostedList_.append(one[0])
    # checkDate_time = int(tools.getSecondByDate(tools.getCurDate() + ' 00:00:00'))
    # checkDate_time = int(tools.getSecondByDate("20210924 12:16:52"))    # 最近一次上传的最新的一个视频的时间戳
    checkDate_time = int(dbOperator.getOneDataFromDB("SELECT * FROM `bilibilidatabase`.`tb_posted_timethenewest`;")[1])

    # 过滤标题操作
    videoInfoList = filter_video.filter_keywordFromTitle(videoInfoList)
    if(videoInfoList):
        checkIfSuccess = False
        newestPubdate = checkDate_time  # 上传成功的最近的一次pubdate`bilibilidatabase`.`tb_posted_timethenewest` SET `timethenewest`
        for item in videoInfoList:
            if(int(item[3]) > checkDate_time and item[0] not in titlePostedList_):
                refererUrl = 'https://www.bilibili.com/video/av' + str(item[1])
                vid_headers = {
                    'Origin': 'https://www.bilibili.com',
                    'Referer': refererUrl,
                    'User-Agent':  str(UserAgent().random)
                }
                try:
                    # 视频数据发布时间在当天
                    tools.downVideo(urlpath=item[2], name=str(i), dstDirPath="E:\\test\\", headers_=vid_headers)
                    checkIfSuccess = True
                except Exception as e:
                    checkIfSuccess = False
                    print("视频下载出错: ", item)

                if(not checkIfSuccess):
                    # 视频下载出错都不用上传了直接跳过
                    continue

                # 上传
                print("上传视频: ", i)
                try:
                    postResult = poster.post_videoSingle(str(i) + '.mp4', title0=item[0])
                    newestPubdate = int(item[3])   # 对应上传视频的时间戳
                except Exception as e:
                    checkIfSuccess = False
                    print("视频上传出错: ", postResult)
                finally:
                    try:
                        # 上传完删除对应单个视频
                        if(i!=1):
                            globalTools.delVideoSingle('E:\\test\\' + str(i-1) + '.mp4')
                    except Exception as e:
                        print("删除上个视频出错： ", str(i-1) + '.mp4')
                        print(e)

                if(checkIfSuccess):
                    # 更新上传过的数据库 postedurldatabase
                    sql = "INSERT INTO `postedurldatabase`.`tb_video_posted` (`title`) VALUES ('{}');".format(
                        item[0]
                    )
                    posted_dbOp.insertData2DB(sql=sql)
                i = i+1
            else:
                print("不符合条件，无法上传")
                print(int(item[3]) > checkDate_time and item[0] not in titlePostedList_)
                print(int(item[3]) > checkDate_time)
                print(item[0] not in titlePostedList_)
                print(titlePostedList_[titlePostedList_.index(item[0])])
                print(item[0])
                continue
        # 上传一切顺利，更新最新上传的视频的时间戳
        sql_update = "UPDATE `bilibilidatabase`.`tb_posted_timethenewest` SET `timethenewest`=\'{}\' WHERE (`id` = '1');".format(
            newestPubdate
        )
        dbOperator.insertData2DB(sql_update)
    else:
        print("数据库为空，无待上传的数据")

    # 上传完成清空存放视频的目录
    globalTools.clearDirFiles('E:\\test\\')
    globalTools.finishTask()

def run():
    updateTime = tools.getCurDate()
    setting = {
        # 爬取下来的图视频的存放路径
        # 'videoCrawledDir': proj_absPath + '\\assets\\viedosCrawled\\' + updateTime + '\\' + oriDomain + '\\'
        'videoCrawledDir': 'E:\\douyinVideos\\'
    }

    # 判断配置里的目录是否存在，不存在则创建对应目录
    for item in setting.values():
        tools.checkACreateDir(item)
    urlList_douyin = [
        "https://www.douyin.com/search/%E8%82%A1?publish_time=1&sort_type=2&source=normal_search&type=video",
        "https://www.douyin.com/search/%E8%82%A1%E7%A5%A8?publish_time=1&sort_type=2&source=normal_search&type=video",
        "https://www.douyin.com/search/%E6%B6%A8%E8%B7%8C?publish_time=1&sort_type=2&source=normal_search&type=video",
        "https://www.douyin.com/search/%E5%A4%A7%E7%9B%98?publish_time=1&sort_type=2&source=normal_search&type=video",
        "https://www.douyin.com/search/B%E8%82%A1?publish_time=1&sort_type=2&source=normal_search&type=video",
        "https://www.douyin.com/search/%E7%9F%AD%E7%BA%BF?publish_time=1&sort_type=2&source=normal_search&type=video",
        "https://www.douyin.com/search/%E6%8C%87%E6%95%B0?publish_time=1&sort_type=2&source=normal_search&type=video"
    ]

    # 抖音视频的爬取及上传
    spider_douyin = bySelenium.crawlFromDouyin()
    for url in urlList_douyin:
        lis = spider_douyin.enterIndexDouyin(move2BottomTimes=1000, douyinUrlIndex=url)
        postResult = spider_douyin.getRealVideo(lis)
    globalTools.finishTask()

