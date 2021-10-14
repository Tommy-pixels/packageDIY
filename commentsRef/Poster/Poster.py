import requests, hashlib
from ..universalTools import tools
from requests_toolbelt import MultipartEncoder


class Poster():
    def __init__(self, interface):
        self.interface = interface
        self.userName = 'qin'
        self.password = 'qin123456'
        self.curDate = str(tools.getCurDate())
        self.key = hashlib.md5(('datapool' + self.userName + self.password + self.curDate).encode('utf-8')).hexdigest()

    # 上传单个数据列表的方法
    def poster(self, postableData):
        # 这里传文件的时候用绝对路径传，不然传了之后显示不了
        formData = (postableData)
        m = MultipartEncoder(formData)
        headers2 = {
            "Content-Type": m.content_type
        }
        paragraphPostResult = requests.post(url=self.interface, data=m, headers=headers2)
        return paragraphPostResult


    def post_auto(self, effectiveDataList, whichKind):
        for item in effectiveDataList:
            if(whichKind=='keyParagraph'):
                postableData = {
                    "key": self.key,
                    "account": self.userName,
                    "password": self.password,
                    'content': item[0],
                    'keyword': item[1],
                    'rekeyword': '配资'
                }
                self.poster(postableData=postableData)
            elif(whichKind=='relativeParagraph'):
                postableData = {
                    "key": self.key,
                    "account": self.userName,
                    "password": self.password,
                    'content': item[0],
                    'keyword': item[1]
                }
                self.poster(postableData=postableData)
            elif(whichKind=='articleComment'):
                postableData = {
                    "key": self.key,
                    "account": self.userName,
                    "password": self.password,
                    'comment': item[0].replace(item[1], '股票')
                }
                self.poster(postableData=postableData)
