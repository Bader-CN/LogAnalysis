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


class OPR_Gateway(BASE):
    """
    OBM opr-gateway.log
    """
    __tablename__ = "obm_opr_gateway"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class OPR_Backend(BASE):
    """
    OBM opr-backend.log
    """
    __tablename__ = "obm_opr_backend"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class OPR_Gateway_Flowtrace(BASE):
    """
    OBM opr-gateway-flowtrace.log
    """
    __tablename__ = "obm_opr_gateway_flowtrace"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class OPR_Backend_Flowtrace(BASE):
    """
    OBM opr-flowtrace-backend.log (名字没写错……)
    """
    __tablename__ = "obm_opr_backend_flowtrace"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class OPR_Scripting_Host(BASE):
    """
    OBM opr-scripting-host.log
    """
    __tablename__ = "obm_opr_scripting_host"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class OPR_ConfigServer(BASE):
    """
    OBM opr-configserver.log
    """
    __tablename__ = "obm_opr_configserver"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class OPR_WebApp(BASE):
    """
    OBM opr-webapp.log
    """
    __tablename__ = "obm_opr_webapp"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class OPR_WS_Response(BASE):
    """
    OBM opr-ws-response.log
    """
    __tablename__ = "obm_opr_ws_response"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class User_Stats_Log_Filter(BASE):
    """
    OBM opr-ws-response.log
    """
    __tablename__ = "obm_user_stats_log_filter"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class Login(BASE):
    """
    OBM login.log
    """
    __tablename__ = "obm_login"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class UserActions_Servlets(BASE):
    """
    OBM login.log
    """
    __tablename__ = "obm_user_actions_servlets"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class OPR_SvcDiscserver(BASE):
    """
    OBM opr-svcdiscserver.log
    """
    __tablename__ = "obm_opr_svcdiscserver"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class OPR_SvcDiscserver_CITrace(BASE):
    """
    OBM opr-svcdiscserver-citrace.log
    """
    __tablename__ = "obm_opr_svcdiscserver_citrace"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class PMI(BASE):
    """
    OBM pmi.log
    """
    __tablename__ = "obm_pmi"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class BVD(BASE):
    """
    OBM bvd.log
    """
    __tablename__ = "obm_bvd"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class DownTime(BASE):
    """
    OBM downtime.log
    """
    __tablename__ = "obm_downtime"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class OPR_CLIS(BASE):
    """
    OBM opr-clis.log
    """
    __tablename__ = "obm_opr_clis"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class OPR_HeartBeat(BASE):
    """
    OBM opr-heartbeat.log
    """
    __tablename__ = "obm_opr_heartbeat"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class BUS(BASE):
    """
    OBM bus.log
    """
    __tablename__ = "obm_bus"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class OPR_CIResolver(BASE):
    """
    OBM opr-ciresolver.log
    """
    __tablename__ = "obm_opr_ciresolver"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class Scripts(BASE):
    """
    OBM scripts.log
    """
    __tablename__ = "obm_scripts"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)