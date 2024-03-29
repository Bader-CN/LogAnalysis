# -*- coding: utf-8 -*-

import time
import os.path
from datetime import datetime
# 类似 java 的抽象类, 这里子类必须要实现带有 @abstractmethod 的方法
# https://docs.python.org/zh-cn/3/library/abc.html
from abc import ABCMeta, abstractmethod
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
try:
    from module.tools.AppDebug import AppMainLogger
except:
    pass

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
            "%a %b %d %H:%M:%S %Z %Y",
            "%b %d %H:%M:%S",
        ]

        for datetime_format in datetime_formats:
            try:
                # 尝试生成 datetime_str, 如果失败, 则替换 datetime_format 重新执行一次
                datetime_str = datetime.strptime(logdate, datetime_format)
                # 如果上一条命令可以执行, 则再返回时间的字符串数据
                return datetime_str.strftime('%Y-%m-%d %H:%M:%S.%f')

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
        # 状态变量
        success = False
        attempt = 0
        # 连接数据库查询数据
        path = r"sqlite:///" + os.path.abspath(targetdb)
        engine = create_engine(path, future=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        while not success:
            try:
                query = session.query(FileHash).filter(FileHash.filepath == file).first()
                success = True
                attempt = 0
            except:
                # 如果遇到 DB locked, 尝试 3 次, 失败则退出
                attempt += 1
                AppMainLogger.warning("DB is locked, waiting 10s and try again, now attempts {}".format(str(attempt)))
                if attempt == 3:
                    break
                time.sleep(10)
        session.close()
        file_id = query.id
        return file_id

    def get_file_encoding(self, file):
        """
        检测并返回文件编码, 如果预设的编码都有问题则默认返回 utf-8
        """
        ok_code = ""
        encodes = ["utf-8", "big5", "shift_jis"]
        # 尝试使用指定的文件编码打开文件
        for encoding in encodes:
            try:
                with open(file, mode="r", encoding=encoding) as f:
                    f.read()
                    ok_code = encoding
                    break
            # 预期错误
            except UnicodeDecodeError:
                pass
            # 其余错误
            except Exception as e:
                print(e)
        # 返回文件的编码
        return ok_code if ok_code != "" else "utf-8"

    @abstractmethod
    def classifiles(self):
        """
        分类文件, 基于文件来决定后续调用什么方法来处理文件
        :return:
        """
        pass