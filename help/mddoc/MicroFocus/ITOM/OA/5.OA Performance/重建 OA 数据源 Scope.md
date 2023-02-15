## Environment
OA 12.x

## Situation 
如何重建 OA 数据源 (DataSource)

## Resolution
1. 停止 oacore 进程
    ```shell
    ovc -stop oacore
    ```
2. 重建 class
    ```shell
    ovconfchg -ns oacore -set UPDATED_MODEL_AVAILABLE true
    ```
3. 启动 oacore 进行
    ```shell
    ovc -start oacore
    ```
## Additional Information
<https://docs.microfocus.com/itom/Operations_Agent:12.23/MiscellaneousTS>
