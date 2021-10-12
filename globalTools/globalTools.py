import os

# 获取当前根目录路径
def getCurOriPath():
    return os.path.abspath(os.path.dirname(__file__))

# 清洗掉开头空格和结尾的空格
def delSpace(paragraph):
    # return paragraph.replace("\r", "").replace("\n", "").replace("\t", "").replace("\xa0", "").replace("\u3000","")
    return paragraph.strip()

def finishTask():
    print("流程结束，单次任务结束（爬取、处理、上传数据， 对应数据库数据的清空以及posturldatabase数据库的更新）")

# 清空指定目录下所有文件
def clearDirFiles(dirPath):
    lis = os.listdir(dirPath)
    for i in lis:
        os.remove(dirPath + i)

