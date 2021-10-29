import os, time
import hashlib, base64

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

# 删除指定文件
def delVideoSingle(filePath):
    os.remove(filePath)



# 获取当前日期
def getCurDate():
    return time.strftime("%Y%m%d", time.localtime())

# 返回指定日期时间戳 时间格式 '%Y%m%d %H:%M:%S' 20210924 00：00：00 该方法用于哔哩哔哩时间的判断
def getSecondByDate(date):
    b = time.strptime(date, '%Y%m%d %H:%M:%S')
    return time.mktime(b)

# 模拟浏览器打开指定连接并且获取header和cookie并输出
def getCookieandHeader(url):
    pass

# 加密类
class Encode:
    # 同一输出类型为str
    def bytes2str(self, b):
        return str(b, encoding='utf-8')

    def str2bytes(self, s):
        return bytes(s, encoding='utf-8')

    def encodeByMd5(self, s):
        return hashlib.md5(s.encode(encoding='utf-8')).hexdigest()

    # base64输出的为bytes类型 要转化为字符串
    def encodeByBase64(self, s):
        res = base64.encodebytes(s).strip()
        # 转换为字符串
        res = self.bytes2str(res)
        return res

    def encode0(self,s):
        return self.encodeByBase64(self.str2bytes(self.encodeByMd5(s)))

# 目录处理类
class Contraler_Dir:
    # 获取当前根目录路径
    def getCurOriPath(self):
        return os.path.abspath(os.path.dirname(__file__))

    # 判断目录是否存在，不存在则创建
    def checkACreateDir(self,dirPath):
        exist = os.path.exists(dirPath)
        if (not exist):
            os.makedirs(dirPath)
        else:
            pass
        pass

    # 清空指定目录下所有文件
    def clearDirFiles(self, dirPath):
        lis = os.listdir(dirPath)
        for i in lis:
            os.remove(dirPath + i)

# 时间处理类
class Contraler_Time:
    # 获取当前日期
    def getCurDate(self):
        return time.strftime("%Y%m%d", time.localtime())

    # 返回指定日期时间戳 时间格式 '%Y%m%d %H:%M:%S' 20210924 00：00：00 该方法用于哔哩哔哩时间的判断
    def getSecondByDate(self, date):
        b = time.strptime(date, '%Y%m%d %H:%M:%S')
        return time.mktime(b)