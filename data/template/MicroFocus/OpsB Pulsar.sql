SELECT file_id, log_line, log_time, log_level, log_comp, log_cont FROM (
    SELECT * FROM opsb_itom_di_pulsar_bookkeeper UNION
    SELECT * FROM opsb_itom_di_pulsar_broker UNION
    SELECT * FROM opsb_itom_di_pulsar_job UNION
    SELECT * FROM opsb_itom_di_pulsar_proxy UNION
    SELECT * FROM opsb_itom_di_pulsar_zookeeper
    )
WHERE log_level != "INFO"
ORDER BY log_time DESC;