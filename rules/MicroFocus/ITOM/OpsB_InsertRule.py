# -*- coding: utf-8 -*-

import re
from datetime import datetime
from module.tools.InsertTools import ReadFileTemplate
from rules.MicroFocus.ITOM.OpsB_SQLTable import FileHash
if __name__ != "__main__":
    from module.tools.AppDebug import MultSQLLogger

class OpsBFiles(ReadFileTemplate):
    """
    MicroFocus ITOM OpsB 文件解析类
    """
    def __init__(self, TaskInfo, QData=None):
        # 继承父类的方法和属性
        super().__init__()
        # 从 TaskInfo 中获取相关数据
        self.TaskInfo = TaskInfo
        self.file = self.TaskInfo.get("file")
        self.encoding = self.get_file_encoding(self.file)
        # 模块模式下, 继续获取下列信息
        if __name__ != "__main__":
            self.targetdb = self.TaskInfo.get("targetdb")
            self.company = self.TaskInfo.get("company")
            self.productline = self.TaskInfo.get("productline")
            self.product = self.TaskInfo.get("product")
            self.total = self.TaskInfo.get("total")
        # 如果匹配到此内容, 则改行不做任何处理
        self.blkline = [
            '""',
            '}\n',
        ]
        # 处理的实际逻辑
        data = self.classifiles()
        # 将处理完成的数据放到队列中
        if __name__ != "__main__":
            QData.put(data)

    def classifiles(self):
        """
        针对 OpsB 文件进行分类, 然后在做后续处理
        :return:
        """
        # itomdipulsar 相关日志
        if re.findall("itomdipulsar-.*\.log", self.file, re.IGNORECASE):
            return self.readlog_opsb_type1()
        # itom-di 相关日志
        elif re.findall("itom-di.*\.log", self.file, re.IGNORECASE):
            return self.readlog_opsb_type1()
        # bvd 相关日志
        elif re.findall("bvd-.*\.log", self.file, re.IGNORECASE):
            return self.readlog_opsb_type1()
        # itom-monitoring 相关日志
        elif re.findall("itom-monitoring-.*\.log", self.file, re.IGNORECASE):
            return self.readlog_opsb_type1()
        # itom-opsb-content-manager 日志
        elif re.findall("itom-opsb-content-manager-.*\.log", self.file, re.IGNORECASE):
            return self.readlog_opsb_type1()
        # itom-ingress-controller 日志
        elif re.findall("itom-ingress-controller-.*\.log", self.file, re.IGNORECASE):
            return self.readlog_opsb_type1()
        # frontend-ingress-controller 日志
        elif re.findall("frontend-ingress-controller-.*\.log", self.file, re.IGNORECASE):
            return self.readlog_opsb_type1()
        # portal-ingress-controller 日志
        elif re.findall("portal-ingress-controller-.*\.log", self.file, re.IGNORECASE):
            return self.readlog_opsb_type1()
        # itom-frontend-ui 日志
        elif re.findall("itom-frontend-ui-.*\.log", self.file, re.IGNORECASE):
            return self.readlog_opsb_type1()
        # kube-registry 日志
        elif re.findall("kube-registry-.*\.log", self.file, re.IGNORECASE):
            return self.readlog_opsb_type1()
        # itom-idm 日志
        elif re.findall("itom-idm-.*\.log", self.file, re.IGNORECASE):
            return self.readlog_opsb_type1()
        # K8S 进程日志
        elif re.findall("kubelet\.\d+.log|containerd.\d+.log", self.file, re.IGNORECASE):
            return self.readlog_k8s_process()

    def readlog_opsb_type1(self):
        """
        OpsB logs
        # itomdipulsar-bookkeeper.*.log
        # itomdipulsar-zookeeper.*.log
        # itomdipulsar-broker.*.log
        # itomdipulsar-proxy.*.log
        # itomdipulsar-minio-connector-post-upgrade-job.*.log
        # itom-di-administration.*.log
        # itom-di-data-access-dpl.*.log
        # itom-di-metadata-server.*.log
        # itom-di-postload-taskcontroller.*.log
        # itom-di-postload-taskexecutor.*.log
        # itom-di-receiver-dpl.*.log
        # itom-di-scheduler-udx.*.log
        # itom-di-vertica-dpl.*.log
        # bvd-ap-bridge-.*.log
        # bvd-controller-deployment-.*.log
        # bvd-explore-deployment-.*.log
        # bvd-quexserv-.*.log
        # bvd-receiver-deployment-.*.log
        # bvd-redis-.*.log
        # bvd-www-deployment-.*.log
        # itom-monitoring-admin-.*.log
        # itom-monitoring-collection-autoconfigure-job-.*.log
        # itom-monitoring-collection-manager-.*.log
        # itom-monitoring-job-scheduler-.*.log
        # itom-monitoring-oa-discovery-collector-.*.log
        # itom-monitoring-oa-metric-collector-.*.log
        # itom-monitoring-oa-metric-collector-bg-.*.log
        # itom-monitoring-service-data-broker-.*.log
        # itom-opsb-content-manager-.*.log
        # itom-ingress-controller-.*.log
        # frontend-ingress-controller-.*.log
        # portal-ingress-controller-.*.log
        # itom-frontend-ui-.*.log
        # kube-registry-.*.log
        # itom-idm-.*.log
        :return: TaskInfo["data"] = SList --> [sqlalchemy obj1, sqlalchemy obj2, ...]
        """
        # 模块模式下, 记录读取的文件名
        if __name__ != "__main__":
            MultSQLLogger.info("Reading File:[{}]".format(self.file))
        # 初始化变量
        DList = []  # 原始文档的每一行数据
        IList = []  # 日志开头的索引
        FList = []  # 切分完并处理完成的数据
        SList = []  # 转换为 SQL 语句的数据
        now_idx = 0

        # 读取文件, 将文件的每一行保存在 DList 中
        with open(self.file, mode="r", encoding=self.encoding, errors="replace") as file:
            for line in file:
                DList.append(line.strip())
        # 判断日志内容的开头, 并将开头所在的索引记录在 IList 中
        for line in DList:
            # 设置判断的初始条件
            is_Start = False                            # 特殊条件, 可以将 is_Start 变更为 True
            log_time_str = "Null"
            log_content_str = line.split(",", 5)[-1]    # 日志都可以用逗号分割为5段, 根据最后一段来判断是否是日志的开头
            # 匹配: "time=""2023-01-20T12:49:05Z"", T 是分隔符; Z 是 UTC
            if re.findall("time=.*\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", log_content_str):
                log_time_str = line.split(",", 1)[0][:-8]
            # 匹配: "2023-01-20T12:19:09,768"
            elif re.findall("\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2},\d{3}", log_content_str):
                log_time_str = line.split(",", 1)[0][:-8]
            # 匹配：12:18:36.944 [main]
            elif re.findall("\d{2}:\d{2}:\d{2}\.\d{3} \[", log_content_str):
                log_time_str = line.split(",", 1)[0][:-8]
            # 计算日志中的时间
            log_time = self.get_logtime(log_time_str)
            # 特殊条件
            if re.findall("Adding config|Applying config", log_content_str, re.IGNORECASE):
                is_Start = True
            # 在非时间的内容中, 如果该行包括 "Exception", "at ", " more", "Caused by" 这类字段, 则判断为多行, 其余为单行
            if is_Start == False:
                is_Match = False
                for key in ["Exception", "at ", " more", "Caused by", '"  ""', '"    ""', '"  },"', "status=eServiceOK coreID="]:
                    if key in log_content_str:
                            is_Start = False
                            is_Match = True
                if is_Match == False:
                        is_Start = True
            # 判断该行是否是日志的开头
            if log_time != "Null" or is_Start == True:
                IList.append(DList.index(line, now_idx))
            now_idx += 1
        # 根据 DList 的数据和 IList 索引来切分日志条目
        idx_list = []
        for idx in IList:
            idx_list.append(idx)
            if len(idx_list) == 1:
                pass
            else:
                try:
                    # 针对切分出来的每一份数据, 获取数据的每一部分
                    log_line = idx_list[0] + 1
                    log_data = DList[idx_list[0]:idx_list[1]]
                    idx_list.pop(0)
                    # 日志时间
                    log_time = self.get_logtime(log_data[0].split(",")[0][:-8].strip())
                    # 日志等级
                    log_level = "Null"
                    if re.findall("\d+\.\d+\.\d+\.\d+\ - - \[.*?\]", log_data[0], re.IGNORECASE):
                        log_level = "INFO"
                    elif re.findall("\[notice] \d+#\d+: signal process", log_data[0], re.IGNORECASE):
                        log_level = "INFO"
                    elif re.findall("level=.*msg=.*", log_data[0], re.IGNORECASE):
                        log_level = log_data[0].split(",", 5)[-1].split("level=")[-1].split(" msg=", 1)[0].upper().strip()
                    elif re.findall("- #.*: ", log_data[0], re.IGNORECASE):
                        log_level = log_data[0].split(",", 5)[-1].split("- #", 1)[-1].split(":", 1)[0].upper().strip()
                    elif re.findall("\D+\s+\[.*?\] .*", log_data[0], re.IGNORECASE):
                        log_level = log_data[0].split(",", 5)[-1].strip().split("[", 1)[0].strip()[1:]
                    elif re.findall("\[(.*?)\] .*", log_data[0], re.IGNORECASE):
                        log_level = log_data[0].split(",", 5)[-1].split("]", 1)[-1].strip().split(" ", 1)[0].strip()
                    elif re.findall("[WIE]\d{4} \d{2}:\d{2}:\d{2}.\d{6}\s+", log_data[0], re.IGNORECASE):
                        for log_key, log_val in {"I012":"INFO", "W012":"WARN", "E012":"ERROR"}.items():
                            if log_key in log_data[0]:
                                log_level = log_val
                    elif re.findall("Adding config|Applying config|Updating config|\S+_\S+=\S+|SHLVL=1|RANDFILE=/tmp/.rnd|container=oci", log_data[0], re.IGNORECASE):
                        log_level = "Config"
                    ### 日志等级, 如果上述条件都没有正确命中
                    if log_level not in ["TRACE", "DEBUG", "INFO", "WARN", "WARNING", "ERROR", "CRITICAL", "Config"]:
                        for key in ["trace", "TRACE", "debug", "DEBUG", "info", "INFO", "warn", "WARN", "warning", "WARNING", "error", "ERROR", "critical", "CRITICAL"]:
                            if key in log_data[0]:
                                log_level = key.upper()
                    if log_level not in ["TRACE", "DEBUG", "INFO", "WARN", "WARNING", "ERROR", "CRITICAL", "Config"]:
                        keywords = ["Can't", "Cannot", "Warning", "Failed", "Exception"]
                        for key in keywords:
                            if key in log_data[0]:
                                log_level = "ERROR"
                    if log_level == "WARNING":
                        log_level = "WARN"
                    # 日志组件
                    log_comp = log_data[0].split(",")[2] + "_" + log_data[0].split(",")[3] + "_" + log_data[0].split(",")[4]
                    # 日志内容
                    log_cont = ""
                    for line in log_data:
                        log_cont += line.split(",", 5)[-1] + "\n"
                    if re.findall("msg=", log_cont, re.IGNORECASE):
                        log_cont = log_cont.split("msg=", 1)[-1].strip()
                    elif re.findall("\d{2}:\d{2}:\d{2}\.\d{3} \[(.*?)\]", log_cont, re.IGNORECASE):
                        log_cont = log_cont.split(re.findall("\d{2}:\d{2}:\d{2}\.\d{3}", log_cont, re.IGNORECASE)[0], 1)[-1].strip()
                    elif re.findall("\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3} \[(.*?)\]", log_cont, re.IGNORECASE):
                        log_cont = log_cont.split(re.findall("\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}", log_cont, re.IGNORECASE)[0], 1)[-1].strip()
                    elif re.findall("\D+\s+\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3}\]", log_cont, re.IGNORECASE):
                        log_cont = "[" + log_cont.split("[", 1)[-1].strip()
                    ### 针对 BVD 日志的特殊处理
                    elif re.findall("\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}.*bvd:.*", log_cont, re.IGNORECASE):
                        log_cont = "bvd:" + log_cont.split("bvd:", 1)[-1].strip()
                    ### 针对 itom-monitoring 日志的特殊处理
                    elif re.findall("\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z\s+.*\s+line:", log_cont, re.IGNORECASE):
                        log_cont = "line:" + log_cont.split("line:", 1)[-1].strip()
                    elif re.findall("\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3} \S+ init:main", log_cont, re.IGNORECASE):
                        log_cont = "init:main" + log_cont.split("init:main", 1)[-1].strip()
                    elif re.findall("\[\d{2}m\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\s+.*:", log_cont, re.IGNORECASE):
                        log_cont = log_cont.split(re.findall("\[\d{2}m\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\s+.*:", log_cont)[0], 1)[-1].strip()
                    elif re.findall("\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3} - entry - ", log_cont, re.IGNORECASE):
                        log_cont = log_cont.split("- entry -", 1)[-1].strip()
                    elif re.findall("\S{3} \S{3} \d{2} \d{2}:\d{2}:\d{2} UTC \d{4} \S+:", log_cont, re.IGNORECASE):
                        log_cont = log_cont.split(re.findall("\S{3} \S{3} \d{2} \d{2}:\d{2}:\d{2} UTC \d{4} \S+:", log_cont, re.IGNORECASE)[0], 1)[-1].strip()
                    ### 针对 ingress-controller 日志的特殊处理
                    elif re.findall("\d+\.\d+\.\d+\.\d+\ - - \[.*?\]", log_cont, re.IGNORECASE):
                        log_cont = log_cont.split("]", 1)[-1].strip()
                    elif re.findall("\[notice] \d+#\d+: signal process", log_cont, re.IGNORECASE):
                        log_cont = "[notice]" + log_cont.split("[notice]", 1)[-1].strip()
                    ### 针对 itom-idm 日志的特殊处理
                    elif re.findall("\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{9}\+\d{2}:\d{2} \S+ \S+", log_cont, re.IGNORECASE):
                        log_cont = log_cont.split(" ", 1)[-1].strip()
                    elif re.findall("\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}\+\d{4} \S+\s+\[.*?]", log_cont, re.IGNORECASE):
                        log_cont = "[" + log_cont.split("[", 1)[-1].strip()
                    ### 针对 kube-registry 日志的特殊处理
                    elif re.findall("\[\d;\d{2}m\[E].*0m", log_cont, re.IGNORECASE):
                        log_cont = "[" + log_cont.split("[", 1)[-1].strip()
                    elif re.findall("\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2} http:", log_cont, re.IGNORECASE):
                        log_cont = "http:" + log_cont.split("http:", 1)[-1].strip()
                    # 检查黑名单, 如果不在, 则将数据放入 FList 中
                    is_Black = False
                    for blk in self.blkline:
                        if blk == log_cont:
                            is_Black = True
                    if is_Black == False:
                        # 将字典数据加入到 FList 中
                        FList.append({
                            "log_line": log_line,
                            "log_time": log_time,
                            "log_level": log_level,
                            "log_comp": log_comp,
                            "log_cont": log_cont,})
                except Exception as e:
                    # 模块模式
                    if __name__ != "__main__":
                        MultSQLLogger.error(e)
                    # 测试模式
                    else:
                        print(e)
        # 基于 FList 转换为 SQLAlchemy 类型的数据类型, 保存在 SList 中
        if __name__ != "__main__":
            # 针对文件做进一步分析, 来判断加载哪一个 SQL 表
            if re.findall("itomdipulsar-bookkeeper.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_DI_Pulsar_BookKeeper as OpsBTable
            elif re.findall("itomdipulsar-zookeeper.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_DI_Pulsar_Zookeeper as OpsBTable
            elif re.findall("itomdipulsar-broker.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_DI_Pulsar_Broker as OpsBTable
            elif re.findall("itomdipulsar-proxy.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_DI_Pulsar_Proxy as OpsBTable
            elif re.findall("itomdipulsar-minio-connector-post-upgrade-job.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_DI_Pulsar_Job as OpsBTable
            elif re.findall("itom-di-administration.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_DI_Administration as OpsBTable
            elif re.findall("itom-di-data-access-dpl.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_DI_Data_Access_DPL as OpsBTable
            elif re.findall("itom-di-metadata-server.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_DI_MetaData_Server as OpsBTable
            elif re.findall("itom-di-postload-taskcontroller.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_DI_Postload_TaskController as OpsBTable
            elif re.findall("itom-di-postload-taskexecutor.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_DI_Postload_TaskExecutor as OpsBTable
            elif re.findall("itom-di-receiver-dpl.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_DI_Receiver_DPL as OpsBTable
            elif re.findall("itom-di-scheduler-udx.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_DI_Scheduler_UDX as OpsBTable
            elif re.findall("itom-di-vertica-dpl.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_DI_Vertica_DPL as OpsBTable
            elif re.findall("bvd-ap-bridge-.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_BVD_AP_Bridge as OpsBTable
            elif re.findall("bvd-controller-deployment-.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_BVD_Controller_Deployment as OpsBTable
            elif re.findall("bvd-explore-deployment-.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_BVD_Explore_Deployment as OpsBTable
            elif re.findall("bvd-quexserv-.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_BVD_Quexserv as OpsBTable
            elif re.findall("bvd-receiver-deployment-.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_BVD_Receiver_Deployment as OpsBTable
            elif re.findall("bvd-redis-.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_BVD_Redis as OpsBTable
            elif re.findall("bvd-www-deployment-.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_BVD_WWW_Deployment as OpsBTable
            elif re.findall("itom-monitoring-admin-.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_Monitoring_Admin as OpsBTable
            elif re.findall("itom-monitoring-collection-autoconfigure-job-.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_Monitoring_Collection_AutoConfigure_Job as OpsBTable
            elif re.findall("itom-monitoring-collection-manager-.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_Monitoring_Collection_Manager as OpsBTable
            elif re.findall("itom-monitoring-job-scheduler-.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_Monitoring_Job_Scheduler as OpsBTable
            elif re.findall("itom-monitoring-oa-discovery-collector-.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_Monitoring_OA_Discovery_Collector as OpsBTable
            elif re.findall("itom-monitoring-oa-metric-collector-bg-.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_Monitoring_OA_Metric_Collector_BG as OpsBTable
            elif re.findall("itom-monitoring-oa-metric-collector-.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_Monitoring_OA_Metric_Collector as OpsBTable
            elif re.findall("itom-monitoring-service-data-broker-.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_Monitoring_Service_Data_Broker as OpsBTable
            elif re.findall("itom-opsb-content-manager-.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_OpsB_Content_Manager as OpsBTable
            elif re.findall("itom-ingress-controller-.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_Ingress_Controller as OpsBTable
            elif re.findall("frontend-ingress-controller-.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_Core_Frontend_Ingress_Controller as OpsBTable
            elif re.findall("portal-ingress-controller-.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_Core_Portal_Ingress_Controller as OpsBTable
            elif re.findall("itom-frontend-ui-.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_Core_Frontend_UI as OpsBTable
            elif re.findall("kube-registry-.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_Core_Kube_Registry as OpsBTable
            elif re.findall("itom-idm-.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_IDM as OpsBTable

            file_id = self.get_file_id(targetdb=self.targetdb, file=self.file, FileHash=FileHash)
            for data in FList:
                try:
                    SList.append(OpsBTable(
                        file_id=file_id,
                        log_line=data.get("log_line"),
                        log_time=datetime.strptime(data.get("log_time"), "%Y-%m-%d %H:%M:%S.%f"),
                        log_level=data.get("log_level"),
                        log_comp=data.get("log_comp"),
                        log_cont=data.get("log_cont")))
                except Exception as e:
                    MultSQLLogger.error(e)
                    MultSQLLogger.error("Faild File: " + self.file)
                    MultSQLLogger.error("Faild Line: " + line)

        # 模块模式下, 将结果数据返回
        if __name__ != "__main__":
            self.TaskInfo["data"] = SList
            return self.TaskInfo
        # 测试模式下, 打印 FList 数据
        else:
            for data in FList:
                print(data)

    def readlog_k8s_process(self):
        """
        OpsB logs
        # kubelet.*.log
        # containerd.*.log
        :return: TaskInfo["data"] = SList --> [sqlalchemy obj1, sqlalchemy obj2, ...]
        """
        # 模块模式下, 记录读取的文件名
        if __name__ != "__main__":
            MultSQLLogger.info("Reading File:[{}]".format(self.file))
        # 初始化变量
        DList = []  # 原始文档的每一行数据
        IList = []  # 日志开头的索引
        FList = []  # 切分完并处理完成的数据
        SList = []  # 转换为 SQL 语句的数据
        now_idx = 0

        # 读取文件, 将文件的每一行保存在 DList 中
        with open(self.file, mode="r", encoding=self.encoding, errors="replace") as file:
            for line in file:
                DList.append(line.strip())
        # 判断日志内容的开头, 并将开头所在的索引记录在 IList 中
        for line in DList:
            # 设置判断的初始条件
            log_time_str = "Null"
            log_content_str = line.split(",", 1)[0]
            if re.findall("\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{9}", log_content_str):
                log_time_str = line.split(",", 1)[0][:-8]
            # 计算日志中的时间
            log_time = self.get_logtime(log_time_str)
            # 判断该行是否是日志的开头
            if log_time != "Null":
                IList.append(DList.index(line, now_idx))
            now_idx += 1
        # 根据 DList 的数据和 IList 索引来切分日志条目
        idx_list = []
        for idx in IList:
            idx_list.append(idx)
            if len(idx_list) == 1:
                pass
            else:
                try:
                    # 针对切分出来的每一份数据, 获取数据的每一部分
                    log_line = idx_list[0] + 1
                    log_data = DList[idx_list[0]:idx_list[1]]
                    idx_list.pop(0)
                    # 日志时间
                    log_time = self.get_logtime(log_data[0].split(",")[0][:-8].strip())
                    # 日志等级
                    log_level = log_data[0].split(",")[1].strip().upper()
                    if log_level == "WARNING":
                        log_level = "WARN"
                    # 日志组件
                    log_comp = log_data[0].split(",")[2] + "_" + log_data[0].split(",")[4]
                    # 日志内容
                    log_cont = ""
                    for line in log_data:
                        log_cont += line.split(",", 5)[-1] + "\n"
                    # 检查黑名单, 如果不在, 则将数据放入 FList 中
                    is_Black = False
                    for blk in self.blkline:
                        if blk == log_cont:
                            is_Black = True
                    if is_Black == False:
                        # 将字典数据加入到 FList 中
                        FList.append({
                            "log_line": log_line,
                            "log_time": log_time,
                            "log_level": log_level,
                            "log_comp": log_comp,
                            "log_cont": log_cont,})
                except Exception as e:
                    # 模块模式
                    if __name__ != "__main__":
                        MultSQLLogger.error(e)
                    # 测试模式
                    else:
                        print(e)
        # 基于 FList 转换为 SQLAlchemy 类型的数据类型, 保存在 SList 中
        if __name__ != "__main__":
            # 针对文件做进一步分析, 来判断加载哪一个 SQL 表
            if re.findall("kubelet.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_K8S_Kubelet as OpsBTable
            elif re.findall("containerd.*\.log", self.file, re.IGNORECASE):
                from rules.MicroFocus.ITOM.OpsB_SQLTable import ITOM_K8S_Containerd as OpsBTable

            file_id = self.get_file_id(targetdb=self.targetdb, file=self.file, FileHash=FileHash)
            for data in FList:
                SList.append(OpsBTable(
                    file_id=file_id,
                    log_line=data.get("log_line"),
                    log_time=datetime.strptime(data.get("log_time"), "%Y-%m-%d %H:%M:%S.%f"),
                    log_level=data.get("log_level"),
                    log_comp=data.get("log_comp"),
                    log_cont=data.get("log_cont")))

        # 模块模式下, 将结果数据返回
        if __name__ != "__main__":
            self.TaskInfo["data"] = SList
            return self.TaskInfo
        # 测试模式下, 打印 FList 数据
        else:
            for data in FList:
                print(data)

if __name__ == "__main__":
    # 读取测试文件
    file = r"D:\opsb_test_log\itomdipulsar-bookkeeper-test-file.log"
    test = OpsBFiles({"file": file})