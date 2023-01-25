SELECT file_id, log_line, log_time, log_level, log_comp, log_cont FROM (
    SELECT * FROM opsb_core_portal_ingress_controller UNION
    SELECT * FROM opsb_core_frontend_ingress_controller UNION
    SELECT * FROM opsb_itom_ingress_controller UNION
    SELECT * FROM opsb_core_and_itom_idm
    )
WHERE log_level != "INFO"
ORDER BY log_time DESC;