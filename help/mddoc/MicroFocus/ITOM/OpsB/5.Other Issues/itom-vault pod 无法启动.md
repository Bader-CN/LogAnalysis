## Environment
OpsB 2022.05

## Situation
K8S 的 itom-vault pod 初始化, 如果执行 kubectl log <pod> 命令可以看到如下错误
```shell
FATAL Vault passphrase and credential already exists, but vault data is empty, stop init.
```

## Cause
这个问题通常是由密钥丢失导致的, 通常只能通过备份数据恢复, 否则只能重装

## Resolution
1. 停止 itom-vault 部署
   ```shell
   kubectl scale deployment itom-vault -n core --replicas=0
   ```
2. 备份当前 vault 数据
   ```shell
   # vault 应该在 NFS 中的 core/data 路径下
   cp /var/vols/itom/core/vault/data /tmp/data
   # 删除当前的 vault 数据
   rm -rf /var/vols/itom/core/vault/data/*
   ```
3. 恢复 vault 数据
   ```shell
   # 该命令路径仅仅是举例, 实际需要自行查找
   tar -xzvf /var/vols/itom/core/vault/backup/<data_x>/backup_data.tgz /var/vols/itom/core/vault/data/ 
   ```
4. 启动 itom-vault 部署
   ```shell
   kubectl scale deployment itom-vault -n core --replicas=1
   ```