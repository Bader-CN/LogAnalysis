## Environment
OpsB 2021.11

## Situation
执行 systemctl start kubelet.service 时提示无法启动, 并在 `kube-start.<date>.log` 中提示如下信息
```shell
kubelet.service - Kubernetes Kubelet
   Loaded: loaded (/usr/lib/systemd/system/kubelet.service; enabled; vendor preset: disabled)
   Active: activating (auto-restart) (Result: exit-code) since <date>; 3s ago
     Docs: https://github.com/GoogleCloudPlatform/kubernetes
  Process: ***** ExecStopPost=/bin/bash -c rm -f /run/kubelet.pid (code=exited, status=0/SUCCESS)
  Process: ***** ExecStartPost=/bin/bash -c umask 0022; pgrep -x kubelet > /run/kubelet.pid (code=exited, status=1/FAILURE)
  Process: ***** ExecStart=/opt/cdf/bin/kubelet ***(code=killed, signal=TERM)
Main PID: ***** (code=killed, signal=TERM)
```

## Cause
这个问题应该 kubelet 服务的启动脚本有问题导致的<br>
脚本中应该包括类似如下的代码
```shell
ExecStopPost=/bin/bash -c rm -f /run/kubelet.pid
ExecStartPost=/bin/bash -c umask 0022; pgrep -x kubelet > /run/kubelet.pid
```
如果 kubelet 在启动时无法执行上述命令, 则会提示此错误

## Resolution
1. 登录 OpsB Master 服务器并停止 K8S 集群
   ```shell
   /opt/kubernetes/bin/kube-stop.sh
   ```
2. 打开 /usr/lib/systemd/system/kubelet.service 文件并删除或注释如下内容
   ```shell
   # 删除 / 注释这两行内容
   ExecStartPost=/bin/bash -c 'umask 0022; pgrep -x kubelet > /run/kubelet.pid'
   ExecStopPost=/bin/bash -c 'rm -f /run/kubelet.pid'
   ```
3. 启动 OpsB K8S 集群
    ```shell
    /opt/kubernetes/bin/kube-start.sh
    ```