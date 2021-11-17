import re
from ..DatabaserOperator import databaseOperator as dbOp
from ..Cleaner import Cleaner
'''
    输入： 元组
    输出： 判断结果 布尔值
    注意： 筛选这里根据数据库表结构的不同，筛选方法有所差异
'''
class Filter():
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
        elif(whichKind == 'articleComment'):
            if (len(paragraph) > 45 and len(paragraph) < 250):
                return True
            else:
                return False

    # -> 关联段落判断关键词
    def checkIfHasKeyword_comment(self, paragraph, keyword):
        if(keyword in paragraph):
            # 关键字存在而且段落字数符合要求返回True
            return True
        else:
            return False

    # -> 评论内容的集成操作方法
    def integratedOp4List_comment(self, commentList, keywordList):
        result = []
        cleanerInstance = Cleaner.Cleaner()
        for item in commentList:
            # 1 进行清洗操作(评论不用清洗 去除两边空格就可了)
            item[1] = cleanerInstance.integratedOp_comment(item[1])
            item[1] = item[1].strip('1.').strip('2.').strip('3.').strip('4.').strip('5.').strip('6.').strip('7.').strip('8.').strip()
            for keyword in keywordList:
                # 2 根据字符串长度25-250间进行筛选
                if (not self.filter_BetweenNumberOfWords(item[1], whichKind='articleComment')):
                    # 段落字数再25-250间，有用可传
                    continue
                # 3 对每个段落进行关键词筛选 若有关键词则跳出当前循环
                if (self.checkIfHasKeyword_comment(item[1], keyword)):
                    # 4 根据筛选结果导入可上传的数据
                    result.append(
                        (
                            item[1],  # 评论内容
                            keyword,  # 相关关键词
                        )
                    )
                    break
        return result

class Filter_Posted():
    def __init__(self):
        self.dbOperator = dbOp.dbOperator(databaseName='postedurldatabase')
        self.cleaner = Cleaner.Cleaner()

    # comment 为待处理上传的数据
    def filterPosted(self, comment):
        comment = self.cleaner.integratedOp_comment(comment)
        comment = comment.strip()  # 清除一下左右空格
        sql = "SELECT * FROM `postedurldatabase`.`tb_comment_posted` where `comment` = \'{}\';".format(comment)

        check = self.dbOperator.getOneDataFromDB(sql)
        if(check):
            return True
        else:
            return False

    def run(self, dataOriList):
        result = []
        for item in dataOriList:
            if(not self.filterPosted(comment=item[1])):
                # 没上传过，加入结果
                result.append(item)
        return result
