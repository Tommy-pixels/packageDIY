'''
    自动执行脚本
        根据参数选择对应的执行引擎
'''
import subprocess
import os
import datetime
import threading
import inspect, time
import ctypes
from . import run_auto_keyParagraph as rakp
from . import run_auto_relativeParagraph as rarp
from . import run_auto_contentImgs as raci
from . import run_auto_thumbnailImgs as rati
from .articlesRef.DatabaserOperator import databaseOperator as dbOp
from . import run_auto_video as rav
# 1. 定时任务基类 (完成)
class TimedTaskBasic():
    '''
        定时任务的类
            taskExcuteDelta     任务的执行间隔 比如 8点到9点间每隔几秒执行一次任务
            timeExcuteDelta=86400     定时器的执行间隔 比如 每个一周运行一次定时器 86400为一天
    '''
    def __init__(self, setting, beginTime=8, endTime=9, taskExcuteDelta=3600, timeExcuteDelta=86400):
        self.setting = setting  # 定时任务配置文件
        self.beginTime = beginTime  # 定时任务每天的启动时间 例子早上8点 08:00:00
        self.endTime = endTime  # 定时任务执行在几点之前 例子早上9点 09:00:00
        self.taskExcuteDelta = taskExcuteDelta  # 定时任务间隔几秒执行一次
        self.timExcuteDelta = timeExcuteDelta

    #任务描述：每天早上8点，隔3600秒执行一次task任务
    def func1(self):
        '''早上8点开启任务'''
        self.func2()
        # 每隔一天（86400秒）执行一次func1
        t = threading.Timer(self.timExcuteDelta,self.func1)
        t.start()

    def func2(self):
        '''8点-9点，隔3600秒执行一次任务task'''
        self.task()
        # 凌晨4点函数结束执行
        now_time = datetime.datetime.now()
        today_9 = datetime.datetime.strptime(str(datetime.datetime.now().year)+'-'+str(datetime.datetime.now().month)+'-'+str(datetime.datetime.now().day) + ' ' + str(self.endTime) ,'%Y-%m-%d %H:%M:%S')
        #因为定时任务会延后10秒钟执行，所以设置终止条件时，需要提前10秒钟
        print(today_9)
        print(now_time <= today_9-datetime.timedelta(seconds=10))
        if(now_time <= today_9-datetime.timedelta(seconds=10)):
            print("进入了定时判断")
            t = threading.Timer(self.taskExcuteDelta, self.func2)
            t.start()

    def task(self, setting):
        '''需要执行的任务'''
        print(' ---------- task任务开始执行 ---------- ')
        print("本定时器未设置定时任务内容")
        time.sleep(1)
        print(' ---------- task任务执行完毕 ---------- ')

    # 任务自动执行启动
    def timedTaskRun(self):
        #获取当前时间
        now_time = datetime.datetime.now()

        #获取当前时间年、月、日
        now_year = now_time.year
        now_month = now_time.month
        now_day = now_time.day

        #今天早上8点时间表示
        # today_8 = datetime.datetime.strptime(str(now_year)+'-'+str(now_month)+'-'+str(now_day)+' '+'08:00:00','%Y-%m-%d %H:%M:%S')
        today_8 = datetime.datetime.strptime(str(now_year)+'-'+str(now_month)+'-'+str(now_day)+' ' + str(self.beginTime),'%Y-%m-%d %H:%M:%S')
        #明天早上8点时间表示
        tomorrow_8 = datetime.datetime.strptime(str(now_year)+'-'+str(now_month)+'-'+str(now_day)+' ' + str(self.beginTime),'%Y-%m-%d %H:%M:%S')

        #判断当前时间是否过了今天凌晨3点,如果没过，则今天早上8点开始执行，过了则从明天早上8点开始执行，计算程序等待执行的时间
        if(now_time <= today_8):
            wait_time = (today_8 - now_time).total_seconds()
        else:
            wait_time = (tomorrow_8 - now_time).total_seconds()

        #等待wait_time秒后（今天早上8点或明天早上8点），开启线程去执行func函数
        self.thread = threading.Timer(wait_time,self.func1)    # 当前线程
        self.thread.start()

