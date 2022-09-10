# -*- coding: utf-8 -*-

import psutil
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

    @staticmethod
    def get_cpu_count(logical=False, *args, **kwargs):
        """
        返回 CPU 的物理核心数, 默认不包括逻辑核心
        :param logical: 是否包含逻辑核心, 默认不包含(False)
        :param args:
        :param kwargs:
        :return: int
        """
        if psutil.cpu_count(logical=logical) != None:
            return psutil.cpu_count(logical=logical)
        else:
            return 2
    
    @staticmethod
    def get_max_process(*args, **kwargs):
        """
        获取配置文件 Max_Processes 中的值
        :param args:
        :param kwargs:
        :return: str
        """
        return cfg.get("App_Optimiz", "Max_Processes")

    @staticmethod
    def get_max_hashsize(*args, **kwargs):
        """
        获取哈希计算每次读取的最大值
        :param args:
        :param kwargs:
        :return: int
        """
        size = int(cfg.getint("App_Optimiz", "Max_Hashsizes"))
        if size >= 1:
            return size
        else:
            return 8192

    @staticmethod
    def get_hash_method(*args, **kwargs):
        """
        返回哈希校验指定的方法, 默认返回 md5
        :param args:
        :param kwargs:
        :return: str
        """
        method = cfg.get("App_Optimiz", "Hash_Method")
        if method in ["md5", "sha1", "sha224", "sha256", "sha384", "sha512"]:
            return method
        else:
            return "md5"
