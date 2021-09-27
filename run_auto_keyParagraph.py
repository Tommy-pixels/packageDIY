'''
    自动化引擎
        从关键段落数据库中获取数据 进行 清洗 筛选 并上传 （已完成）
'''
from .articlesRef.DatabaserOperator import databaseOperator as dbOp
from .articlesRef.Filter import Filter
from .articlesRef.Poster import Poster

def run(setting):
    # setting = {
    #     'databaseName': 'magicsunshadingdatabase',
    #     'databaseUser': 'root',
    #     'databasePasswd': 'root',
    #     'tableName': 'tb_articlecontent',
    #     'tableName4Tag': 'tb_articleinfo',
    #     'tagRefSqlKind': 'url',
    #     'domain' : 'magicsunshading'
    # }

    if(setting['domain'] == 'peizitoutiao'):
        for topicName in setting['topicNameList']:
            tableName = 'tb_' + topicName + '_articlecontent'
            tableName4Tag = 'tb_' + topicName + '_articleinfo'
            setting['tableName'] = tableName
            setting['tableName4Tag'] = tableName4Tag
            setting['sql'] = "SELECT * FROM " + setting['databaseName'] + "."+ setting['tableName'] +";"
            # 1 获取对应数据
            dbOperator = dbOp.dbOperator(databaseName=setting['databaseName'], user=setting['databaseUser'], passwd=setting['databasePasswd'])
            dataList = dbOperator.getAllDataFromDB(setting['sql'])

            # 2 对所有段落内容判断，若上传过则删除对应上传过的段落
            filter4postedcheck = Filter.Filter_Posted()
            dataList = filter4postedcheck.run(dataList=dataList)

            # 3 过滤操作 输入的列表为从数据库中获取的列表（过滤操作包含清洗操作，不用单独进行清洗）
            filterInstance = Filter.Filter()
            postableList = filterInstance.integratedOp4List_keyParagraph(
                paragraphList=dataList,
                databaseName=setting['databaseName'],
                tableName=setting['tableName'],
                tableName4Tag=setting["tableName4Tag"],
                tagRefSqlKind='url'
            )

            # 5 将上传过的数据放到postedurldatabase中
            postedDBOP = dbOp.dbOperator(databaseName='postedurldatabase', user='root', passwd='root')
            for paragraph in postableList:
                sql = "INSERT INTO `postedurldatabase`.`tb_article_posted` (`paragraph`) VALUES (\'{}\');".format(
                    paragraph[0])
                postedDBOP.insertData2DB(sql)
            print("postedurldatabase 数据库的更新操作完成 流程结束")


    elif(setting['domain'] == 'magicsunshading'):
        print("here is magicsunshading")
        setting['sql'] = "SELECT * FROM " + setting['databaseName'] + "."+ setting['tableName'] +";"

        # 1 获取对应数据
        dbOperator = dbOp.dbOperator(databaseName=setting['databaseName'], user=setting['databaseUser'], passwd=setting['databasePasswd'])
        dataList = dbOperator.getAllDataFromDB(setting['sql'])

        # 2 对所有段落内容判断，若上传过则删除对应上传过的段落
        filter4postedcheck = Filter.Filter_Posted()
        dataList = filter4postedcheck.run(dataOriList=dataList)

        # 3 过滤操作 输入的列表为从数据库中获取的列表（过滤操作包含清洗操作，不用单独进行清洗）
        filterInstance = Filter.Filter()
        postableList = filterInstance.integratedOp4List_keyParagraph(
            paragraphList=dataList,
            databaseName=setting['databaseName'],
            tableName=setting['tableName'],
            tableName4Tag=setting["tableName4Tag"],
            tagRefSqlKind='url'
        )

        print("过滤操作完成， 接下来完成上传操作")
        # 4 上传列表
        posterInstance = Poster.Poster(interface='http://121.40.187.51:8088/api/key_paragraph_api')
        posterInstance.post_auto(postableList, whichKind='keyParagraph')

        print("上传操作完成， 接下来完成 postedurldatabase 数据库的更新操作")
        # 5 将上传过的数据放到postedurldatabase中
        postedDBOP = dbOp.dbOperator(databaseName='postedurldatabase', user='root',passwd='root')
        for paragraph in postableList:
            sql = "INSERT INTO `postedurldatabase`.`tb_article_posted` (`paragraph`) VALUES (\'{}\');".format(paragraph[0])
            postedDBOP.insertData2DB(sql)
        print("postedurldatabase 数据库的更新操作完成 流程结束")
