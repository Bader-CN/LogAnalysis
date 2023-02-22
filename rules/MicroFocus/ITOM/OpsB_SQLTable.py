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


class ITOM_DI_Administration(BASE):
    """
    OpsB ITOM_DI_Administration
    # administration.log
    # administration-audit.log
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
    OpsB ITOM_DI_Administration
    # dataaccess.log
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


class ITOM_DI_Metadata_Server(BASE):
    """
    OpsB ITOM_DI_Metadata_Server
    # metadata-server-app.log
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
    OpsB ITOM_DI_Postload_TaskController
    # taskcontroller.log
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
    OpsB ITOM_DI_Postload_TaskExecutor
        # aggregate.log
        # csv-direct-load.log
        # forecast.log
        # perl-task.log
        # taskexecutor.log
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
    OpsB ITOM_DI_receiver_dpl
    # receiver-itom-di-receiver-dpl.*.log
    # receiver-out.log
    """
    __tablename__ = "opsb_itom_di_receiver_dpl"

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
    OpsB ITOM_DI_Scheduler_UDX
    # scheduler.log
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


class ITOM_IDM(BASE):
    """
    OpsB ITOM_IDM
    # idm-loader.log
    # idm-service.log
    """
    __tablename__ = "opsb_itom_idm"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)