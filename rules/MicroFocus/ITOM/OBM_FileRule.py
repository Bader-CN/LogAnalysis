# -*- coding: utf-8 -*-

# 文件级别的匹配规则, 支持正则表达式
NeedFilesRule = [
    # OBM Gateway logs
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
]

# 文件级别的反匹规则, 支持正则表达式
BlckFilesRule = []