import time

from .globalTools import GetParams_Selenium
from .globalTools import Downloader
from .sliderCheck import SliderChecker
from selenium.webdriver.common.action_chains import ActionChains


class DouyinCrack(GetParams_Selenium):
    '''
        可以根据参数driver的不同针对不同driver做的验证码破解
        但这里的方案是通过破解滑块验证来获取有效cookies，之后再通过接口获取数据
    '''
    def __init__(self, *driverPath, captchaDstDirPath):
        if(driverPath!=()):
            # 显示继承父类
            GetParams_Selenium.__init__(self, driverPath)
            self.downloader = Downloader()  # 资源下载器
            self.captchaDstDirPath = captchaDstDirPath
        else:
            self.downloader = Downloader()  # 资源下载器
            self.captchaDstDirPath = captchaDstDirPath


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

    def handle_SlideCheck(self, *browser):
        '''
            处理指定browser的抖音滑块验证
        :param browser: 指定的browser
        :return:
        '''
        while (1):
            if(browser==()):
                # 无指定浏览器
                targetWidth = self.download_img_sliderCheck(dstDirPath=self.captchaDstDirPath)  # 滑块图片下载器 返回目标网页显示的宽
                movement = SliderChecker.getMovement_sliderCheck_douyin_static(self.captchaDstDirPath+'template.png', self.captchaDstDirPath+'target.png', targetWidth)  # 验证码处理器
                print("滑动的实际距离：", movement)
                # 滑动滑块
                # self.move_sliderTemplate(int(movement))
                self.move_sliderTemplate_likeHuman(int(movement))
            else:
                targetWidth = self.download_img_sliderCheck(browser[0],dstDirPath=self.captchaDstDirPath)  # 滑块图片下载器 返回目标网页显示的宽
                movement = SliderChecker.getMovement_sliderCheck_douyin_static(self.captchaDstDirPath+'template.png', self.captchaDstDirPath+'target.png', targetWidth)
                print("滑动的实际距离：", movement)
                # 滑动滑块
                # self.move_sliderTemplate(int(movement))
                self.move_sliderTemplate_likeHuman(int(movement), browser[0])

            # 滑完一会查看是否需要验证，不需要则滑块验证通过，否则重新执行该方法
            time.sleep(2)
            try:
                if(browser==()):
                    # 无指定浏览器
                    sliderTargetSelector = self.browser.find_element_by_xpath("//img[@id='captcha-verify-image']")  # 背景
                else:
                    sliderTargetSelector = browser.find_element_by_xpath("//img[@id='captcha-verify-image']")  # 背景

            except Exception as e:
                print("验证通过")
                break
            # 验证通过后输出cookie
        return self.get_Obj_allCookies()

    def download_img_sliderCheck(self, *browser, dstDirPath='E:\Projects\packageDIY\\videoRef\\assets\\'):
        '''
        下载滑块以及滑块背景用于识别位置
        :return: targetWidth 背景图在网页中的宽度 用于步长计算
        '''
        try:
            # 背景 target
            # 滑块 template
            if(browser==()):
                    # 无指定浏览器
                sliderTargetSelector = self.browser.find_element_by_xpath("//img[@id='captcha-verify-image']")  # 背景
                sliderTemplateSelector = self.browser.find_element_by_xpath("//img[@class='captcha_verify_img_slide react-draggable sc-VigVT ggNWOG']") # 滑块
            else:
                sliderTargetSelector = browser[0].find_element_by_xpath("//img[@id='captcha-verify-image']")  # 背景
                sliderTemplateSelector = browser[0].find_element_by_xpath("//img[@class='captcha_verify_img_slide react-draggable sc-VigVT ggNWOG']")  # 滑块
            print("出现滑块，下载识别滑块")

            targetImgUrl = sliderTargetSelector.get_attribute('src')    # 背景图url
            templateImgUrl = sliderTemplateSelector.get_attribute('src')    # 滑块url
            targetWidth = sliderTargetSelector.size['width']     # 背景图片宽
            templateWidth = sliderTemplateSelector.size['width']    # 滑块宽
            # 下载模板图片——滑块
            self.downloader.download_img(templateImgUrl, 'template', dstDirPath)
            # 下载背景图片
            self.downloader.download_img(targetImgUrl, 'target', dstDirPath)
            return targetWidth
        except Exception as e:
            # print("无滑块出现，下载失败请刷新浏览器重新操作")
            return ''

    def move_sliderTemplate(self, movement, *browser):
        '''
            移动滑块，移动速度慢了点，后面再想办法处理一下
        :param movement:
        :return:
        '''
        if(browser==()):
            # 无指定浏览器
            # 实例化鼠标操作
            action = ActionChains(self.browser)
            templateSelector = self.browser.find_element_by_xpath("//*[@class='captcha_verify_img_slide react-draggable sc-VigVT ggNWOG']") #滑块
            # 按住滑块
            action.click_and_hold(templateSelector).perform()

            for i in range(movement):
                action.move_by_offset(1, 0)
            # 释放滑块
            action.release().perform()
        else:
            # 实例化鼠标操作
            action = ActionChains(browser[0])
            templateSelector = browser[0].find_element_by_xpath("//*[@class='captcha_verify_img_slide react-draggable sc-VigVT ggNWOG']")  # 滑块
            # 按住滑块
            action.click_and_hold(templateSelector).perform()

            print("验证中...")
            for i in range(movement):
                action.move_by_offset(1, 0)
            # 释放滑块
            action.release().perform()


    # 模拟人操作
    def get_tracks(self, distance, rate=0.6, t=0.2, v=0):
        """
        将distance分割成小段的距离
        :param distance: 总距离
        :param rate: 加速减速的临界比例
        :param a1: 加速度
        :param a2: 减速度
        :param t: 单位时间
        :param t: 初始速度
        :return: 小段的距离集合
        """
        tracks = []
        # 加速减速的临界值
        mid = rate * distance
        # 当前位移
        s = 0
        # 循环
        while s < distance:
            # 初始速度
            v0 = v
            if s < mid:
                a = 20
            else:
                a = -3
            # 计算当前t时间段走的距离
            s0 = v0 * t + 0.5 * a * t * t
            # 计算当前速度
            v = v0 + a * t
            # 四舍五入距离，因为像素没有小数
            tracks.append(round(s0))
            # 计算当前距离
            s += s0
        return tracks

    def move_sliderTemplate_likeHuman(self, movement, *browser):
        '''
            移动滑块，移动速度慢了点，后面再想办法处理一下
        :param movement:
        :return:
        '''
        if (browser == ()):
            # 无指定浏览器
            # 实例化鼠标操作
            action = ActionChains(self.browser)
            templateSelector = self.browser.find_element_by_xpath("//*[@class='captcha_verify_img_slide react-draggable sc-VigVT ggNWOG']")  # 滑块
            # 按住滑块
            action.click_and_hold(templateSelector).perform()

            print("验证中...")
            _tracks = self.get_tracks(movement)
            new_1 = _tracks[-1] - (sum(_tracks) - movement)
            _tracks.pop()
            _tracks.append(new_1)
            print(_tracks)
            for mouse_x in _tracks:
                action.move_by_offset(mouse_x, 0)
            # 释放滑块
            action.release().perform()
            time.sleep(2)

        else:
            # 实例化鼠标操作
            action = ActionChains(browser[0])
            templateSelector = browser[0].find_element_by_xpath("//*[@class='captcha_verify_img_slide react-draggable sc-VigVT ggNWOG']")  # 滑块
            # 按住滑块
            action.click_and_hold(templateSelector).perform()

            print("验证中...")
            _tracks = self.get_tracks(movement)
            new_1 = _tracks[-1] - (sum(_tracks) - movement)
            _tracks.pop()
            _tracks.append(new_1)
            print(_tracks)
            for mouse_x in _tracks:
                action.move_by_offset(mouse_x, 0)
            # 释放滑块
            action.release().perform()
            time.sleep(2)


    def get_Ori_allCookies(self):
        return self.browser.get_cookies()

    def get_Obj_allCookies(self):
        # 获取cookie
        dictCookies = self.browser.get_cookies()
        cookies = {}
        for item in dictCookies:
            key = item['name']
            cookies[str(key)] = str(item['value'])
        return cookies

    def get_Obj_allHeaders(self):
        pass

    def get_URL(self, *browser):
        if(browser==()):
            curUrl = self.browser.current_url()
        else:
            curUrl = browser.browser.current_url()
        return curUrl

    def get_s_v_web_id(self):
        self.handle_SlideCheck()
        pass

    def get_msToken(self):
        pass

    def get_X_Bogus(self):
        pass




