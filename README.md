# LogAnalysis

## 软件概述
基于 Qt PySide6 的通用日志分析工具

## 下载地址
https://github.com/Bader-CN/LogAnalysis/releases

## 开发环境
1. 安装 Python 3.8+
2. 利用 pip install 命令安装第三方库
```shell
pip install -r requirements.txt
```
3. 运行 LogAnalysis.py 即可启动软件
4. 如果不想看到 console 界面, 可以将 LogAnalysis.py 重命名为 LogAnalysis.pyw

## 编译方法
可以使用 PyInstaller 来进行编译, 注意修改相关参数的路径
```shell
# PowerShell
pyinstaller -w .\LogAnalysis.py --distpath "C:\LogAnalysis" --workpath "C:\LogAnalysis\build" `
--add-data ".\data\template;.\data\template" `
--add-data ".\LogAnalysis.chm;."
# CMD
pyinstaller -w .\LogAnalysis.py --distpath "C:\LogAnalysis" --workpath "C:\LogAnalysis\build" ^
--add-data ".\data\template;.\data\template" ^
--add-data ".\LogAnalysis.chm;."
```

## 支持产品
* MicroFocus
  * ITOM
    * Operations Agent(OA)
    * Operations Bridge Manager(OBM)
    * Operations Bridge Suite(OpsB)
* RedHat
  * RedHat Linux System
    * Syslog