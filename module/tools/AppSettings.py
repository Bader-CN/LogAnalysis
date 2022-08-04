# -*- coding: utf-8 -*-

from configparser import ConfigParser

cfg = ConfigParser()
# 添加 encoding = utf-8 的目的是防止解析错误
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
        获取指定部分的日志等级
        :param logsection:
        :param args:
        :param kwargs:
        :return:
        """
        loglevel = cfg.get("App_logging", option)
        if loglevel in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            return loglevel
        else:
            return "INFO"


