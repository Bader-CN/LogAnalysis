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

    # 外联关系, 此关系仅在 Python 中存在
    OASystem = relationship("System")

    def __repr__(self):
        return "<FileHash(id='%s', filepath='%s', hash='%s')>" % (self.id, self.filepath, self.hash)

class System(BASE):
    """
    OA System.txt
    """
    __tablename__ = "system"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)

    def __repr__(self):
        return "<System(file_id='%s', log_line='%s', log_time='%s', log_level='%s', log_comp='%s', log_cont='%s')>" % (self.file_id, self.log_line, self.log_time, self.log_level, self.log_comp, self.log_cont)
    