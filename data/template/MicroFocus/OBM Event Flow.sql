SELECT * FROM (
    SELECT file_id, log_line, log_time, log_level, log_comp, log_cont FROM obm_opr_gateway UNION
    SELECT file_id, log_line, log_time, log_level, log_comp, log_cont FROM obm_opr_gateway_flowtrace UNION
    SELECT file_id, log_line, log_time, log_level, log_comp, log_cont FROM obm_opr_backend UNION
    SELECT file_id, log_line, log_time, log_level, log_comp, log_cont FROM obm_opr_backend_flowtrace)
WHERE log_level != "INFO"
ORDER BY log_time DESC;