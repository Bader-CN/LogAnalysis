SELECT file_id, log_line, log_time, log_level, log_comp, log_cont FROM (
    SELECT * FROM obm_opr_gateway UNION
    SELECT * FROM obm_bus UNION
    SELECT * FROM obm_opr_backend UNION
    SELECT * FROM obm_scripts UNION
    SELECT * FROM obm_opr_scripting_host
	 )
WHERE log_level != "INFO"
ORDER BY log_time DESC;