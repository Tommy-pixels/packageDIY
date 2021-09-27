"""
    抖音视频 快手视频 的过滤爬取上传自动化流程
        注意做好滑块的验证功能：
            该功能下注意图片的缩放， 网页图片的显示的尺寸同下载下来的图片的尺寸是有差别的，导致滑块识别出来的值有差异
        滑块模板和背景图片下载下来后通过 opencv进行模板匹配获得滑动的距离
        最后再利用
            selenium的控制
            pyguiauto的鼠标模拟

        数据要抓当天的而且去除重复
            过滤条件要判断发布的时间是否是当天的
                抖音有一个发布时间的标签，显示了视频的发布时间如 2021-09-17
                快手没有发布时间，显示的只有 n小时前 n天前 n周前 n月前，一般不会有1天前，只有两天前，一天内的都用x小时表示，如 10小时前
            去除重复
                对于抖音:
                    通过在本地数据库 postedurldatabase 存储上传过的视频的title，每次上传时和本地数据库的title比较进行判断
                对于快手：
                    通过在本地数据库 postedurldatabase 存储对应视频链接的clientCacheKey进行判断，每次上传时和本地数据库的clientCacheKey比较进行判断
        爬取的url
        抖音：{
            # "股市-综合排序-发布时间": "https://www.douyin.com/search/%E8%82%A1%E5%B8%82?publish_time=0&sort_type=0&source=normal_search&type=video"
            "股-最新发布-一天内": "https://www.douyin.com/search/%E8%82%A1?publish_time=1&sort_type=2&source=normal_search&type=video"
            "杠杆-最新发布-一天内": "https://www.douyin.com/search/%E6%9D%A0%E6%9D%86?publish_time=1&sort_type=2&source=normal_search&type=video"
            "股票-最新发布-一天内": "https://www.douyin.com/search/%E8%82%A1%E7%A5%A8?publish_time=1&sort_type=2&source=normal_search&type=video"
            "涨跌-最新发布-一天内": "https://www.douyin.com/search/%E6%B6%A8%E8%B7%8C?publish_time=1&sort_type=2&source=normal_search&type=video"
            "大盘-最新发布-一天内": "https://www.douyin.com/search/%E5%A4%A7%E7%9B%98?publish_time=1&sort_type=2&source=normal_search&type=video"
            "B股-最新发布-一天内": "https://www.douyin.com/search/B%E8%82%A1?publish_time=1&sort_type=2&source=normal_search&type=video"
            "短线-最新发布-一天内": "https://www.douyin.com/search/%E7%9F%AD%E7%BA%BF?publish_time=1&sort_type=2&source=normal_search&type=video"
            "指数-最新发布-一天内": "https://www.douyin.com/search/%E6%8C%87%E6%95%B0?publish_time=1&sort_type=2&source=normal_search&type=video"
        }
        快手：{
            "股": "https://www.kuaishou.com/search/video?searchKey=%E8%82%A1"
            ""
        }

    关于滑块验证：
        + 百度查了好久就只有两种方法,但是每一种管用
            1 用cv2模板匹配的方式获得滑动距离，然后selenium再滑动对应元素
                这里涉及可能匹配错误，导致获得错误的距离，即便匹配正确获得正确的滑动距离，好像也是会被检测到导致滑动失败
            2 添加option
                · 针对旧版本 chrome
                option = webdriver.ChromeOptions()
                option.add_experimental_option('excludeSwitches', ['enable-automation'])
                option.add_experimental_option('useAutomationExtension', False)
                self.browser = webdriver.Chrome(executable_path="E:\Projects\webDriver\\chrome\\chromedriver.exe", options=option)
                · 针对新版本 chrome
                option = webdriver.ChromeOptions()
                option.add_experimental_option('excludeSwitches', ['enable-automation'])
                option.add_experimental_option('useAutomationExtension', False)
                self.browser = webdriver.Chrome(executable_path="E:\Projects\webDriver\\chrome\\chromedriver.exe", options=option)
                self.browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                    'source': 'Object.defneProperty(navigator, "webdriver", {get: () => Chrome})'
                })
            上面这几种方法好像以前能用，反正现在我用了没一点效果
        + 最后反而再哔哩哔哩某个没用的视频的评论里找到了有效的方法
            option = webdriver.ChromeOptions()
            option.add_experimental_option('excludeSwitches', ['enable-automation'])
            option.add_argument('--disable-blink-features=AutomationControlled')

"""