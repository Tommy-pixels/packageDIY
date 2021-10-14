'''
    进行数据库的操作
'''
import pymysql

class dbOperator():
    def __init__(self, databaseName, user='root', passwd='root'):
        self.databaseName = databaseName
        self.user = user
        self.passwd = passwd
        self.openDB()
        pass

    def openDB(self):
        self.conn = pymysql.connect(
            host='localhost',
            user=self.user,
            passwd=self.passwd,
            db=self.databaseName,
            autocommit=True
        )
        self.cursor = self.conn.cursor()
        pass

    def getAllDataFromDB(self, sql):
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            # 将数据转换成列表
            result = []
            for item in data:
                result.append(
                    [
                        item[i] for i in range(len(item))
                    ]
                )
            return result
        except Exception as e:
            print(e)
            return -1

    def getOneDataFromDB(self, sql):
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchone()
            # 查找不到的话返回None
            return data
        except Exception as e:
            # 报错才返回-1
            print(e)
            return -1

    def insertData2DB(self, sql):
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print(e)
            return -1

    def closeDb(self):
        self.cursor.close()
        self.conn.close()
        pass
