'''
    自动化引擎
        内容图 清洗 筛选 并上传
'''
from .globalTools import globalTools
from .imagesRef.Poster import Poster
from .imagesRef.universalTools import tools
from .imagesRef.Classifier import Classifier
from .imagesRef.Filter import Filter
from .imagesRef.DatabaserOperator import databaseOperator as dbOp
from .imagesRef.Processing import Processing

def run(proj_absPath, oriDomain, database, tableNameList, maskFilt=False):
    updateTime = tools.getCurDate()
    '''
    oriDomain = 'huxiu'
    '''
    setting = {
        # 爬取下来的图片的存放路径
        'imgsCrawledDir': proj_absPath + '\\assets\imgsCrawled\\' + updateTime + '\\' + oriDomain + '\\',
        # 经过百度识别重命名后存放的目录路径
        'imgsReconizedDir': proj_absPath + '\\assets\imgsReconized\\' + updateTime + '\\' + oriDomain + '\\',
        # 初步处理过后的无水印的图片的目录
        'imgsDirDontHasWaterMask': proj_absPath + '\\assets\imgsDontHasWaterMask\\' + updateTime + '\\' + oriDomain + '\\',
        # 初步处理过后有水印的图片的目录
        'imgsDirHasWaterMask': proj_absPath + '\\assets\imgDirHasWaterMask\\' + updateTime + '\\' + oriDomain + '\\',
        # 处理完成的图片目录
        'imgsCleanedDir': proj_absPath + '\\assets\imgsCleanedDir\\' + updateTime + '\\' + oriDomain + '\\',
        # 缩略图保存位置图片目录
        'imgsThumbnailDir': proj_absPath + '\\assets\imgsThumbnailDir\\' + updateTime + '\\' + oriDomain + '\\',
    }

    # 判断配置里的目录是否存在，不存在则创建对应目录
    for item in setting.values():
        tools.checkACreateDir(item)

    # 从数据库获取图片链接 下载图片
    print("从数据库获取图片链接")
    dbOperator = dbOp.dbOperator(database)
    # 上传过的图片去重
    picList_posted_ = dbOperator.getAllDataFromDB("SELECT `origin_pic_path` FROM `postedurldatabase`.`tb_contentimgs_posted`")
    picList_posted = []
    for item in picList_posted_:
        picList_posted.append(item[0])
    print(picList_posted)
    print("下面开始下载图片")
    for table in tableNameList:
        sql = "SELECT `id`,`origin_pic_path` FROM `" + table + "`;"
        imgUrlPathList = dbOperator.getAllDataFromDB(sql)
        print("数据表为 ", table, "获得图片链接数量： ", len(imgUrlPathList))
        for imgUrl in imgUrlPathList:
            if (imgUrl[1] in picList_posted):
                continue
            imgName = table + "_" + str(imgUrl[0])
            tools.downimg(urlpath=imgUrl[1], imgname=imgName, dstDirPath=setting["imgsCrawledDir"])
            insert_SQL = "INSERT INTO `postedurldatabase`.`tb_contentimgs_posted` (`origin_pic_path`) VALUES (\'{}\');".format(
                imgUrl[1])
            dbOperator.insertData2DB(insert_SQL)

    print("图片下载完成")

    # 对爬取下来的图片进行处理 - 识别重命名、过滤、水印的识别及裁切 处理完后放在路径  ./assets/imgsCleanedDir 下
    # 2 重命名
    classifier = Classifier.imgsClassifier(crawledDirPath=setting['imgsCrawledDir'], savedDirPath=setting['imgsReconizedDir'])
    classifier.run()

    # 3 过滤 (关键词过滤、空文件过滤、水印识别及处理）
    print("下面开始过滤操作")
    filter = Filter.imgsFilter(
        imgsDontHasWaterMaskDir=setting['imgsDirDontHasWaterMask'],
        imgDirHasWaterMask=setting['imgsDirHasWaterMask'],
        imgCleanedStep1=setting['imgsCleanedDir'],
        dirOriPath=setting['imgsReconizedDir']
        # dirOriPath=setting['imgsCrawledDir']
    )
    if(maskFilt):
        filter.run()  # 这里再做一下优化
    else:
        filter.run_nomaskOp()
    print("过滤操作完成")

    # 4 resize指定目录下的图片 默认为宽度小1000
    setImgSizer = Processing.ImgsSetSize(setting['imgsCleanedDir'])
    setImgSizer.resize_byDir()

    # 5 创建图片发送的poster 传送处理完成的图片
    # 传送内容图
    imgposter0 = Poster.ImgPoster(imgDirPath=setting['imgsCleanedDir'])
    imgposter0.updateImgs()
    globalTools.finishTask()
