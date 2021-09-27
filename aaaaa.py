'''
    关于
    @class
'''

class A():
    a = 'AA'
    @classmethod
    def func1(cls):
        # 使用classmethod 函数的第一个参数必须是cls，表示类本身
        print("func1")
        print(A.a)
        print(cls.a)
        A().func3()
        cls().func3()
        cls.func2()


    @staticmethod
    def func2():
        # 使用staticmethod 函数可以不用添加实例参数self和类参数cls
        print("func2")
        print(A.a)
        A.func3()
        pass

    def func3(self):
        # 不添加classmethod和staticmethod注解，函数需添加实例参数self
        print("func3")
        pass
