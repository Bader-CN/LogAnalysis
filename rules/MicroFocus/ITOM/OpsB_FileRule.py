# -*- coding: utf-8 -*-

# 文件级别的匹配规则, 支持正则表达式
NeedFilesRule = [
    # OpsB statefulsets.apps
    "itomdipulsar-bookkeeper.*\.log",
    "itomdipulsar-zookeeper.*\.log",
    # OpsB deployments.apps
    "itomdipulsar-broker.*\.log",
    "itomdipulsar-proxy.*\.log",
    "itom-di-administration.*\.log",
    "itom-di-data-access-dpl.*\.log",
    "itom-di-metadata-server.*\.log",
    "itom-di-postload-taskcontroller.*\.log",
    "itom-di-postload-taskexecutor.*\.log",
    "itom-di-receiver-dpl.*\.log",
    "itom-di-scheduler-udx.*\.log",
    "itom-di-vertica-dpl.*\.log",
    "bvd-ap-bridge-.*\.log",
    "bvd-controller-deployment-.*\.log",
    "bvd-explore-deployment-.*\.log",
    "bvd-quexserv-.*\.log",
    "bvd-receiver-deployment-.*\.log",
    "bvd-redis-.*\.log",
    "bvd-www-deployment-.*\.log",
    # OpsB Jobs
    "itomdipulsar-minio-connector-post-upgrade-job.*\.log",
]

# 文件级别的反匹规则, 支持正则表达式
BlckFilesRule = []