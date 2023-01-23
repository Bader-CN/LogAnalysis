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


class ITOM_DI_Administration(BASE):
    """
    OpsB deployments itom-di-administration
    """
    __tablename__ = "opsb_itom_di_administration"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)

class ITOM_DI_Data_Access_DPL(BASE):
    """
    OpsB deployments itom-di-data-access-dpl
    """
    __tablename__ = "opsb_itom_di_data_access_dpl"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class ITOM_DI_MetaData_Server(BASE):
    """
    OpsB deployments itom-di-metadata-server
    """
    __tablename__ = "opsb_itom_di_metadata_server"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class ITOM_DI_Postload_TaskController(BASE):
    """
    OpsB deployments itom-di-postload-taskcontroller
    """
    __tablename__ = "opsb_itom_di_postload_taskcontroller"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class ITOM_DI_Postload_TaskExecutor(BASE):
    """
    OpsB deployments itom-di-postload-taskexecutor
    """
    __tablename__ = "opsb_itom_di_postload_taskexecutor"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class ITOM_DI_Receiver_DPL(BASE):
    """
    OpsB deployments itom-di-receiver-dpl
    """
    __tablename__ = "opsb_itom_di_postload_receiver_dpl"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class ITOM_DI_Scheduler_UDX(BASE):
    """
    OpsB deployments itom-di-scheduler-udx
    """
    __tablename__ = "opsb_itom_di_scheduler_udx"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class ITOM_DI_Vertica_DPL(BASE):
    """
    OpsB deployments itom-di-vertica-dpl
    """
    __tablename__ = "opsb_itom_di_vertica_dpl"

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