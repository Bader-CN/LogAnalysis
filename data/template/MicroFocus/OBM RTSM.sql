SELECT file_id, log_line, log_time, log_level, log_comp, log_cont FROM (
    SELECT * FROM obm_cmdb_reconciliation_error UNION
    SELECT * FROM obm_cmdb_reconciliation_datain_merged UNION
    SELECT * FROM obm_cmdb_reconciliation_datain_ignored UNION
    SELECT * FROM obm_cmdb_reconciliation_datain_multiplematch
    )
WHERE log_level != "INFO"
ORDER BY log_time DESC;