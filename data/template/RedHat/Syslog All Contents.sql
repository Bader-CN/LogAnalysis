SELECT file_id, log_line, log_time, log_level, log_comp, log_cont FROM(
    SELECT * FROM syslog_cron UNION
    SELECT * FROM syslog_maillog UNION
    SELECT * FROM syslog_messages UNION
    SELECT * FROM syslog_secure
    )
ORDER BY log_time DESC;