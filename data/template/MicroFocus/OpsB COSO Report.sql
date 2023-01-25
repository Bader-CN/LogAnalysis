SELECT file_id, log_line, log_time, log_level, log_comp, log_cont FROM (
    SELECT * FROM opsb_itom_ingress_controller UNION
    SELECT * FROM opsb_itom_di_administration UNION
    SELECT * FROM opsb_itom_di_data_access_dpl UNION
    SELECT * FROM opsb_itom_di_metadata_server UNION
    SELECT * FROM opsb_itom_di_postload_receiver_dpl UNION
    SELECT * FROM opsb_itom_di_postload_taskcontroller UNION
    SELECT * FROM opsb_itom_di_postload_taskexecutor UNION
    SELECT * FROM opsb_itom_di_pulsar_bookkeeper UNION
    SELECT * FROM opsb_itom_di_pulsar_broker UNION
    SELECT * FROM opsb_itom_di_pulsar_job UNION
    SELECT * FROM opsb_itom_di_pulsar_proxy UNION
    SELECT * FROM opsb_itom_di_pulsar_zookeeper UNION
    SELECT * FROM opsb_itom_di_scheduler_udx UNION
    SELECT * FROM opsb_itom_di_vertica_dpl
    )
WHERE log_level != "INFO"
ORDER BY log_time DESC;