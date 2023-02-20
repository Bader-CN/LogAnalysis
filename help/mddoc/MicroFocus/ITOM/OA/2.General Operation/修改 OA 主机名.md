## Environment
OA 12.x

## Situation 
如何修改 OA 传递数据时携带的主机名

## Resolution
```shell
# 不能修改 OPC_NODENAME, 这位这是一个内部参数, 重启后会自动覆盖
# 这个修改通常用于调整 PrimaryDnsName 的值, 该值用于 UCMDB 的合并规则
ovconfchg -ns xpl.net -set LOCAL_NODE_NAME <HostName/FQDN>
ovconfchg –ns eaagt –set OPC_NAMESRV_LOCAL_NAME <HostName/FQDN>
```

## Additional Information
- [NodeResolutionOverview](https://docs.microfocus.com/itom/Operations_Agent:12.23/NodeResolutionOverview)