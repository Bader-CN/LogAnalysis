# -*- coding: utf-8 -*-

import hashlib
from module.tools.AppSettings import ReadConfig


class HashTools():
    """
    哈希工具类, 用于返回任何字符串的哈希值
    """
    def __init__(self):
        # 决定哈希方法
        self.method = ReadConfig.get_hash_method()
        # 每次读取多大的数据
        self.hash_rdsize = ReadConfig.get_max_hashsize()

    def filehash(self, filepath):
        """
        指定文件路径, 读取文件内容并返回对应的哈希值
        :param filepath:
        :return:
        """
        method = self.method
        hash_rdsize = self.hash_rdsize
        # 注意: 不能将 hash 方法写在 init 中!
        # 因为会导致计算的不是每一个文件内容的 hash, 而是所有文件内容的 hash 之和
        if method == "md5":
            self.hash_method = hashlib.md5()
        elif method == "sha1":
            self.hash_method = hashlib.sha1()
        elif method == "sha224":
            self.hash_method = hashlib.sha224()
        elif method == "sha256":
            self.hash_method = hashlib.sha256()
        elif method == "sha384":
            self.hash_method = hashlib.sha384()
        else:
            self.hash_method = hashlib.sha512()

        with open(filepath, "rb") as f:
            # https://zhuanlan.zhihu.com/p/351140647
            # 海象运算符, 支持 Python 3.8+
            while b := f.read(hash_rdsize):
                self.hash_method.update(b)

        hash_value = self.hash_method.hexdigest()
        return hash_value
