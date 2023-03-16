## Environment
OBM 2020.x 及以上版本

## Situation 
如何在 OBM 上控制 OA 远程执行指令

## Resolution
可以使用 ovdeploy -cmd 命令
```shell
# Linux
/opt/OV/bin/ovdeploy -cmd <command> -ovrg server -host <node_ip/fqdn>
# Windows
ovdeploy -cmd <command> -ovrg server -host <node_ip/fqdn>
```