# -*- coding: utf-8 -*-

from multiprocessing import Queue

QTask = Queue()  # 向子进程发布任务
QData = Queue()  # 子进程处理完成的数据