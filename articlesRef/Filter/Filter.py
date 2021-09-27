import re
from ..DatabaserOperator import databaseOperator as dbOp
from ..Cleaner import Cleaner
'''
    输入： 元组
    输出： 判断结果 布尔值
    注意： 筛选这里根据数据库表结构的不同，筛选方法有所差异
        关键词段落 _keyParagraph
        关联段落 _relativeParagraph
'''
class Filter():
    def __init__(self):
        # 日期相关关键词
        self.dateRefList = [
            '周一', '周二', '周三', '周四','周五', '周六', '周日'
        ]
        # 从数据库获取股票名字和代码
        sql = "select name, code from `tb_namecode`"
        dbOperator = dbOp.dbOperator('stocksnamecode')
        self.stocksNameCodeList = dbOperator.getAllDataFromDB(sql)
        dbOperator.closeDb()
        del dbOperator


    # 输入 段落
    def filter_BetweenNumberOfWords(self, paragraph, whichKind):
        if(whichKind == 'relativeParagraph'):
            if (len(paragraph) > 125 and len(paragraph) < 250):
                return True
            else:
                return False
        elif(whichKind == 'keyParagraph'):
            if (len(paragraph) > 50 and len(paragraph) < 250):
                return True
            else:
                return False

    # 过滤含有股票关键字（中文及对应代码）的段落 输入为段落字符串 输出为布尔值
    def filter_hasStockCode(self, paragraph):
        for stock in self.stocksNameCodeList:
            if(stock[0] in paragraph or stock[1] in paragraph):
                # 含有股票对应名称和代码 返回True
                return True
            return False

    # 过滤掉日期相关的段落 输入为段落字符串 输出为布尔值
    def filter_dateRef(self, paragraph):
        # 利用正则表达式 匹配 ['5:45', '7/10/2017', '3月2日', '98年3月3日', '2019年8月1日', '10月5日']
        # \b 表示边界，加上的话表对应模式的字符串左右两边必须是空格（边界），否则匹配不到
        pattern = re.compile(r'\b\d{2}/\d{2}/\d{4}\b|\b\d{1,2}:\d{1,2}\b|\b\d{1,2}/\d{1,2}/\d{2,4}\b|\d{2,4}年\d{1,2}月\d{1,2}日|\d{1,2}月\d{1,2}日')  # 定义匹配模式
        for date in self.dateRefList:
            if (date in paragraph):
                # 含有日期相关的关键字 返回True
                return True
            elif(re.findall(pattern, paragraph)):
                return True
            return False

    # 输入 元组
    def filter_hasTag_keyParagraph(self, item):
        if (item[3] == 'False'):
            return False
        else:
            return True


    def integratedOp_keyParagraph(self, item):
        # 先判断是否有标签，有标签才进行后面的判断
        if(self.filter_hasTag_keyParagraph(item)):
            # 有标签 接着判断字数在120-250间
            return self.filter_Between120to250(item[1])
        else:
            # 无标签 输出False
            return False

    # -> 关联段落判断关键词
    def checkIfHasKeyword_relativeParagraph(self, paragraph, keyword):
        if(keyword in paragraph):
            # 关键字存在而且段落字数符合要求返回True
            return True
        else:
            return False


    # 输入的列表为从数据库获取的列表, 输出的列表为 最终过滤完成输出 可以上传的列表(指定好了格式)  -> 关键词段落的集成操作方法
    def integratedOp4List_keyParagraph(self, paragraphList, databaseName, tableName, tableName4Tag, tagRefSqlKind='id'):
        result = []
        cleanerInstance = Cleaner.Cleaner()
        dbOperator = dbOp.dbOperator(databaseName=databaseName)
        for item in paragraphList:
            # 筛选有标签的
            if (self.filter_hasTag_keyParagraph(item)):
                # 进行清洗操作
                item[1] = cleanerInstance.integratedOp(item[1])
                # 筛选判断 ： 1 字符串长度不在125-250之间；2 段落含有股票名或代码 3 段落包含日期关键词
                ##          但凡满足上面任何一个的段落筛选条件的段落都过滤掉
                check = (not self.filter_BetweenNumberOfWords(item[1], whichKind='keyParagraph')) or self.filter_hasStockCode(item[1]) or self.filter_dateRef(item[1])
                if(check):
                    # 进入该判断条件说明对应段落无效跳过， 因此希望有效段落的check最终为false
                    continue
                if(tagRefSqlKind=='id'):
                    sql = "SELECT `tag_origin` FROM " + databaseName + "." + tableName4Tag + " WHERE `id`=" + str(
                        item[2]) + ";"
                elif(tagRefSqlKind=='url'):
                    sql = "SELECT `tag_origin` FROM " + databaseName + "." + tableName4Tag + " WHERE `url`='" + str(
                        item[2]) + "';"
                result.append(
                    (
                        item[1],  # 段落内容
                        dbOperator.getOneDataFromDB(sql)[0],  # 段落关键词
                    )
                )
            else:
                continue
        dbOperator.closeDb()
        del dbOperator
        return result

    # -> 关联段落的集成操作方法
    def integratedOp4List_relativeParagraph(self, paragraphList, keywordList):
        result = []
        cleanerInstance = Cleaner.Cleaner()
        for item in paragraphList:
            # 1 进行清洗操作
            item[1] = cleanerInstance.integratedOp(item[1])
            for keyword in keywordList:
                # 2 根据字符串长度125-250间进行筛选
                if (not self.filter_BetweenNumberOfWords(item[1], whichKind='relativeParagraph')):
                    # 段落字数再125-250间，有用可传
                    continue
                # 3 对每个段落进行关键词筛选 若有关键词则跳出当前循环
                if (self.checkIfHasKeyword_relativeParagraph(item[1], keyword)):
                    # 4 根据筛选结果导入可上传的数据
                    result.append(
                        (
                            item[1],  # 段落内容
                            keyword,  # 相关关键词
                        )
                    )
                    break
        return result

class Filter_Posted():
    def __init__(self):
        self.dbOperator = dbOp.dbOperator(databaseName='postedurldatabase')

    # paragraph 为待处理上传的数据
    def filterPosted(self,paragraph):
        paragraph = paragraph.strip()  # 清除一下左右空格
        sql = "SELECT * FROM `postedurldatabase`.`tb_article_posted` where `paragraph` = \'{}\';".format(paragraph)

        check = self.dbOperator.getOneDataFromDB(sql)
        if(check):
            # 上传过130 12
            return True
        else:
            return False

    def run(self, dataOriList):
        result = []
        for item in dataOriList:
            if(not self.filterPosted(paragraph=item[1])):
                # 没上传过，加入结果
                result.append(item)
        return result
