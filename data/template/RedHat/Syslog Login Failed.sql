SELECT file_id, log_line, log_time, log_level, log_comp, log_cont FROM syslog_secure
WHERE log_level != "INFO"
ORDER BY log_time DESC;