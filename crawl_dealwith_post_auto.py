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
from . import run_auto_comment as rac
from . import run_auto_selenium as ras
from .articlesRef.DatabaserOperator import databaseOperator as dbOp
from . import run_auto_video as rav

# 1. 定时任务基类 (完成)
class TimedTaskBasic():
    '''
        定时任务的类
            taskExcuteDelta     任务的执行间隔 比如 8点到9点间每隔几秒执行一次任务
            timeExcuteDelta=86400     定时器的执行间隔 比如 每个一周运行一次定时器 86400为一天
            beginTime="09:00:00"
            endTime="10:00:00"
            taskExcuteDelta=30
            timeExcuteDelta=86400
    '''
    def __init__(self, setting):
        self.setting = setting  # 定时任务配置文件
        self.beginTime = self.setting['beginTime']  # 定时任务每天的启动时间 例子早上8点 08:00:00
        self.endTime = self.setting['endTime']  # 定时任务执行在几点之前 例子早上9点 09:00:00
        self.taskExcuteDelta = self.setting['taskExcuteDelta']  # 定时任务间隔几秒执行一次
        self.timeExcuteDelta = self.setting['timeExcuteDelta']

    #任务描述：每天早上8点，隔3600秒执行一次task任务
    def func1(self):
        '''早上8点开启任务'''
        self.func2()
        # 每隔一天（86400秒）执行一次func1
        t = threading.Timer(self.timeExcuteDelta,self.func1)
        t.start()

    def func2(self):
        '''8点-9点，隔3600秒执行一次任务task'''
        self.task()
        # 10点函数结束执行
        now_time = datetime.datetime.now()
        today_9 = datetime.datetime.strptime(str(datetime.datetime.now().year)+'-'+str(datetime.datetime.now().month)+'-'+str(datetime.datetime.now().day) + ' ' + str(self.endTime) ,'%Y-%m-%d %H:%M:%S')
        # 因为定时任务会延后10秒钟执行，所以设置终止条件时，需要提前10秒钟
        if(now_time <= today_9-datetime.timedelta(seconds=10)):
            print("当前时间 " + str(now_time) + " ,该时间在任务执行时段内，继续间隔 " + str(self.taskExcuteDelta)  + " 执行任务")
            t = threading.Timer(self.taskExcuteDelta, self.func2)
            t.start()
        else:
            print("当前时间 " + str(now_time) + " ,该时间不在任务执行时段内，等待 " + str(self.timeExcuteDelta) + " 后再重新开启执行任务定时器")

    def task(self):
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

        # 今天早上8点时间表示
        # today_8 = datetime.datetime.strptime(str(now_year)+'-'+str(now_month)+'-'+str(now_day)+' '+'08:00:00','%Y-%m-%d %H:%M:%S')
        today_8 = datetime.datetime.strptime(str(now_year)+'-'+str(now_month)+'-'+str(now_day)+' ' + str(self.beginTime),'%Y-%m-%d %H:%M:%S')
        #明天早上8点时间表示
        tomorrow_8 = datetime.datetime.strptime(str(now_year)+'-'+str(now_month)+'-'+str(now_day)+' ' + str(self.beginTime),'%Y-%m-%d %H:%M:%S')

        # 判断当前时间是否过了今天凌晨8点,如果没过，则今天早上8点开始执行，过了则从明天早上8点开始执行，计算程序等待执行的时间
        if(now_time <= today_8):
            wait_time = (today_8 - now_time).total_seconds()
        else:
            wait_time = (tomorrow_8 - now_time).total_seconds()

        # 等待wait_time秒后（今天早上8点或明天早上8点），开启线程去执行func函数
        self.thread = threading.Timer(wait_time,self.func1)    # 当前线程
        self.thread.start()

# 永久执行任务
class PermanentTask(TimedTaskBasic):
    # 任务描述：永久任务 隔3600秒执行一次task任务
    def func1(self):
        # 该任务设置的
        #   beginTime="00:01:00"
        #   endTime="23:59:00"
        self.func2()


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
            raci.run(proj_absPath=self.setting["proj_absPath"], oriDomain=self.setting["oriDomain"], database=self.setting['databaseName'], tableNameList=self.setting['tableName'])
        elif(self.setting["whichKind"] == 'thumbnailImgs'):
            rati.run(proj_absPath=self.setting["proj_absPath"], oriDomain=self.setting["oriDomain"], database=self.setting['databaseName'], tableNameList=self.setting['tableName'])
        elif (self.setting['whichKind'] == 'video' and self.setting['crawlMethod'] == 'Selenium'):
            ras.run_douyin(proj_absPath=self.setting["proj_absPath"], crawlUrl_list=self.setting['crawlUrl_list'],oriDomain=self.setting["oriDomain"])
        elif(self.setting["whichKind"]=='video' and self.setting['crawlMethod'] == 'Scrapy'):
            rav.run_bilibili(setting=self.setting)
        elif(self.setting["whichKind"]=='articleComment'):
            rac.run(setting=self.setting)
        print("上传数据完成，接下来清空数据库")
        # 上传完直接清空数据库，不用再用定时器
        clearDB = TimedTask4AutoClearDB(setting=self.setting)
        clearDB.task()


