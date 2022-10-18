# -*- coding: utf-8 -*-

import os.path
from datetime import datetime
# 类似 java 的抽象类, 这里子类必须要实现带有 @abstractmethod 的方法
# https://docs.python.org/zh-cn/3/library/abc.html
from abc import ABCMeta, abstractmethod
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

class ReadFileTemplate(metaclass=ABCMeta):
    """
    读取日志文件的基类, 同时也是公用的工具类
    """
    def __init__(self):
        pass

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
            "%m/%d/%Y %H:%M:%S",
        ]

        for datetime_format in datetime_formats:
            try:
                # 尝试生成 datetime_str, 如果失败, 则替换 datetime_format 重新执行一次
                datetime_str = datetime.strptime(logdate, datetime_format)
                # 如果上一条命令可以执行, 则再返回时间的字符串数据
                return datetime_str.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

            except Exception as e:
                pass

        # 如果都不符合, 则返回 Null
        return str('Null')

    def get_file_id(self, targetdb, file, FileHash):
        """
        返回 FileHash 表中对应的 id
        :param targetdb:
        :param file:
        :param FileHash:
        :return: int
        """
        path = r"sqlite:///" + os.path.abspath(targetdb)
        engine = create_engine(path, future=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        query = session.query(FileHash).filter(FileHash.filepath == file).first()
        session.close()
        file_id = query.id
        return file_id

    @abstractmethod
    def classifiles(self):
        """
        分类文件, 基于文件来决定后续调用什么方法来处理文件
        :return:
        """
        pass