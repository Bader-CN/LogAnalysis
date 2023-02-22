# -*- coding: utf-8 -*-

# 文件级别的匹配规则, 支持正则表达式
NeedFilesRule = [
    # itom_di_administration
    "administration\.log",
    "administration-audit\.log",
    # itom_di_data_access_dpl
    "dataaccess\.log",
    # itom_di_metadata_server
    "metadata-server-app\.log",
    # itom_di_postload_taskcontroller
    "taskcontroller\.log",
    # itom_di_postload_taskexecutor
    "aggregate\.log",
    "csv-direct-load\.log",
    "forecast\.log",
    "perl-task\.log",
    "taskexecutor\.log",
    # itom_di_receiver_dpl
    "receiver-itom-di-receiver-dpl.*\.log",
    "receiver-out\.log",
    # itom_di_scheduler_udx
    "scheduler\.log",
    # itom_idm
    "idm-loader\.log",
    "idm-service\.log",
]

# 文件级别的反匹规则, 支持正则表达式
BlckFilesRule = [
]