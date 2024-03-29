# -*- coding: utf-8 -*-

# 文件级别的匹配规则, 支持正则表达式
NeedFilesRule = [
    # OBM logs
    "opr-gateway\.log",
    "opr-gateway-flowtrace\.log",
    "opr-scripting-host\.log",
    "opr-configserver\.log",
    "opr-webapp\.log",
    "opr-ws-response\.log",
    "user_stats_log_filter\.log",
    "login\.log",
    "UserActions.servlets\.log",
    "opr-svcdiscserver\.log",
    "opr-svcdiscserver-citrace\.log",
    "pmi\.log",
    "bvd\.log",
    "downtime\.log",
    "opr-clis\.log",
    "opr-heartbeat\.log",
    "opr-backend\.log",
    "opr-flowtrace-backend\.log",
    "bus\.log",
    "opr-ciresolver\.log",
    "scripts\.log",
    "nanny_all\.log",
    "wrapper\.log",
    "jvm_statistics\.log",
    "OvSvcDiscServer\.log",
    # OBM Config file
    "opr-checker-xml\.txt",
    # OBM RTSM.sql log
    "cmdb\.reconciliation\.error.*log",
    "cmdb\.reconciliation\.datain\.merged.*log",
    "cmdb\.reconciliation\.datain\.ignored.*log",
    "cmdb\.reconciliation\.datain\.multiplematch.*log",
]

# 文件级别的反匹规则, 支持正则表达式
BlckFilesRule = []