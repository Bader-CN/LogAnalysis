SELECT file_id, log_line, log_time, log_level, log_comp, log_cont FROM (
    SELECT * FROM opsb_itom_ingress_controller UNION
    SELECT * FROM opsb_core_and_itom_idm UNION
    SELECT * FROM opsb_itom_bvd_ap_bridge UNION
    SELECT * FROM opsb_itom_bvd_controller_deployment UNION
    SELECT * FROM opsb_itom_bvd_explore_deployment UNION
    SELECT * FROM opsb_itom_bvd_quexserv UNION
    SELECT * FROM opsb_itom_bvd_receiver_deployment UNION
    SELECT * FROM opsb_itom_bvd_redis UNION
    SELECT * FROM opsb_itom_bvd_www_deployment
    )
WHERE log_level != "INFO"
ORDER BY log_time DESC;