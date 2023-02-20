## Environment
OBM 2021.05

## Situation
检查 itomdipulsar-bookkeeper 相关 Pod 日志, 会提示无法 持久化(Persistent) Topic

## Cause
Apache Pulsar 的数据是基于 Topic 来存储的<br>
如果 Topic 没有创建的话, 那么消息是无法被缓存的

## Resolution
1. 进入 Pulsar bastion pod
   ```shell
   # bastion pod 名字可以使用 kubectl get pods -A 命令来查看
   kubectl exec -it <bastion pod> -c pulsar -n <suite namespace> -- bash
   ```
2. 检查 & 创建 Topic
   ```shell
   # list the topics
   # eg: persistent://public/default/di_task_status_topic-partition-0
   # -> di_task_status_topic 就是 topic name
   ./bin/pulsar-admin topics list public/default
   
   # 创建一个 topic, -s | -subscription-name 是一个 Subscription name
   ./bin/pulsar-client consume -s test-subscription -n 0 <topic name>
   # 删除一个 topic
   ./bin/pulsar-admin topics unsubscribe -s test-subscription -f <topic name>
   ```

## Additional Information
- [How to check if OPTIC DL Message Bus topics and data is created](https://docs.microfocus.com/doc/Containerized_Operations_Bridge/2022.05/CheckTopicData)
- [Pulsar command-line tools](https://pulsar.apache.org/docs/2.10.x/reference-cli-tools/#pulsar-client)