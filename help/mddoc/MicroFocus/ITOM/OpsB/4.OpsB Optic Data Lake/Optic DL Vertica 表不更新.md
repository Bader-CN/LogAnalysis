## Environment
OBM 2021.11

## Situation
Optic Data Lake 中 Vertica 中表的时间停止更新了

## Cause
出现这种情况, 一般有2个原因

1. 任务被卡在 DISPATCHED 或 RUNNING 或 FINISHED 状态, 而在任务恢复之前已经升级了套件
2. 任务相关的信息在 OPTIC DL Message Bus 中丢失

## Resolution
1. 将 `itom-di-postload-taskcontroller` 和 `itom-di-postload-taskexecutor` 的 deployment 数量降为 0
    ```shell
    kubectl scale deployment itom-di-postload-taskcontroller --replicas=0 -n <suite namespace>
    kubectl scale deployment itom-di-postload-taskexecutor --replicas=0 -n <suite namespace>
    ```
2. 使用 `kubetl exec` 命令进入 pulsar bastion 这个 pod
    ```shell
    kubectl exec -it <bastion pod> -n <suite namespace> -c pulsar -- bash
    ```
3. 在 pulsar bastion 这个 pod 中执行如下命令, 执行完毕后可以按 `Ctrl + D` 退出这个 pod
    ```shell
    bin/pulsar-admin topics delete-partitioned-topic -f persistent://public/itomdipostload/di_internal_postload_state
    bin/pulsar-admin topics delete-partitioned-topic -f persistent://public/itomdipostload/di_postload_task_status_topic
    bin/pulsar-admin topics delete-partitioned-topic -f persistent://public/itomdipostload/di_postload_task_topic
    ```
4. 将 `itom-di-postload-taskcontroller` 和 `itom-di-postload-taskexecutor` 的 deployment 数量恢复为原来的值
    ```shell
    kubectl scale deployment itom-di-postload-taskcontroller --replicas=<replica count> -n <suite namespace>
    kubectl scale deployment itom-di-postload-taskexecutor --replicas=<replica count> -n <suite namespace>
    ```

## Additional Information
- [Aggregate not happening after upgrade](https://docs.microfocus.com/doc/Containerized_Operations_Bridge/2021.11/Aggregateissueafterupgrade)