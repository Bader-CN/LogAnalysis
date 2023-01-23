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


class ITOM_DI_Pulsar_BookKeeper(BASE):
    """
    OpsB statefulsets itomdipulsar-bookkeeper
    """
    __tablename__ = "opsb_itom_di_pulsar_bookkeeper"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class ITOM_DI_Pulsar_Zookeeper(BASE):
    """
    OpsB statefulsets itomdipulsar-zookeeper
    """
    __tablename__ = "opsb_itom_di_pulsar_zookeeper"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class ITOM_DI_Pulsar_Broker(BASE):
    """
    OpsB deployments itomdipulsar-broker
    """
    __tablename__ = "opsb_itom_di_pulsar_broker"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class ITOM_DI_Pulsar_Proxy(BASE):
    """
    OpsB deployments itomdipulsar-proxy
    """
    __tablename__ = "opsb_itom_di_pulsar_proxy"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class ITOM_DI_Pulsar_Jobs(BASE):
    """
    OpsB Jobs itomdipulsar-minio-connector-post-upgrade-job
    """
    __tablename__ = "opsb_itom_di_pulsar_jobs"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)