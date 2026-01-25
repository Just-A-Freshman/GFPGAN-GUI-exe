# GFPGAN-GUI-exe
## 简介
这是一个基于开源项目: https://github.com/TencentARC/GFPGAN  封装而成的项目，界面基于tkinter编写。GFPGAN是一个用于高清人像的开源项目。上传一系列包含人像的照片，该程序可以快速地将照片中的人脸识别出来并高清。特别的，你可以只选择照片中的部分人像进行高清。

这个项目是我在刚学Python不到1年时所写的。代码之混乱以及程序界面之丑陋不言而喻。最大的优点可能就是，它至少能跑。项目使用Pyinstaller进行了打包，你可以直接下载使用。

## 注意事项
由于使用cv2进行了图像处理。该图像处理库对中文路径非常敏感，直接导致中文名或中文路径下的图片不可被正常处理。虽然实际上我们可以在代码中将文件迁移到在一个特定的英文路径下重命名来解决这个问题，但是我太懒了，完全不想维护这个项目了。

## 环境配置
你需要Python版本在3.7-3.8之间，随后使用如下命令安装依赖：
```
pip install -r requirements.txt
```

注意不要直接运行main.py，先运行gfpgan/utils.py，确保能跑通才行。torchvision可能报错：```No module named ‘torchvision.transforms.functional_tensor```，解决办法把报错文件里的```torchvision.transforms.functional_tensor```改为```torchvision.transforms.functional```

安装依赖后，你需要下载模型并将三个模型解压到gfpgan/weights/目录下。
三个模型模型压缩包的下载地址：[https://github.com/Just-A-Freshman/GFPGAN-GUI-exe/releases/download/models/models.7z](https://github.com/Just-A-Freshman/GFPGAN-GUI-exe/releases/download/models/models.7z)

## 打包程序下载地址(Windows版本，可一键运行)
[https://github.com/Just-A-Freshman/GFPGAN-GUI-exe/releases/download/program/default.zip](https://github.com/Just-A-Freshman/GFPGAN-GUI-exe/releases/download/program/default.zip)

