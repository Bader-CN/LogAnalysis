## Environment
OA 12.x

## Situation 
当 OA 上包含多个 IP 地址时, 如何绑定通信的 IP 地址?

## Resolution
```shell
# SERVER_BIND_ADDR - Specifies the bind address of a http server
# CLIENT_BIND_ADDR - Bind address for the client requests
ovconfchg -ns eaagt -set OPC_IP_ADDRESS <IP_Address>
ovconfchg -ns bbc.cb -set SERVER_BIND_ADDR <IP_Address>
ovconfchg -ns bbc.http -set SERVER_BIND_ADDR <IP_Address>
ovconfchg -ns bbc.http -set CLIENT_BIND_ADDR <IP_Address>

# 绑定完成后, 请重启 OA 进程
ovc -kill
ovc -start
# 使用 opcagt -cleanstart 也可以
opcagt -cleanstart
```

## Additional Information
- [ConfigurationVariablesCommunicationComponent](https://docs.microfocus.com/doc/Operations_Agent/12.23/ConfigurationVariablesCommunicationComponent)
- [NodeResolutionOverview](https://docs.microfocus.com/doc/Operations_Agent/12.23/NodeResolutionOverview)