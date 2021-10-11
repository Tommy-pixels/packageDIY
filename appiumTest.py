from appium import webdriver

caps = {}
caps["platformName"] = "Android"
caps["platformVersion"] = "10.0"
caps["deviceName"] = "HWHLK-H"
caps["ensureWebviewsHavePages"] = True

driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
TouchAction(driver).tap(x=153, y=837).perform()
TouchAction(driver).tap(x=938, y=2250).perform()
TouchAction(driver).tap(x=139, y=2278).perform()
TouchAction(driver).tap(x=497, y=1483).perform()
TouchAction(driver).tap(x=990, y=153).perform()
desired_caps = self.driver.desired_capabilities()

driver.quit()