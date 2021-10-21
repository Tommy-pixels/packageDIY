import os, time, requests, hashlib
from requests_toolbelt import MultipartEncoder
from ..universalTools import tools
from ..Filter import Filter
from ..DatabaserOperator.databaseOperator import dbOperator as dbOp
from io import TextIOWrapper, BytesIO
'''
    Post 视频的类
        参数：
            videoDirPath  处理完的图片目录路径dir   注意这里的路径最后加\\的

'''


class VideoPoster:
    # 传入的dirPath必须是这样的格式： XX:\\XX\\ 最后是有 \\ 的
    def __init__(self, videoDirPath, interface='http://121.40.187.51:8088/api/videos_api'):
        self.videoDirPath = videoDirPath
        self.get_videoPathList()
        self.interface = interface
        self.userName = 'qin'
        self.password = 'qin123456'
        self.curDate = str(tools.getCurDate())
        self.key = hashlib.md5(('datapool' + self.userName + self.password + self.curDate).encode('utf-8')).hexdigest()
        # self.videoPathFilteredList = videoPathFilteredList

    # 获取目录下所有文件的路径列表
    def get_videoPathList(self):
        videoNameList = os.listdir(self.videoDirPath)  # 获取目录下的所有文件名
        videoPathList = []
        for videoName in videoNameList:
            item = self.videoDirPath + '\\' + videoName
            videoPathList.append(item)
        self.videoNameList = videoNameList
        return videoNameList

    # 获取时间戳
    def getCurTime(self):
        return int(round(time.time()))

    def changeMD5(self, videoSrc):
        with open(videoSrc, 'rb') as f:
            md5 = hashlib.md5(f.read()).hexdigest()
        file = open(videoSrc, 'rb').read()
        with open(videoSrc, 'wb') as new_file:
            new_file.write(file + bytes('\0', encoding='utf-8'))  # here we are adding a null to change the file content
            newMD5 = hashlib.md5(open(videoSrc, 'rb').read()).hexdigest()

    # ndarray图像转换io TextIOWrapper
    def translateFrom_Ndarray2TIWrapper(self, ndFile):
        str_encode = ndFile.tostring()
        # str_encode = np.int64(np.all(ndFile[:, :, :3] == 0, axis=2))
        f4 = BytesIO(str_encode)
        f5 = TextIOWrapper(f4)
        return f5

    # 从数据库获取名字
    def getTitleFromDB(self, titleId):
        dbOperator = dbOp("articledatabase")
        sql = "SELECT videoTitle FROM `tb_videodouyingangang` WHERE `id`={};".format(
            titleId
        )
        title = dbOperator.getOneDataFromDB(sql)[0]
        return title

    def post_videoSingle(self, videoName, title0,coverSavedPath='E:\\cur_Cover.jpg'):
        videoPath = self.videoDirPath + videoName
        print("处理的路径： ", videoPath)
        imgfil = Filter.videoFilter()
        # imgf = self.translateFrom_Ndarray2TIWrapper(imgfil.getCoverImg(videoPath, coverSavedPath))  # 该获取截图的方法无效——无法上传
        # 判断是否满足条件
        if(imgfil.checkIfTimeLength(videoPath)):
            imgfil.getCoverImg(videoPath, coverSavedPath) # 截图并保存
            imgf = open(coverSavedPath, 'rb')
            videof = open(videoPath, 'rb')
            # title = self.getTitleFromDB(videoName.split('.')[0])

            # 这里传文件的时候用绝对路径传，不然传了之后显示不了
            formData = ({
                "key": self.key,
                "account": self.userName,
                "password": self.password,
                'title': tools.cleanTitle(title0),
                'img': ('cover.jpg', imgf, "image/jpeg"),
                'video': (videoName, videof)
            })
            m = MultipartEncoder(formData)
            headers2 = {
                "Content-Type": m.content_type
            }
            videoPostResult = requests.post(url=self.interface, data=m, headers=headers2)
            imgf.close()
            videof.close()
            return videoPostResult

    # 发送目录下的所有所有视频
    def updateVideos(self):
        # for videoName in self.videoNameList:
        #     self.post_videoSingle(videoName)
        for videoName in self.videoNameList:
            self.post_videoSingle(videoName)

