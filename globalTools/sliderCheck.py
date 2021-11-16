import cv2
import numpy as np

'''
    集成各种验证：
        滑块验证等
'''
class SliderChecker:
    def __init__(self, templatePath='E:\Projects\packageDIY\\videoRef\\assets\\template.png', targetPath='E:\Projects\packageDIY\\videoRef\\assets\\target.png'):
        self.templatePath = templatePath
        self.targetPath = targetPath


    # 滑块验证 输出水平移动的距离 计算坐标的偏移量
    # templatePath 滑块 , targetPath 背景模板
    def getMovement_sliderCheck_douyin(self, elWidth):
        '''
            滑块验证 输出水平移动的距离 计算坐标的偏移量
            注意：这一个算法没问题，只是可能需要试几次才有一次正确的
        :param elWidth: 背景图在网页上显示的宽度，用于比例计算实际滑动距离
        :param templatePath: 滑块图片路径
        :param targetPath: 背景图片路径
        :return: 偏移量
        '''
        target_rgb = cv2.imdecode(np.fromfile(self.targetPath, dtype=np.uint8), -1)
        target_gray = cv2.cvtColor(target_rgb, cv2.COLOR_BGR2GRAY)
        template_rgb = cv2.imread(self.templatePath, 0)
        ori_width = target_rgb.shape[1]
        ori_height = target_rgb.shape[0]
        res = cv2.matchTemplate(target_gray, template_rgb, cv2.TM_CCOEFF_NORMED)
        value = cv2.minMaxLoc(res)
        # (因为下载的图片跟网页上的图片是有缩放的)所以要根据比例计算网页端需要移动的偏移量
        effectiveVal = value[2][0] * elWidth / ori_width

        print('effectiveVal:', effectiveVal)
        print('value2:', value[2][0])
        print('value3:', value[3][0])
        print('res:', res.shape)

        return effectiveVal

    # 滑块验证 输出水平移动的距离 计算坐标的偏移量
    # templatePath 滑块 , targetPath 背景模板
    @staticmethod
    def getMovement_sliderCheck_douyin_static(templatePath, targetPath, elWidth):
        '''
            滑块验证 输出水平移动的距离 计算坐标的偏移量
            注意：这一个算法没问题，只是可能需要试几次才有一次正确的
        :param elWidth: 背景图在网页上显示的宽度，用于比例计算实际滑动距离
        :param templatePath: 滑块图片路径
        :param targetPath: 背景图片路径
        :return: 偏移量
        '''
        target_rgb = cv2.imdecode(np.fromfile(targetPath, dtype=np.uint8), -1)
        target_gray = cv2.cvtColor(target_rgb, cv2.COLOR_BGR2GRAY)
        template_rgb = cv2.imread(templatePath, 0)
        ori_width = target_rgb.shape[1]
        ori_height = target_rgb.shape[0]
        res = cv2.matchTemplate(target_gray, template_rgb, cv2.TM_CCOEFF_NORMED)
        value = cv2.minMaxLoc(res)
        # (因为下载的图片跟网页上的图片是有缩放的)所以要根据比例计算网页端需要移动的偏移量
        effectiveVal = value[2][0] * elWidth / ori_width

        print('effectiveVal:', effectiveVal)
        print('value2:', value[2][0])
        print('value3:', value[3][0])
        print('res:', res.shape)

        return effectiveVal




