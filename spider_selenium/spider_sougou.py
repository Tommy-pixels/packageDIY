import time

from selenium import webdriver
from time import sleep
from articlesRef.DatabaserOperator import databaseOperator as dbOp
class Crawler_Sougou:
    def __init__(self, chromeDriverPath=r'E:\Projects\webDriver\\chrome\\chromedriver.exe'):
        option = webdriver.ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_argument('--disable-blink-features=AutomationControlled')

        self.browser = webdriver.Chrome(executable_path=chromeDriverPath, options=option)
        self.contraler_db = dbOp.dbOperator('paragraphdatabase')
        self.browser.get(
            'https://weixin.sogou.com/weixin?type=2&s_from=input&query=%E8%82%A1%E7%A5%A8%E5%85%A5%E9%97%A8%E5%9F%BA%E7%A1%80%E7%9F%A5%E8%AF%86&ie=utf8&_sug_=y&_sug_type_=&w=01019900&sut=1323&sst0=1637824112380&lkt=0%2C0%2C0')
        sleep(5)

    def get_articleList(self):
        articleList = []
        liList = self.browser.find_elements_by_xpath('//ul[@class="news-list"]//li')
        for li in liList:
            pubTime = li.find_element_by_xpath('.//span[@class="s2"]').text
            url = li.find_element_by_xpath('.//h3//a').get_attribute('href')
            if ('小时前' in pubTime):
                articleList.append(url)
        return articleList

    def get_content(self):
        sections = self.browser.find_elements_by_xpath('//div[@class="rich_media_content "]//section')
        paragraphList = []
        for section in sections:
            paragraph = section.text
            if (paragraph != '' and self.filter_unrelative(paragraph)):
                paragraphList.append(paragraph)
        return paragraphList

    def filter_unrelative(self, paragraph):
        filter_words = [
            '戳上面的', '专注分享股票', '文中内容仅为个人观点', '标签', '长按二维码', '扫码关注', '关注公众号', '添加助理', '扫描二维码', '加助理进群',
            '好的投资理财软件', '关注我们', '入门学习', '记得置顶', '点我【关注】', '直播回放', '下期视频告诉你'
        ]
        for word in filter_words:
            if (word in paragraph):
                return False
            else:
                continue
        return True

    def insert_db(self, pList: list):
        for paragraph in pList:
            sql = 'INSERT INTO `paragraphdatabase`.`tb_relativeparagraph_sougouweixin` (`paragraph`) VALUES (\'{}\');'.format(
                paragraph)
            self.contraler_db.insertData2DB(sql)

    def run(self):
        urlList = self.get_articleList()
        for url in urlList:
            self.browser.get(url)
            time.sleep(2)
            pList = self.get_content()
            self.insert_db(pList=pList)
        self.browser.close()



def spider_sougou(origin):
    if (origin == 'sougou'):
        sougou = Crawler_Sougou()
        sougou.run()
        del sougou
