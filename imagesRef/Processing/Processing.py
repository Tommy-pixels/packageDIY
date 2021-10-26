from PIL import Image
import os
'''
    将图片转换成缩略图
'''
# 注意这里目录路径的最后要加上 “//”
class Imgs2ThumbnailByDir():
    def __init__(self, thumbnailOriDirPath, thumbnailDstDirPath):
        self.thumbnailOriDirPath = thumbnailOriDirPath
        self.thumbnailDstDirPath = thumbnailDstDirPath
        self.thumbnailOriImgsList = os.listdir(thumbnailOriDirPath)

    def getCutOffWidthandHeight(self, widthOri, heightOri, scaleW=121, scaleH=75):
        widthCheck = 121/75 * heightOri
        i = 0
        while(widthCheck > widthOri):
            i = i + 1
            widthCheck = 121/75 * (heightOri-i)
        return (widthCheck,heightOri-i)

    # 等比例裁切做成缩略图 121：75 定宽
    def cutOff2ThumbnailSingle(self, imgName, srcDirPath, dstDirPath, scaleW=121, scaleH=75):
        imgSrc = srcDirPath + imgName
        print("正在处理的图： ", imgSrc)
        img = Image.open(imgSrc)
        if (img is not None):
            imgSize = img.size
            if (imgSize[1] < 500 and imgSize[0] > imgSize[1]):
                widthOri = imgSize[0]
                heightOri = imgSize[1]
                sizeNew = self.getCutOffWidthandHeight(widthOri=widthOri, heightOri=heightOri)
            elif (imgSize[1] < 500 and imgSize[0] < imgSize[1]):
                widthOri = imgSize[1]
                heightOri = imgSize[0]
                sizeNew = self.getCutOffWidthandHeight(widthOri=widthOri, heightOri=heightOri)
            elif (imgSize[1] >= 500 and imgSize[0] > imgSize[1]):
                # print("图片宽度超过500, 缩放为高度500")
                widthOri = int(imgSize[0] / imgSize[1] * 500)
                heightOri = 500
                img = img.resize((int((imgSize[0] / imgSize[1]) * 500), 500), Image.ANTIALIAS)  # 缩放
                sizeNew = self.getCutOffWidthandHeight(widthOri=widthOri, heightOri=heightOri)
                print(imgName, "  widthOri: ", widthOri, "  heightOri: ", heightOri, "  sizeNew: ", sizeNew)
            elif (imgSize[1] >= 500 and imgSize[0] < imgSize[1]):
                # print("图片宽度超过500, 缩放为高度500")
                widthOri = 500
                heightOri = int(imgSize[0] / imgSize[1] * 500)
                img = img.resize((int((imgSize[0] / imgSize[1]) * 500), 500), Image.ANTIALIAS)  # 缩放
                sizeNew = self.getCutOffWidthandHeight(widthOri=heightOri, heightOri=widthOri)
            box = (0,0,sizeNew[0], sizeNew[1])
            img = img.crop(box)
            img.save(dstDirPath + imgName)

    # 对目录下的所有文件进行缩略图转换并放在缩略图目录下
    def cutOff2ThumbnailByDir(self):
        for imgName in self.thumbnailOriImgsList:
            self.cutOff2ThumbnailSingle(imgName=imgName, srcDirPath=self.thumbnailOriDirPath, dstDirPath=self.thumbnailDstDirPath, scaleW=121, scaleH=75)

class ImgsSetSize:
    def __init__(self, imgsOriDirPath):
        self.imgsOriDirPath = imgsOriDirPath
        self.oriImgNameList = os.listdir(imgsOriDirPath)

    # 获取图片大小
    def get_size(self, imgSrc):
        # 获取文件大小:KB
        size = os.path.getsize(imgSrc)
        return size / 1024

    # 压缩图片到指定大小，尺寸不变
    def compress_image(self, imgName, mb=150, step=1, quality=80, k=0.9):
        """不改变图片尺寸压缩到指定大小
        :param infile: 压缩源文件
        :param outfile: 压缩文件保存地址
        :param mb: 压缩目标，KB
        :param step: 每次调整的压缩比率
        :param quality: 初始压缩比率
        :return: 压缩文件地址，压缩文件大小
        """
        imgSrc = self.imgsOriDirPath + imgName
        o_size = self.get_size(imgSrc)
        if o_size <= mb:
            return imgSrc
        while o_size > mb:
            img = Image.open(imgSrc)
            x, y = img.size
            img = img.resize((int(x*k), int(y*k)), Image.ANTIALIAS)
            img.save(imgSrc, quality=quality)
            if quality - step < 0:
                break
            quality -= step
            o_size = self.get_size(imgSrc)
        return imgSrc, self.get_size(imgSrc)


    # 判断图片宽度是否超过制定长度默认1000，超过则按比例改变宽度为1000，保存原位置
    def resize_singleImg(self, imgName, setWidth=1000):
        imgOriSrc = self.imgsOriDirPath + imgName
        img = Image.open(imgOriSrc)
        if (img is not None):
            imgSize = img.size
            if(imgSize[0] > setWidth and imgSize[0] > imgSize[1]):
                # print("图片宽度超过500, 缩放为高度500")
                widthOri = setWidth
                heightOri = int(imgSize[1] / imgSize[0] * setWidth)
                img = img.resize((setWidth, heightOri), Image.ANTIALIAS)  # 缩放
                img.save(imgOriSrc)
            else:
                pass


    # 把指定目录下的图片resize，覆盖原文件
    def resize_byDir(self):
        for imgName in self.oriImgNameList:
            self.resize_singleImg(imgName, setWidth=1000)
            self.compress_image(imgName)

