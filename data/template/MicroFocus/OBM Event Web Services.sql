SELECT file_id, log_line, log_time, log_level, log_comp, log_cont FROM (
    SELECT * FROM obm_opr_webapp UNION
    SELECT * FROM obm_opr_ws_response
    )
WHERE log_level != "INFO"
ORDER BY log_time DESC;