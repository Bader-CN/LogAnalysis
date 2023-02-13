# -*- coding: utf-8 -*-

# 文件级别的匹配规则, 支持正则表达式
NeedFilesRule = [
    # ITOM 基本日志
    'system\.txt',
    # ITOM policy 相关文件
    '\w{8}-\w{4}-\w{4}-\w{4}-\w{12}_header\.xml',
    # ITOM agent.log
    'agent\.log_\d+-\d+-\d+_\d+\.\d+',
    # ITOM hpcstrace.log
    "hpcstrace\.log",
]

# 文件级别的反匹规则, 支持正则表达式
BlckFilesRule = [
    # ITOM 日志里通常有2份, 可以考虑去掉这个
    r'\\public\\System.txt',
    # 出现于 OpsB 的 ITOM 中
    r'\\PaxHeaders',
]