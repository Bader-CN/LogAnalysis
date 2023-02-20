## Environment
OA 12.x

## Situation 
如何开启 OA HPSensor 的 trace 日志?

## Resolution
- 修改方法
    ```shell
    # 将 hpcs.conf 中的 hpcs.trace.Debug_Level 修改为 DEBUG
    [hpcs.trace]
    Debug_Level=DEBUG
    ```
- 文件位置
    ```shell
    # Windows
      配置: %ovdatadir%\hpcs\hpcs.conf
      日志: %ovdatadir%\hpcs\hpcstrace.log
    # Linux
      配置: /var/opt/OV/hpcs/hpcs.conf
      日志: /var/opt/OV/hpcs/hpcstrace.log
    ```