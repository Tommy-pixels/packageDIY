import cv2
import numpy as np

'''
    集成各种验证：
        滑块验证等
'''
class SliderChecker:
    def getMovement_sliderCheck_1(self, elWidth, templatePath='E:\Projects\packageDIY\\videoRef\\assets\\template.png',
                               targetPath='E:\Projects\packageDIY\\videoRef\\assets\\target.png'):
        '''
            滑块验证 输出水平移动的距离 计算坐标的偏移量
        :param elWidth: 背景图在网页上显示的宽度，用于比例计算实际滑动距离
        :param templatePath: 滑块图片路径
        :param targetPath: 背景图片路径
        :return: 偏移量
        '''
        target_rgb = cv2.imdecode(np.fromfile(targetPath, dtype=np.uint8), -1)
        target_gray = cv2.cvtColor(target_rgb, cv2.COLOR_BGR2GRAY)
        template_rgb = cv2.imread(templatePath, 0)
        ori_width = template_rgb.shape[1]
        ori_height = template_rgb.shape[0]
        res = cv2.matchTemplate(target_gray, template_rgb, cv2.TM_CCOEFF_NORMED)

        # 给匹配到的位置画个圈
        loc = np.where(res >= 0.5)  # Store the coordinates of matched area in a numpy array
        x = loc[0]
        y = loc[1]

        w, h = target_gray.shape[::-1]
        # Draw a rectangle around the matched region.
        if (len(x) and len(y)):
            for pt in zip(*loc[::-1]):
                # pt[0]表示水印位置所在的像素高度
                cv2.rectangle(template_rgb, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)
                # Show the final image with the matched area.
                cv2.imwrite(templatePath, template_rgb)

        value = cv2.minMaxLoc(res)
        # (因为下载的图片跟网页上的图片是有缩放的)所以要根据比例计算网页端需要移动的偏移量
        effectiveVal = value[2][0] * elWidth / ori_width
        return effectiveVal


    def getMovement_sliderCheck_2(self, elWidth, templatePath='E:\Projects\packageDIY\\videoRef\\assets\\template.png',
                                  targetPath='E:\Projects\packageDIY\\videoRef\\assets\\target.png'):
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



