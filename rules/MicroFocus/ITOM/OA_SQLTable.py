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
    filepath = Column(String)
    hash = Column(String, unique=True)

    # 外联关系, 此关系仅在 Python 中存在
    OASystem = relationship("System")


class Summary(BASE):
    """
    ITOM agent.log Summary
    """
    __tablename__ = "oa_summary"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    key = Column(String)
    value = Column(String)


class Config(BASE):
    """
    ITOM ovconfget command
    """
    __tablename__ = "oa_config"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    key = Column(String)
    value = Column(String)


class System(BASE):
    """
    ITOM System.txt
    """
    __tablename__ = "oa_system"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class HPCSTrace(BASE):
    """
    ITOM System.txt
    """
    __tablename__ = "oa_hpcstrace"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class Policy(BASE):
    """
    ITOM Policy
    """
    __tablename__ = "oa_policy"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    ply_name = Column(String)
    ply_version = Column(String)
    ply_status = Column(String)
    ply_type = Column(String)
    ply_data = Column(String)
