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


class ITOM_BVD_AP_Bridge(BASE):
    """
    OpsB deployments bvd-ap-bridge
    """
    __tablename__ = "opsb_itom_bvd_ap_bridge"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class ITOM_BVD_Controller_Deployment(BASE):
    """
    OpsB deployments bvd-controller-deployment
    """
    __tablename__ = "opsb_itom_bvd_controller_deployment"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class ITOM_BVD_Explore_Deployment(BASE):
    """
    OpsB deployments bvd-explore-deployment
    """
    __tablename__ = "opsb_itom_bvd_explore_deployment"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class ITOM_BVD_Quexserv(BASE):
    """
    OpsB deployments bvd-quexserv
    """
    __tablename__ = "opsb_itom_bvd_quexserv"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class ITOM_BVD_Receiver_Deployment(BASE):
    """
    OpsB deployments bvd-receiver-deployment
    """
    __tablename__ = "opsb_itom_bvd_receiver_deployment"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class ITOM_BVD_Redis(BASE):
    """
    OpsB deployments bvd-redis
    """
    __tablename__ = "opsb_itom_bvd_redis"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class ITOM_BVD_WWW_Deployment(BASE):
    """
    OpsB deployments bvd-www-deployment
    """
    __tablename__ = "opsb_itom_bvd_www_deployment"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class ITOM_Monitoring_Admin(BASE):
    """
    OpsB deployments itom-monitoring-admin
    """
    __tablename__ = "opsb_itom_monitoring_admin"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class ITOM_Monitoring_Collection_Manager(BASE):
    """
    OpsB deployments itom-monitoring-collection-manager
    """
    __tablename__ = "opsb_itom_monitoring_collection_manager"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class ITOM_Monitoring_OA_Discovery_Collector(BASE):
    """
    OpsB deployments itom-monitoring-oa-discovery-collector
    """
    __tablename__ = "opsb_itom_monitoring_oa_discovery_collector"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class ITOM_Monitoring_OA_Metric_Collector(BASE):
    """
    OpsB deployments itom-monitoring-oa-metric-collector
    """
    __tablename__ = "opsb_itom_monitoring_oa_metric_collector"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class ITOM_Monitoring_OA_Metric_Collector_BG(BASE):
    """
    OpsB deployments itom-monitoring-oa-metric-collector-bg
    """
    __tablename__ = "opsb_itom_monitoring_oa_metric_collector_bg"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class ITOM_Monitoring_Service_Data_Broker(BASE):
    """
    OpsB deployments itom-monitoring-service-data-broker
    """
    __tablename__ = "opsb_itom_monitoring_service_data_broker"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class ITOM_DI_Pulsar_Job(BASE):
    """
    OpsB Jobs itomdipulsar-minio-connector-post-upgrade-job
    """
    __tablename__ = "opsb_itom_di_pulsar_job"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class ITOM_Monitoring_Collection_AutoConfigure_Job(BASE):
    """
    OpsB Jobs itom-monitoring-collection-autoconfigure-job
    """
    __tablename__ = "opsb_itom_monitoring_collection_autoconfigure_job"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)


class ITOM_Monitoring_Job_Scheduler(BASE):
    """
    OpsB Jobs itom-monitoring-job-scheduler
    """
    __tablename__ = "opsb_itom_monitoring_job_scheduler"

    # 表定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("filehash.id"))
    log_line = Column(Integer)
    log_time = Column(DateTime)
    log_level = Column(String)
    log_comp = Column(String)
    log_cont = Column(String)