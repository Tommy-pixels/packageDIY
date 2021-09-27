######  下面是关于本库的说明 
######  author : 唐国钦 
######  time : 20210909
######  库功能描述： 定时爬取各个网站的文章段落数据和图片数据，处理之后上传到对应指定接口中，特别注意上传的数据不能重复。爬虫的项目需要单独创建，这里的定时爬虫只是定时运行指定爬虫项目的对应爬虫命令
    
# 一、爬虫自动化流程
## 1、库中包含的类：
        1. 自动化封装的类 ———— 定时器
        2. 段落相关(articlesRef)：
            2.1 段落字符串清洗封装的类
            2.2 段落字符串过滤封装的类
            2.3 段落字符串上传封装的类
            2.4 数据库操作通用封装的类
            2.5 通用的工具库(universalTools)
        3. 图片相关(imagesRef)：
            3.1 图片重命名封装的类(通用物体和场景识别)
            3.2 图片过滤封装的类
            3.3 图片处理相关封装的类
            3.4 图片上传的类
            3.5 数据库操作通用的类（同articlesRef中数据库操作通用封装的类）
            3.6 通用的工具库(universalTools)
        4. 全局通用的工具库(globalTools)
        5. 自动化操作封装的类(run_auto_*.py)
        6. 各个类型定时器封装的类(crawl_dealwith_post_auto.py)
## 2、整个流程
        1. 根据要爬取的网站的内容类型及规则创建好数据库
        2. 创建爬虫项目 Scrapy startproject XXX
            注意：对于段落，爬取到的段落需要去除左右空格之后再录入数据库
        3. 创建爬虫、数据处理和上传、数据库清空三个定时器，设计好爬取、处理和清空数据库等各个时间端让整个流程能顺利进行。
            注意：
                数据库清空前都需要先把上传的数据相关内容放在特定的数据库（postedurldatabase.tb_article_posted）中，方便后面对上传内容是否重复进行判断。
        4. 分别执行三个定时器
