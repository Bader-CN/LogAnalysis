## 定制文件规则
1. 添加对应的文件读取规则
   - SQLTable
   - FileRule
   - InsertRule

2. 修改 category_dict 字典中的内容
   - path<br>
     module.gui.LogImport_md.LogAnalysisImport.category_dict
   - goal<br>
     修改 category_dict 字典中的内容

3. 修改 check_taskdict 函数
   - path<br>
     module.gui.LogAnalysis_md.LogAnalysisMain.check_taskdict()
   - goal<br>
     在 check_taskdict 方法中加载 FileRule 和 SQLTable 规则

4. 修改 logfile_to_sql 函数
   - path<br>
     LogAnalysis.logfile_to_sql(QTask, QData)
   - goal<br>
     在 logfile_to_sql 方法中加载 InsertRule 规则