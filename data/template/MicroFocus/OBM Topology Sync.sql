SELECT file_id, log_line, log_time, log_level, log_comp, log_cont FROM (
    SELECT * FROM obm_opr_svcdiscserver UNION
    SELECT * FROM obm_opr_svcdiscserver_citrace UNION
    SELECT * FROM obm_ovsvcdiscserver
    )
WHERE log_level != "INFO"
ORDER BY log_time DESC;