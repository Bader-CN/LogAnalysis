SELECT * FROM (
    SELECT file_id, log_line, log_time, log_level, log_comp, log_cont FROM obm_opr_svcdiscserver UNION
    SELECT file_id, log_line, log_time, log_level, log_comp, log_cont FROM obm_opr_svcdiscserver_citrace)
WHERE log_level != "INFO"
ORDER BY log_time DESC;