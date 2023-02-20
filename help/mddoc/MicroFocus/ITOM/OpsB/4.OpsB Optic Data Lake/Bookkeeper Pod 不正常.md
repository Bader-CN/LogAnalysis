## Environment
OBM 2021.05

## Situation
itomdipulsar-bookkeeper 相关 Pod 状态不正常

## Cause
一般是由于磁盘满了导致的(超过 95%), 此时会导致 bookkeeper 进入只读状态

## Resolution
可以考虑将 Optic Data Message Bus 缓存全都删除掉(实际是 Apache Pulsar 消息队列中的数据)
1. 停止 OpsB 相关 Pods
    ```shell
    /opt/kubernetes/scripts/cdfctl.sh runlevel set -l DOWN -n <suite namespace>
    ```
2. 在 K8S 的每个 worker 节点上, 清理 Optic Data Message Bus 中的内容
    ```shell
    # 实际路径可以使用 kubectl get pv / kubectl describe pv <pv_name> 来查看 
    cd <path to the volume used by Optic Data Message Bus pods>
    rm –rf *
    ```
3. 登录 Vertica DB, 然后 Drop 掉 Vertica Streaming Loader schema
    ```shell
    # <schema name> 名字默认为 itom_di_scheduler_provider_default
    # eg: DROP SCHEMA itom_di_scheduler_provider_default CASCADE
    DROP SCHEMA <schema name> CASCADE;
    ```
4. 启动 OpsB 相关 Pods
    ```shell
    /opt/kubernetes/scripts/cdfctl.sh runlevel set -l UP -n <suite namespace>
    ```
5. 使用如下命令将 Pods 的状态变为 Running
    ```shell
    # For noop=true, you must use a parameter that isn't used in any of the suite charts
    helm upgrade <release name> <suite chart path> -n <suite namespace> --set noop=true --reuse-values
    ```
6. 检查 BookKeeper pods 写入状态
   - 导航到 COSO Health Insights > Pulsar - Bookie Metrics dashboard
   - 检查 Bookies panel 是否至少有 2 个 BookKeeper pods 处于可写入的状态

## Additional Information
- [The itomdipulsar-bookkeeper pods are not accessible](https://docs.microfocus.com/doc/Containerized_Operations_Bridge/2021.05/BookkeeperReadOnly)