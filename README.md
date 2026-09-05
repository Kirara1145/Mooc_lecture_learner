# 学习通刷课宝
一个自动化刷学习通网课的软件，基于RapidOCR+Openvino视觉识别框架以及pyautogui自动点击  
注意⚠️：本软件仅供交流学习使用，请遵循你所在学校对网络课程的管理规定  
喜欢的话留下一颗星星吧～

## 主要功能
自动化观看指定课程内的所有视频
目前无法答题，或者应对课程中的打断问题

## 系统需求
注意⚠️：本软件仅能在Win10/11（arm64）上测试过

## 配置指南
### 安装python
本程序开发于Python3.12环境，理论上Python3.12+均可运行  
在官网下载安装Python，或者：
```cmd
winget install Python.Python.3.12
```
### 下载浏览器
本软件仅支持Chrome浏览器，自行下载浏览器或者：
```cmd
winget install Google.Chrome
```

### 安装依赖
在项目文件夹右键空白处，选择“在终端中打开”
输入命令：
```cmd
pip install -r requirements.txt
```
## 运行
左键双击init.py
或者 
在项目文件夹右键空白处，选择“在终端中打开”
```cmd
#运行软件
python run init.py
```
电脑此时会打开学习通界面，登录你自己的账号，打开自己希望刷的课程
在命令框里输入任意键后回车，即可开始刷课
