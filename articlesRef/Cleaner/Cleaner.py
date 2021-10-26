from ..DatabaserOperator import databaseOperator as dbOp
'''
    输入： 段落字符串
    输出： 段落字符串
    清洗这里是通用的
'''
class Cleaner():
    def __init__(self):
        self.filterWord = [
            '●', '但是，', '所以，', '再说，', '虽然说，', '另外，', '最后，', '而且，',
            '其次，', '首先，', '再者，', '同时，', '不过，', '当然，', '当然啦，', '那么，', '虽然，',
            '其实，', '通常，','接着，','综上所述，', '因此，', '、'
        ]
        self.alphabeticList = [
            'A','B','C','D','E','F','G','H'
        ]
        self.numList1 = ['一','二','三','四','五','六','七','八','九','十']
        self.numList2 = ['第一','第二','第三','第四','第五','第六','第七','第八','第九','第十']
        for i in range(1, 10):
            self.filterWord.append(str(i) + '.')
            self.filterWord.append(str(i) + '。')
            self.filterWord.append(str(i) + '，')
            self.filterWord.append(str(i) + '、')
            self.filterWord.append('（' + str(i) + '）')
            self.filterWord.append(str(i) + '）')
            self.filterWord.append('(' + str(i) + ')')
        for item in self.numList1:
            self.filterWord.append(item + '、')
            self.filterWord.append(item + '。')
            self.filterWord.append('(' + item + ')')
        for item in self.numList2:
            self.filterWord.append(item + '、')
            self.filterWord.append(item + '，')
        for item in self.alphabeticList:
            self.filterWord.append(item + '.')
        self.filterWord = tuple(self.filterWord)

        # 从数据库获取股票名字和代码
        sql = "select name, code from `tb_namecode`"
        dbOperator = dbOp.dbOperator('stocksnamecode')
        self.stocksNameCodeList = dbOperator.getAllDataFromDB(sql)
        dbOperator.closeDb()
        del dbOperator

    # 清洗掉空格和结尾的空格
    def delSpace(self, paragraph):
        return paragraph.replace("\r", "").replace("\n", "").replace("\t", "").replace("\xa0", "").replace("\u3000","")

    # 删除开头的序号 如 1. 2. 1、 2、 1， 2，
    def delHeaderNum(self, paragraph):
        for filterword in self.filterWord:
            if(paragraph.startswith(filterword)):
                paragraph = paragraph[len(filterword):]
                break
            # paragraph = paragraph.lstrip(filterword)
        return paragraph

    # 删除股票名字和股票代码
    def delStocksNameAndCode(self, paragraph):
        for item in self.stocksNameCodeList:
            li = []
            li.append(item[0] + "（{}）".format(item[1]))
            li.append("（{}）".format(item[0]))
            li.append("（{}）".format(item[1]))
            li.append(item[0])
            li.append(item[1])
            for stock in li:
                paragraph = paragraph.replace(stock, "")  # 删除股票关键字（包括中文及代买关键字）
        return paragraph

    # 删除杂七杂八的不相关的文字 如： 图9-5
    def delIrrelevantWord(self, paragraph):
        self.irrelevantWordList = ['图']
        for irrelevantWord in self.irrelevantWordList:
            paragraph = paragraph.replace(irrelevantWord, "")
        return paragraph

    # 集成操作方法， 输出的结果为最终清洗完成的结果
    def integratedOp(self, paragraph):
        # 清序号
        temp = self.delHeaderNum(paragraph)
        # 清空格
        temp = self.delSpace(temp)
        # 清序号
        temp = self.delHeaderNum(temp)
        # 清股票
        # temp = self.delStocksNameAndCode(temp)
        # 清不相关的文字
        result = self.delIrrelevantWord(temp)
        return result