## Environment
OA 12.x

## Situation
如何检查 OA ASSD (Agent Side System Detection) 的数据

## Resolution
- Windows
    ```shell
    ovodetect -verbose
    # 请在 cmd 中执行, 然后截图
    ```

- Unix Like
    ```shell
    export PATH=$PATH:/opt/OV/bin
    ovodetect -verbose
    # 如果想输出到文件, 可以执行 ovodetect -verbose > oa_assd.txt
    ```