SELECT
    log_time,
    Round(non_heap_free/non_heap_max, 2) as non_heap_percent_free_max,
    non_heap_used, non_heap_commit, non_heap_max, non_heap_free,
    log_line, filehash.filepath
FROM obm_jvm_statistics, filehash
WHERE filehash.id == file_id
ORDER BY log_time DESC;