# 二、定义一下各种规则
## 1、爬虫相关
    1. 段落相关：
        a. 爬到的段落数据入库前一定要先做左右空格的清除工作
        b. 爬取的流程：
            进入到一个包含文章列表的页面-获取文章信息列表（包含文章的title/url/tag/publishTime）-获取到列表后将其放入Request中
                注意： 这俩步需要再同一个parse中进行，不要分开成俩个爬虫文件。
                        自动化流程中的爬虫项目只能有一个爬虫命令来爬取到所有需要的数据，即只需一个命令：Scrapy crawl SpiderName就可以完成对应网站所需全部数据的爬取操作
            爬取后进入pipeline:
                根据爬取数据内容的不同分别处理：
                    对于文章信息（title/url/tag/publishTime）的入库处理
                    对于文章内容（paragraph/url/hasTag）的入库处理
                    在同一个pipeline中进行，判断依据为 item.fields中是否含有title或是paragraph
            最后入库
        c. 数据库表定义：
            注意对于文章段落的爬取，表的结构已经定下来了。
            CREATE TABLE `databasename`.`tb_articleinfo` (
              `id` int NOT NULL AUTO_INCREMENT,
              `title` longtext,
              `url` longtext,
              `tag_origin` varchar(120) DEFAULT NULL,
              `publishTime` varchar(45) DEFAULT NULL,
              PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='文章列表基础信息\n';
            
            CREATE TABLE `databasename`.`tb_articlecontent` (
              `id` int NOT NULL AUTO_INCREMENT,
              `paragraph` longtext,
              `url` longtext,
              `hasTag` varchar(45) DEFAULT NULL COMMENT '该段落是否包含标签',
              PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='存放文章的段落内容';

    2. 定时器相关
        定时器根据上传数据内容的不同分为多个不同任务类型的定时器的类，每个类都继承于同一个基础定时器
        各个不同任务类型的定义通过对类下的task()方法的重写

    3. 缩略图相关 thumbnailImgs
        数据库表的结构已经定下来了
            CREATE TABLE `postedurldatabase`.`tb_thumbnailimgs_posted` (
              `id` int NOT NULL AUTO_INCREMENT,
              `dateline` varchar(45) DEFAULT NULL,
              `formatDate` varchar(45) DEFAULT NULL,
              `origin_pic_path` longtext,
              `pic_path` longtext,
              `title` longtext,
              `user_name` varchar(45) DEFAULT NULL,
              `user_uid` varchar(45) DEFAULT NULL,
              `user_avatar` longtext,
              PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='缩略图相关上传过的数据';
            
    4. 内容图相关 contentImgs
        数据库表的结构已经定下来了
            CREATE TABLE `postedurldatabase`.`tb_contentimgs_posted` (
              `id` int NOT NULL AUTO_INCREMENT,
              `title` longtext,
              `article_url` longtext,
              `share_url` longtext,
              `behot_time` varchar(45) DEFAULT NULL,
              `group_id` longtext,
              `has_image` varchar(45) DEFAULT NULL,
              `user_name` longtext,
              `user_id` longtext,
              `user_avatarUrl` longtext,
              PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='内容图相关上传过的所有文章链接的信息';
    5. 存放上传过数据的数据库 ———— postedurldatabase
        - 表数量： 3
        - 表结构：
            · tb_article_posted (段落相关)
                CREATE TABLE `tb_article_posted` (
                  `id` int NOT NULL AUTO_INCREMENT,
                  `paragraph` longtext,
                  PRIMARY KEY (`id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='存放已经爬取过的文章的段落内容';
            
            · tb_thumbnailimgs_posted （缩略图相关）
                CREATE TABLE `tb_thumbnailimgs_posted` (
                  `id` int NOT NULL AUTO_INCREMENT,
                  `dateline` varchar(45) DEFAULT NULL,
                  `formatDate` varchar(45) DEFAULT NULL,
                  `origin_pic_path` longtext,
                  `pic_path` longtext,
                  `title` longtext,
                  `user_name` varchar(45) DEFAULT NULL,
                  `user_uid` varchar(45) DEFAULT NULL,
                  `user_avatar` longtext,
                  PRIMARY KEY (`id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='存放缩略图相关上传过的数据';

            · tb_contentimgs_posted （内容图相关）
                CREATE TABLE `tb_contentimgs_posted` (
                  `id` int NOT NULL AUTO_INCREMENT,
                  `title` longtext,
                  `article_url` longtext,
                  `share_url` longtext,
                  `behot_time` varchar(45) DEFAULT NULL,
                  `group_id` longtext,
                  `has_image` varchar(45) DEFAULT NULL,
                  `user_name` longtext,
                  `user_id` longtext,
                  `user_avatarUrl` longtext,
                  PRIMARY KEY (`id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='内容图相关上传过的所有文章链接的信息';
## 2、数据处理及上传相关
    1. 数据处理相关

# 三、整个项目过程中遇到的主要问题及对应解决方案
    1、 定时爬虫跟数据处理及上传，怎么定时
        通过创建定时器，不要用while True
        定时器都是事先封装好整个流程各个步骤，后面再调用

    2、 数据上传重复的问题
        描述： 针对段落数据，由于数据源网站中的显示的文章并没有依据时间进行显示，亦即每次爬取对应数据源获得的文章数据是全部的数据，这就会导致文章内容重复问题，
              而我们希望上传到接口的数据是没有重复数据的。
        想到的方案：
            1 在爬取数据时候判断发布时间，若发布时间包含小时这个字符串说明是最近一天内发布的，那么该文章就可以爬取，否则就跳过不爬取。但是每个网站发布时间的内容不一样，
                这就需要针对各个数据源网站分别设计爬取规则，感觉挺麻烦，所以没有采取该方案。
            2 本机数据库中创建一个专门存放已经上传数据内容的数据库（postedurldatabase）,数据库内有存放段落数据的表（tb_article_posted），每次上传完成在清空上传源表之前
                都把上传源表中的数据复制到tb_article_posted，然后在上传操作之前都对待上传的数据列表进行判断，若数据中的段落内容存在与tb_article_posted则表示该段落之前上传过
                那么就不再重复上传。 这里采用的是这种方法，而复制操作放在清空数据库表的定时器中。
    
    3、 当只有一个pipeline但是却有多个不同类型Item时，怎么根据不同的item执行不同的操作。
        例如本例中有:
            文章列表信息的item————articleInfoItem(url/title/tag)
            文章段落内容的item————articleContentItem(url/paragraph/hasTag
        针对不同item要执行不同的数据获取和数据库录入操作，这时候怎么让程序自动判断并执行呢？
        - 方案1：通过判断item的唯一键名是否再item.fields中判断是否是某个item。
            如本例中两个item中取不同的 title 和 paragraph，通过判断如下
            'paragraph' in item.fields 则对应item是articleContentItem
            'title' in item.fields 则对应item是articleInfoItem
        - 方案2：通过 isinstance(item, articleInfoItem) 方法，判断item是否是articleInfoItem的实例
