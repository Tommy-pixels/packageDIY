import time


# 获取当前年月日 如： 20210831
def getCurDate():
    return time.strftime("%Y%m%d", time.localtime())