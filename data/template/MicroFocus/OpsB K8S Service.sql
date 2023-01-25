SELECT file_id, log_line, log_time, log_level, log_comp, log_cont FROM (
    SELECT * FROM k8s_service_containerd UNION
    SELECT * FROM k8s_service_kubelet
    )
WHERE log_level != "INFO"
ORDER BY log_time DESC;