from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()

class FileHash(BASE):
    """
    维护文件路径和对应的哈希值
    """
    __tablename__ = "filehash"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    filepath = Column(String, unique=True)
    hash = Column(String, unique=True)