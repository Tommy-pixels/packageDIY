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
