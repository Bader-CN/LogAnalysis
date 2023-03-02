SELECT filehash.filepath, log_line, log_time, log_level, log_comp, log_cont FROM filehash
INNER JOIN (
    SELECT file_id, log_line, log_time, log_level, log_comp, log_cont FROM (
	SELECT * FROM opsb_itom_di_administration UNION
	SELECT * FROM opsb_itom_di_data_access_dpl UNION
	SELECT * FROM opsb_itom_di_metadata_server UNION
	SELECT * FROM opsb_itom_di_postload_taskcontroller UNION
	SELECT * FROM opsb_itom_di_postload_taskexecutor UNION
	SELECT * FROM opsb_itom_di_receiver_dpl UNION
	SELECT * FROM opsb_itom_di_scheduler_udx)
	)
ON filehash.id == file_id
WHERE log_level != "INFO"
ORDER BY log_time DESC;