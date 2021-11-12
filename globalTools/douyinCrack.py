import time

from .globalTools import GetParams_Selenium
from .globalTools import Downloader
from .sliderCheck import SliderChecker
from selenium.webdriver.common.action_chains import ActionChains


class DouyinCrack(GetParams_Selenium):

    downloader = Downloader()  # 资源下载器
    checker = SliderChecker()  # 验证码处理器

    '''
        抖音的滑块验证以及获取所需要的参数
    '''
    def enter_url(self, url):
        '''
        进入指定链接
        :param url: 注意需要加上协议 如：https://
        :return:
        '''
        self.browser.get(url)
        pass

    def del_All_cookies(self):
        '''
        删除本地保存的所有cookie，以便网站弹出验证框
        :return: none
        '''
        self.browser.delete_all_cookies()
        pass

    def handle_SlideCheck(self):
        '''
        处理滑块验证：
            下载图片-计算滑动距离-模拟滑动
        :return:
        '''
        while(1):
            targetWidth = self.download_img_sliderCheck()
            movement = self.checker.getMovement_sliderCheck_2(targetWidth)
            print("滑动的实际距离：", movement)
            # 滑动滑块
            self.move_sliderTemplate(int(movement))
            # 滑完一会查看是否需要验证，不需要则滑块验证通过，否则重新执行该方法
            time.sleep(2)
            try:
                sliderTargetSelector = self.browser.find_element_by_xpath("//img[@id='captcha-verify-image']")  # 背景
            except Exception as e:
                print("验证通过")
                break
        # 验证通过后输出cookie
        return self.get_Obj_allCookies()


    def download_img_sliderCheck(self, dstDirPath='E:\Projects\packageDIY\\videoRef\\assets\\'):
        '''
        下载滑块以及滑块背景用于识别位置
        :return: targetWidth 背景图在网页中的宽度 用于步长计算
        '''
        try:
            # 背景 target
            # 滑块 template
            sliderTargetSelector = self.browser.find_element_by_xpath("//img[@id='captcha-verify-image']")  # 背景
            sliderTemplateSelector = self.browser.find_element_by_xpath("//img[@class='captcha_verify_img_slide react-draggable sc-VigVT ggNWOG']") # 滑块
            targetImgUrl = sliderTargetSelector.get_attribute('src')    # 背景图url
            templateImgUrl = sliderTemplateSelector.get_attribute('src')    # 滑块url
            targetWidth = sliderTargetSelector.size['width']     # 背景图片宽
            print('targetWidth: ',targetWidth)
            templateWidth = sliderTemplateSelector.size['width']    # 滑块宽
            # 下载模板图片——滑块
            self.downloader.download_img(templateImgUrl, 'template', dstDirPath)
            # 下载背景图片
            self.downloader.download_img(targetImgUrl, 'target', dstDirPath)
            # self.checkSlide(browser=self.browser, x=x)
            return targetWidth
        except Exception as e:
            print("无滑块出现，下载失败请刷新浏览器重新操作")
            return ''

    def move_sliderTemplate(self, movement):
        '''
            移动滑块，移动速度慢了点，后面再想办法处理一下
        :param movement:
        :return:
        '''
        # 实例化鼠标操作
        action = ActionChains(self.browser)
        templateSelector = self.browser.find_element_by_xpath("//*[@class='captcha_verify_img_slide react-draggable sc-VigVT ggNWOG']") #滑块
        # 按住滑块
        action.click_and_hold(templateSelector).perform()
        for i in range(movement):
            action.move_by_offset(1, 0)
        # 释放滑块
        action.release().perform()


    def get_Obj_allCookies(self):
        # 获取cookie
        dictCookies = self.browser.get_cookies()
        cookies = {}
        for item in dictCookies:
            key = item['name']
            cookies[str(key)] = str(item['value'])
        return cookies

    def get_URL(self):
        pass

    def get_s_v_web_id(self):
        self.handle_SlideCheck()
        pass

    def get_msToken(self):
        pass

    def get_X_Bogus(self):
        pass

