SELECT
    logs.log_line, logs.log_time, logs.log_level, logs.log_comp, logs.log_cont, f.filepath
FROM (
    SELECT * FROM obm_opr_gateway UNION
    SELECT * FROM obm_opr_gateway_flowtrace UNION
    SELECT * FROM obm_opr_backend UNION
    SELECT * FROM obm_opr_backend_flowtrace
) as logs
-- logs 和 filehash 表进行拼接, 条件为 logs.file_id = f.id (使用 ON 关键字)
JOIN filehash as f ON logs.file_id = f.id
WHERE logs.log_level != 'INFO'
ORDER BY logs.log_time DESC;