# -*- coding: utf-8 -*-

import logging
from module.tools.AppSettings import ReadConfig

# 日志格式器
formatter = logging.Formatter('%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')

# 日志输出位置及等级
StreamHandler = logging.StreamHandler()
StreamHandler.setFormatter(formatter)
ReadConfig.set_loglevel(StreamHandler, "App_Console_Level")

FileHandler1 = logging.FileHandler("./log/AppMain.log")
FileHandler1.setFormatter(formatter)
ReadConfig.set_loglevel(FileHandler1, "App_Main_Level")

# 设置记录器及默认等级
AppMainLogger = logging.getLogger("AppMain")
AppMainLogger.setLevel(logging.DEBUG)

# 记录器添加 Handler
AppMainLogger.addHandler(FileHandler1)
AppMainLogger.addHandler(StreamHandler)
