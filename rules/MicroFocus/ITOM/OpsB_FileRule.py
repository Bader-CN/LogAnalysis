# -*- coding: utf-8 -*-

# 文件级别的匹配规则, 支持正则表达式
NeedFilesRule = [
    # OpsB statefulsets.apps
    "itomdipulsar-bookkeeper.*\.log",
    "itomdipulsar-zookeeper.*\.log",
    # OpsB deployments.apps
    "itomdipulsar-broker.*\.log",
    "itomdipulsar-proxy.*\.log",
    "itom-di-administration.*\.log",
    "itom-di-data-access-dpl.*\.log",
    "itom-di-metadata-server.*\.log",
    "itom-di-postload-taskcontroller.*\.log",
    "itom-di-postload-taskexecutor.*\.log",
    "itom-di-receiver-dpl.*\.log",
    "itom-di-scheduler-udx.*\.log",
    "itom-di-vertica-dpl.*\.log",
    "bvd-ap-bridge-.*\.log",
    "bvd-controller-deployment-.*\.log",
    "bvd-explore-deployment-.*\.log",
    "bvd-quexserv-.*\.log",
    "bvd-receiver-deployment-.*\.log",
    "bvd-redis-.*\.log",
    "bvd-www-deployment-.*\.log",
    "itom-monitoring-admin-.*.log",
    "itom-monitoring-collection-manager-.*\.log",
    "itom-monitoring-oa-discovery-collector-.*\.log",
    "itom-monitoring-oa-metric-collector-.*\.log",
    "itom-monitoring-oa-metric-collector-bg-.*\.log",
    "itom-monitoring-service-data-broker-.*\.log",
    "itom-opsb-content-manager-.*\.log",
    "itom-ingress-controller-.*\.log",
    # OpsB Jobs
    "itomdipulsar-minio-connector-post-upgrade-job.*\.log",
    "itom-monitoring-collection-autoconfigure-job-.*\.log",
    "itom-monitoring-job-scheduler-.*\.log",
    # OpsB core deployments.apps
    "frontend-ingress-controller-.*\.log",
    "portal-ingress-controller-.*\.log",
    "itom-frontend-ui-.*\.log",
    "kube-registry-.*\.log",
    # OpsB IDM (core/itom)
    "itom-idm-.*\.log",
    # OpsB K8S Service.sql
    "kubelet\.\d+.log",
    "containerd.\d+.log",
]

# 文件级别的反匹规则, 支持正则表达式
BlckFilesRule = [
    # itom-idm 的 Pod 中有相关信息, 并且格式不对
    "idm-service\.log",
    "idm-loader\.log",
    "startidm\.sh\.log",
]