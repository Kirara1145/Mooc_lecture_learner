# 学习通刷课宝
一个自动化刷学习通网课的软件，基于RapidOCR+Openvino视觉识别框架以及pyautogui自动点击
喜欢的话留下一颗星星吧～

## 主要功能
自动化观看指定课程内的所有视频
目前无法答题，或者应对课程中的打断问题

## 系统需求
注意⚠️：本软件仅能在Win10/11（arm64）上测试过

## 配置指南
### 下载浏览器
本软件仅支持Chrome浏览器
```cmd
#Winget安装chrome
winget install Google.chrome
```

### 安装依赖
在项目文件夹右键空白处，选择“在终端中打开”
输入命令：
```cmd
#安装所有依赖
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
