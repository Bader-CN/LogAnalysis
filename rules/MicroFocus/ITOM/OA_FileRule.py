# -*- coding: utf-8 -*-

# 文件级别的匹配规则, 支持正则表达式
NeedFilesRule = [
    # OA 基本日志
    'system\.txt',
    # OA policy 相关文件
    '\w{8}-\w{4}-\w{4}-\w{4}-\w{12}_header\.xml',

    # OA Trace 日志文件
    'trace_\d+\.txt',
    'ovcd_\d+\.txt',
    'oacore_\d+\.txt',
    'ovbbccb_\d+\.txt',
    'opcmsga_\d+\.txt',
    'opcmona_\d+\.txt',
]

# 文件级别的反匹规则, 支持正则表达式
BlckFilesRule = [
    # OA 日志里通常有2份, 可以考虑去掉这个
    r'\\public\\System.txt',
    # 出现于 OpsB 的 OA 中
    r'\\PaxHeaders',
]