# -*- coding: utf-8 -*-

# 文件级别的匹配规则, 支持正则表达式
NeedFilesRule = [
    # OpsB statefulsets.apps
    "itomdipulsar-bookkeeper.*\.log",
    "itomdipulsar-zookeeper.*\.log",
    # OpsB deployments.apps
    "itomdipulsar-broker.*\.log",
]

# 文件级别的反匹规则, 支持正则表达式
BlckFilesRule = []