# 2. 定时任务 ———— 爬取数据的的类
class TimedTask4Spider(TimedTaskBasic):
    def task(self):
        '''
        setting = {
            "spiderPath": "E:\\Projects\\Crawl_Dealwith_Post_Auto\\stocksNameCode_Crawl_Auto\\stocksNameCode_Crawl_Auto",
            "spiderName": "StcockNameCodeSpider",
            "command": "Scrapy crawl StcockNameCodeSpider",
            "beginTime": '08:00:00',  # 注意表示 一位数字的要0开头
            "endTime": '09:00:00',
            "excuteDelta": 3600  # 间隔1h 也就是说一天执行一次
        }
        '''
        # 通过os改变工作路径,注意路径是绝对路径，而且还要是\\  只要环境是同一个 这样可以执行对应的爬虫项目
        os.chdir(self.setting['spiderPath'])
        subprocess.Popen(self.setting['command'])


# 结束线程的类没有用到
class StopThread():
    '''结束线程的类'''
    def _async_raise(self,tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if(not inspect.isclass(exctype)):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if(res == 0):
            raise ValueError("invalid thread id")
        elif(res != 1):
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    # 任务自动执行结束 结束本线程实例，在调用本方法之前得先调用 timedTaskRun()
    def stopCurThread(self, thread):
        self._async_raise(thread.ident, SystemExit)


# 2. 定时任务 ———— 处理数据及上传 段落数据 到接口的类（完成）
class TimedTask4AutoDealwithPost(TimedTaskBasic):
    def task(self):
        '''
        setting = {
            "beginTime": '08:00:00',  # 注意表示 一位数字的要0开头
            "endTime": '09:00:00',
            "excuteDelta": 3600,  # 间隔1h 也就是说一天执行一次
            "whichKind" : 'keyParagraph'
        }
        '''
        if(self.setting["whichKind"] == 'keyParagraph'):
            rakp.run(setting=self.setting)
        elif(self.setting["whichKind"] == 'relativeParagraph'):
            rarp.run(setting=self.setting)
        elif(self.setting["whichKind"] == 'contentImgs'):
            raci.run(proj_absPath=self.setting["proj_absPath"], oriDomain=self.setting["oriDomain"], database=self.setting['dbName'], tableNameList=self.setting['tableName'])
        elif(self.setting["whichKind"] == 'thumbnailImgs'):
            rati.run(proj_absPath=self.setting["proj_absPath"], oriDomain=self.setting["oriDomain"], database=self.setting['dbName'], tableNameList=self.setting['tableName'])
        elif(self.setting["whichKind"]=='video'):
            rav.run_bilibili(setting=self.setting)

# 3. 定时任务 ———— 数据库对应上传过的数据清除的类
class TimedTask4AutoClearDB(TimedTaskBasic):
    def task(self, setting):
        '''
        setting = {
            "beginTime": '08:00:00',  # 注意表示 一位数字的要0开头
            "endTime": '09:00:00',
            "excuteDelta": 3600,  # 间隔1h 也就是说一天执行一次
            "whichKind": 'keyParagraph',
            "databaseName" : ['stocksnamecode'],   # 对应的数据库名列表
            "tableName" : ['tb_namecode']    # 待清空的表名
        }
        '''
        if(setting['whichKind'] == 'keyParagraph' or setting['whichKind'] == 'relativeParagraph'):
            # 处理的是段落相关的表
            for table in setting['tableName']:
                # 1 创建并复制数据库表到指定的用于存放上传过的数据内容的库中
                # sql4copy2postedDB = "CREATE TABLE `postedurldatabase`.`tb_article_posted` as select * from `anxinscdatabase`.`tb_articleinfo` where 1=1;"
                # sql4copy2tb_posted = "insert  into `postedurldatabase`.`tb_article_posted`(paragraph, url, hasTag) select paragraph, url, hasTag from `{}`.`tb_articleinfo`;".format(
                #     setting["databaseName"]
                # )
                # 2 清空数据库表的sql
                sql4truncate = "TRUNCATE `{}`.`{}`;".format(
                    setting["databaseName"],
                    table
                )

                dbOperator = dbOp.dbOperator(setting["databaseName"])
                # 清空表之前先复制的操作已经放在了上传数据完成的后面
                # dbOperator.cursor.execute(sql4copy2tb_posted)
                dbOperator.cursor.execute(sql4truncate)
            dbOperator.closeDb()
        elif(setting['whichKind'] == 'thumbnailImgs'):
            # 处理的是缩略图相关的表
            for table in setting['tableName']:
                # 1 创建并复制数据库表到指定的用于存放上传过的数据内容的库中
                sql4copy2tb_posted = "insert  into `postedurldatabase`.`tb_thumbnailimgs_posted`(`dateline`, `formatDate`, `origin_pic_path`, `pic_path`, `title`, `user_name`, `user_uid`, `user_avatar`) select paragraph, `dateline`, `formatDate`, `origin_pic_path`, `pic_path`, `title`, `user_name`, `user_uid`, `user_avatar` from `{}`.`{}`;".format(
                    setting["databaseName"],
                    table
                )
                # 2 清空数据库表的sql
                sql4truncate = "TRUNCATE `{}`.`{}`;".format(
                    setting["databaseName"],
                    table
                )
                # 清空表之前先复制
                dbOperator = dbOp.dbOperator(setting["databaseName"])
                dbOperator.cursor.execute(sql4copy2tb_posted)
                dbOperator.cursor.execute(sql4truncate)
            dbOperator.closeDb()
        elif (setting['whichKind'] == 'contentImgs'):
            # 处理的是缩略图相关的表
            for table in setting['tableName']:
                # 1 创建并复制数据库表到指定的用于存放上传过的数据内容的库中
                sql4copy2tb_posted = "insert  into `postedurldatabase`.`tb_contentimgs_posted`(`dateline`, `formatDate`, `origin_pic_path`, `pic_path`, `title`, `user_name`, `user_uid`, `user_avatar`) select paragraph, `dateline`, `formatDate`, `origin_pic_path`, `pic_path`, `title`, `user_name`, `user_uid`, `user_avatar` from `{}`.`{}`;".format(
                    setting["databaseName"],
                    table
                )
                # 2 清空数据库表的sql
                sql4truncate = "TRUNCATE `{}`.`{}`;".format(
                    setting["databaseName"],
                    table
                )
                # 清空表之前先复制
                dbOperator = dbOp.dbOperator(setting["databaseName"])
                dbOperator.cursor.execute(sql4copy2tb_posted)
                dbOperator.cursor.execute(sql4truncate)
            dbOperator.closeDb()

        elif(setting['whichKind'] == 'video'):
            # 处理视频相关的表
            for table in setting['tableName']:
                # 2 清空数据库表的sql
                sql4truncate = "TRUNCATE `{}`.`{}`;".format(
                    setting["databaseName"],
                    table
                )
                # 清空表之前先复制
                dbOperator = dbOp.dbOperator(setting["databaseName"])
                dbOperator.cursor.execute(sql4truncate)
            dbOperator.closeDb()

if(__name__ == '__main__'):
    '''
        下面是对股票代码数据的爬取流程自动化操作
    '''
    setting4Spider = {
        "spiderPath": "E:\\Projects\\Crawl_Dealwith_Post_Auto\\stocksNameCode_Crawl_Auto\\stocksNameCode_Crawl_Auto",
        "spiderName": "StcockNameCodeSpider",
        "command": "Scrapy crawl StcockNameCodeSpider",
        "beginTime" : '08:00:00', # 注意表示 一位数字的要0开头
        "endTime" : '09:00:00',
        "excuteDelta" : 3600  # 间隔1h 也就是说一天执行一次
    }
    setting4AutoDP = {
        "beginTime": '08:00:00',  # 注意表示 一位数字的要0开头
        "endTime": '09:00:00',
        "excuteDelta": 3600,  # 间隔1h 也就是说一天执行一次
        "whichKind": 'keyParagraph'
    }
    setting4AutoCDB = {
        "beginTime": '08:00:00',  # 注意表示 一位数字的要0开头
        "endTime": '09:00:00',
        "excuteDelta": 3600,  # 间隔1h 也就是说一天执行一次
        "whichKind": 'keyParagraph',
        "databaseName" : 'stocksnamecode',   # 对应的数据库名
        "tableName" : 'tb_namecode'    # 待清空的表名
    }

    # 创建定时任务器 -- Spider任务
    timedTask1_Spider = TimedTask4Spider(setting=setting4Spider, beginTime=setting4Spider["beginTime"], endTime=setting4Spider["endTime"], excuteDelta=setting4Spider["excuteDelta"])
    timedTask1_Spider.task(setting=setting4Spider)
    timedTask1_Spider.timedTaskRun()

    # 2 定时器 ———— 处理和上传数据
    timedTask1_autoDP = TimedTask4AutoDealwithPost()
    timedTask1_autoDP.task(setting=setting4AutoDP)
    timedTask1_autoDP.timedTaskRun()

    # 3 定时器 ———— 删除数据库对应上传完成的数据
    timedTask1_autoCDB = TimedTask4AutoClearDB()
    timedTask1_autoCDB.task(setting=setting4AutoCDB)