# 3. 定时任务 ———— 数据库对应上传过的数据清除的类
class TimedTask4AutoClearDB(TimedTaskBasic):
    def task(self):
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
        if(self.setting['whichKind'] == 'keyParagraph' or self.setting['whichKind'] == 'relativeParagraph' or self.setting['whichKind'] == 'articleComment'):
            # 处理的是段落相关的表
            if(type(self.setting['tableName2Clear'])==str):
                # 传入的等待清空的是表名字符串
                # 2 清空数据库表的sql
                sql4truncate = "TRUNCATE `{}`.`{}`;".format(
                    self.setting["databaseName"],
                    self.setting['tableName2Clear']
                )
                dbOperator = dbOp.dbOperator(self.setting["databaseName"])
                # 清空表之前先复制的操作已经放在了上传数据完成的后面
                # dbOperator.cursor.execute(sql4copy2tb_posted)
                dbOperator.cursor.execute(sql4truncate)
                dbOperator.closeDb()
            else:
                # 传入的等待清空的是表名列表
                for table in self.setting['tableName2Clear']:
                    # 2 清空数据库表的sql
                    sql4truncate = "TRUNCATE `{}`.`{}`;".format(
                        self.setting["databaseName"],
                        table
                    )

                    dbOperator = dbOp.dbOperator(self.setting["databaseName"])
                    # 清空表之前先复制的操作已经放在了上传数据完成的后面
                    # dbOperator.cursor.execute(sql4copy2tb_posted)
                    dbOperator.cursor.execute(sql4truncate)
                dbOperator.closeDb()

        elif(self.setting['whichKind'] == 'thumbnailImgs'):
            if (type(self.setting['tableName2Clear']) == str):
                # 传入的等待清空的是表名字符串
                # 1 清空数据库表的sql
                sql4truncate = "TRUNCATE `{}`.`{}`;".format(
                    self.setting["databaseName"],
                    self.setting['tableName2Clear']
                )
                dbOperator = dbOp.dbOperator(self.setting["databaseName"])
                dbOperator.cursor.execute(sql4truncate)
                dbOperator.closeDb()
            else:
                # 传入的等待清空的是表名列表
                # 处理的是缩略图相关的表
                for table in self.setting['tableName2Clear']:
                    # 2 清空数据库表的sql
                    sql4truncate = "TRUNCATE `{}`.`{}`;".format(
                        self.setting["databaseName"],
                        table
                    )
                    # 清空表之前先复制
                    dbOperator = dbOp.dbOperator(self.setting["databaseName"])
                    dbOperator.cursor.execute(sql4truncate)
                dbOperator.closeDb()

        elif (self.setting['whichKind'] == 'contentImgs'):

            if (type(self.setting['tableName2Clear']) == str):
                # 传入的等待清空的是表名字符串
                # 2 清空数据库表的sql
                sql4truncate = "TRUNCATE `{}`.`{}`;".format(
                    self.setting["databaseName"],
                    self.setting['tableName2Clear']
                )
                # 清空表之前先复制
                dbOperator = dbOp.dbOperator(self.setting["databaseName"])
                dbOperator.cursor.execute(sql4truncate)
                dbOperator.closeDb()
            else:
                # 传入的等待清空的是表名列表
                # 处理的是缩略图相关的表
                for table in self.setting['tableName2Clear']:
                    # 2 清空数据库表的sql
                    sql4truncate = "TRUNCATE `{}`.`{}`;".format(
                        self.setting["databaseName"],
                        table
                    )
                    # 清空表之前先复制
                    dbOperator = dbOp.dbOperator(self.setting["databaseName"])
                    dbOperator.cursor.execute(sql4truncate)
                dbOperator.closeDb()

        elif(self.setting['whichKind'] == 'video'):
            if (type(self.setting['tableName2Clear']) == str):
                # 传入的等待清空的是表名字符串
                # 2 清空数据库表的sql
                sql4truncate = "TRUNCATE `{}`.`{}`;".format(
                    self.setting["databaseName"],
                    self.setting['tableName2Clear']
                )
                # 清空表之前先复制
                dbOperator = dbOp.dbOperator(self.setting["databaseName"])
                dbOperator.cursor.execute(sql4truncate)
                dbOperator.closeDb()
            else:
                # 传入的等待清空的是表名列表
                # 处理视频相关的表
                for table in self.setting['tableName2Clear']:
                    # 2 清空数据库表的sql
                    sql4truncate = "TRUNCATE `{}`.`{}`;".format(
                        self.setting["databaseName"],
                        table
                    )
                    # 清空表之前先复制
                    dbOperator = dbOp.dbOperator(self.setting["databaseName"])
                    dbOperator.cursor.execute(sql4truncate)
                dbOperator.closeDb()

