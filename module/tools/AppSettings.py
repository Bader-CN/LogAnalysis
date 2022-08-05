# -*- coding: utf-8 -*-

import logging
from configparser import ConfigParser

cfg = ConfigParser()
cfg.read('config.cfg', encoding='utf-8')


class ReadConfig():
    """
    用于获取和设置 config.cfg 的相关参数
    """

    @staticmethod
    def get_language():
        """
        获取配置文件中语言的设定
        :return: str(language)
        """
        if cfg.get('App_Display', 'App_Language') in ["Auto", "auto"]:
            import locale
            return locale.getdefaultlocale()[0]
        else:
            return cfg.get('App_Display', 'App_Language')

    @staticmethod
    def get_loglevel(option, *args, **kwargs):
        """
        获取指定部分的日志等级, 如果值不对, 则返回 INFO
        :param option:
        :param args:
        :param kwargs:
        :return:str("DEBUG" or "INFO" or "WARNING" or "ERROR" or "CRITICAL")
        """
        loglevel = cfg.get("App_Logging", option)
        if loglevel in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            return loglevel
        else:
            return "INFO"

    @staticmethod
    def set_loglevel(Logger, option):
        """
        将日志等级设定为指定值
        :param Logger: logging 模块中的 Handler
        :param option: [App_Logging] 部分的值
        :return:
        """
        loglevel = ReadConfig.get_loglevel(option)
        if loglevel == "DEBUG":
            Logger.setLevel(logging.DEBUG)
        elif loglevel == "ERROR":
            Logger.setLevel(logging.ERROR)
        elif loglevel == "WARNING":
            Logger.setLevel(logging.WARNING)
        elif loglevel == "CRITICAL":
            Logger.setLevel(logging.CRITICAL)
        else:
            Logger.setLevel(logging.INFO)