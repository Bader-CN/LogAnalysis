## Environment
OA 12.x

## Situation
如何拦截 (Intercept) 并修改 OA internal messages

## Resolution
1. 设置 `OPC_INT_MSG_FLT` 参数为 `True`
    ```shell
    ovconfchg -ns eaagt -set OPC_INT_MSG_FLT TRUE
    ```
2. 重启 OA 进程
    ```shell
    ovc -restart / opcagt -cleanstart
    ```
3. 部署一个消息接口类型的 Policy (Message Interface) 

## Additional Information
<https://docs.microfocus.com/itom/Operations_Agent:12.23/ConfigurationVariablesMonitoringComponent>
