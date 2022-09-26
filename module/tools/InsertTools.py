# -*- coding: utf-8 -*-

from datetime import datetime

class ReadFile():
    """
    读取日志文件的基类, 同时也是公用的工具类
    """
    def __init__(self, TaskInfo):
        self.file = TaskInfo.get("file")
        self.targetdb = TaskInfo.get("targetdb")

    def get_logtime(self, logdate):
        """
        根据日志内容来获取日志时间
        :param logdate: 时间的字符串
        :return: str(datetime)
        """
        datetime_formats = [
            '%Y-%m-%d %H:%M:%S.%f',
            '%Y-%m-%dT%H:%M:%S.%f',
            '%Y-%m-%d %H:%M:%S,%f',
            '%Y/%m/%d %H:%M:%S.%f',
            "%a %b %d %H:%M:%S %Y",
            "%Y-%m-%d %H:%M:%S",
            "%Y/%m/%d %H:%M:%S",
            "%y/%m/%d %H:%M:%S",
            "%Y %b %d %H:%M:%S",
            "%d-%b-%Y %H:%M:%S",
        ]

        for datetime_format in datetime_formats:
            try:
                # 尝试生成 datetime_str, 如果失败, 则替换 datetime_format 重新执行一次
                datetime_str = datetime.strptime(logdate, datetime_format)
                # 如果上一条命令可以执行, 则再返回时间的字符串数据
                if datetime_format == '%Y-%m-%d %H:%M:%S.%f':
                    return datetime_str.strftime('%Y-%m-%d %H:%M:%S.%f')
                elif datetime_format == '%Y-%m-%dT%H:%M:%S.%f':
                    return datetime_str.strftime('%Y-%m-%dT%H:%M:%S.%f')
                elif datetime_format == '%Y-%m-%d %H:%M:%S,%f':
                    return datetime_str.strftime('%Y-%m-%d %H:%M:%S.%f')
                elif datetime_format == '%Y/%m/%d %H:%M:%S.%f':
                    return datetime_str.strftime('%Y-%m-%d %H:%M:%S.%f')
                else:
                    return datetime_str.strftime('%Y-%m-%d %H:%M:%S.%f')

            except Exception as e:
                pass

        # 如果都不符合, 则返回 Null
        return str('Null')
