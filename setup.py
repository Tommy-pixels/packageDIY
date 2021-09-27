import setuptools



setuptools.setup(
    name="packageDIY", # Replace with your own username  #自定义封装模块名与文件夹名相同
    version="0.0.1", #版本号，下次修改后再提交的话只需要修改当前的版本号就可以了
    author="唐国钦", #作者
    author_email="dreamertgq@163.com", #邮箱
    description="用于爬取段落数据、图片数据、视频数据以及处理上传等", #描述
    long_description='用于爬取段落数据、图片数据、视频数据以及处理上传等', #描述
    long_description_content_type="text/markdown", #markdown
    url="https://github.com/Tommy-pixels/packageDIY", #github地址
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", #License
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6.8',  #支持python版本
)