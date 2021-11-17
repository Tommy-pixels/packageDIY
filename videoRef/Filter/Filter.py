import datetime
import os
from moviepy.editor import VideoFileClip
import cv2
from ..DatabaserOperator import databaseOperator as dbOp

class FileCheck():
    def get_filesize(self, filename):
        u"""
        获取文件大小（M: 兆）
        """
        file_byte = os.path.getsize(filename)
        return self.sizeConvert(file_byte)

    def get_file_times(self, filePath):
        u"""
        获取视频时长（s:秒）
        """
        clip = VideoFileClip(filePath)
        file_time = self.timeConvert(clip.duration)
        return file_time

    def sizeConvert(self, size):  # 单位换算
        K, M, G = 1024, 1024 ** 2, 1024 ** 3
        if size >= G:
            return str(size / G) + 'G Bytes'
        elif size >= M:
            return str(size / M) + 'M Bytes'
        elif size >= K:
            return str(size / K) + 'K Bytes'
        else:
            return str(size) + 'Bytes'

    def timeConvert(self, size):  # 单位换算
        M, H = 60, 60 ** 2
        if size < M:
            return str(size) + u'秒'
        if size < H:
            return u'%s分钟%s秒' % (int(size / M), int(size % M))
        else:
            hour = int(size / H)
            mine = int(size % H / M)
            second = int(size % H % M)
            tim_srt = u'%s小时%s分钟%s秒' % (hour, mine, second)
            return tim_srt


class videoFilter():
    def __init__(self, dirOriPath="E:\Projects\\4spideWeb\\tutorial\\videoDownload\\"):
        self.videoDirPath = dirOriPath  # 存放视频的目录路径
        self.videoNameList = os.listdir(dirOriPath)  # 获取目录下所有图片的名字
        self.checker = FileCheck()
        self.videoPathList = []
        self.dbOperator = dbOp.dbOperator(databaseName='postedurldatabase')
        self.filterwordList = [
            '早评', '午评', '午间点评', '点评', '午间短评', '评述',
            '昨夜', '昨天', '今日', '今天', '明天', '明日', '十年未来',
            '周一', '周二', '周三', '周四', '周五', '周六', '周日', '下周', '本周', '现状', '本月',
            '九月', '十月', '十一月', '十二月', '一月',
            '9月', '10月', '11月', '12月', '1月',
            '华为',
            '板块', '军工', '白酒', '医药', '新能源光伏', '白酒', '煤炭', '电力', '新能源', '科技股', '储能', '光伏', '锂电池概念', '光伏',
            '银行券商',
            '主力拉升', '走势', '大盘', '小幅拉升', '上涨行情', '拉升', '窄幅震荡',
            '值得长期持有', '将迎来', '股价大涨', '再创历史新高', '走强', '反弹'
        ]
        # 股票名
        stocksnamecodeList = self.dbOperator.getAllDataFromDB(sql="SELECT `name` FROM stocksnamecode.tb_namecode;")
        for stock in stocksnamecodeList:
            self.filterwordList.append(stock[0])
        # 获取日期作为过滤关键词
        date_str = str(datetime.date.today()).split('-')
        year = date_str[0]
        month = date_str[1]
        day = date_str[2]
        self.filterwordList.append(year + month + day)
        self.filterwordList.append(month + day)


        def translate(day):
            if (int(day) < 10):
                return '0' + str(day)
            else:
                return str(day)

        self.filterwordList.append(month + str(translate(int(day) - 1)))
        self.filterwordList.append(month + str(translate(int(day) + 1)))
        self.filterwordList.append(month + '.' + day)
        self.filterwordList.append(month + '.' + str(int(day)))
        self.filterwordList.append(month + '.' + str(translate(int(day) - 1)))
        self.filterwordList.append(month + '.' + str(translate(int(day) + 1)))
        self.filterwordList.append(month + '-' + day)
        self.filterwordList.append(month + '月' + day)
        self.filterwordList.append(month + '/' + day)
        self.filterwordList.append(month + '/' + str(translate(int(day) - 1)))
        self.filterwordList.append(day + '日')
        self.filterwordList.append(str(translate(int(day) - 1)) + '日')

        self.filterwordList_bilibili = [
            '第一集', '第七集', '第三课'
        ]
        for i in range(20):
            self.filterwordList_bilibili.append('（' + str(i) + '）')



    # 获取视频文件的封面
    def getCoverImg(self, videoPath, coverSavedPath='E:\\cur_Cover.jpg',frameNum=180):
        # frameNum 没有输入帧数，默认帧数为180
        cap = cv2.VideoCapture(videoPath)  # 读取视频文件
        cap.set(cv2.CAP_PROP_POS_FRAMES, float(frameNum))
        if(cap.isOpened()):  # 判断是否正常打开
            rval, frame = cap.read()
        cv2.imencode('.jpg', frame)[1].tofile(coverSavedPath)
        cover = cv2.imencode('.jpg', frame)[1]
        cap.release()
        return cover

    # 判断视频时间长度是否满足条件 2-5min
    def checkIfTimeLength(self, videoPath):
        timeLength = self.checker.get_file_times(videoPath)
        if('分钟' in timeLength):
            t = int(timeLength.split('分钟')[0])
            if(t>=2 and t<=5):
                # print(timeLength)
                return True
            else:
                # print(timeLength)
                return False
        else:
            # print(timeLength)
            return False

    def filter_time(self):
        filteredNameList = []
        for videoName in self.videoNameList:
            if(self.checkIfTimeLength(videoPath=self.videoDirPath + videoName)):
                filteredNameList.append(videoName)
            else:
                continue
        return filteredNameList

    # 过滤掉上传过的视频
    def filter_posted(self, urlList):
        # 从数据库获取上传过的数据
        postedList = self.dbOperator.getAllDataFromDB("SELECT title, videoUrl FROM `postedurldatabase`.`tb_video_posted`;")
        tempList = []
        if(postedList):
            for postedItem in postedList:
                for item in urlList:
                    if(item[0] == postedItem[0]):
                        tempList.append(item)
                    else:
                        continue
        if(tempList):
            # 待上传的列表中有已上传过的数据，清除上传过的数据
            for item in tempList:
                urlList.remove(item)
        return urlList

    # 快手对于是否当天发布的判断，输入为视频的发布时间 如 5小时前 2天前
    def checkIfCurDatePub_kuaishou(self, str_pub):
        if('小时' in str_pub):
            return True
        else:
            return False

    # 过滤标题关键词
    def filter_keywordFromTitle(self, videoInfoLis):
        fl_videoInfoList = []
        for videoInfo in videoInfoLis:
            check = False
            for keyword in self.filterwordList:
                if (keyword in videoInfo[0]):
                    check = True
            if (videoInfo not in fl_videoInfoList and not check):
                fl_videoInfoList.append(videoInfo)
        return fl_videoInfoList

    # 针对哔哩哔哩的过滤标题关键词
    def filter_keywordFromTitle4bilibili(self, videoInfoLis):
        fl_videoInfoList = []
        for videoInfo in videoInfoLis:
            check = False
            for keyword in self.filterwordList_bilibili:
                if (keyword in videoInfo[0]):
                    check = True
            if (videoInfo not in fl_videoInfoList and not check):
                fl_videoInfoList.append(videoInfo)
        return fl_videoInfoList


# 针对抖音的Filter
class douyinFilter(videoFilter):
    def __init__(self, dirOriPath):
        videoFilter.__init__(self, dirOriPath=dirOriPath)
        douyinFilterWordList = [
            '#搞笑', '#动漫', '#物价'
        ]
        self.filterwordList.extend(douyinFilterWordList)






