SELECT
    log_time,
    Round(heap_free/heap_max, 2) as heap_percent_free_max,
    heap_used, heap_commit, heap_max, heap_free,
    log_line, filehash.filepath
FROM obm_jvm_statistics, filehash
WHERE filehash.id == file_id
ORDER BY log_time DESC;