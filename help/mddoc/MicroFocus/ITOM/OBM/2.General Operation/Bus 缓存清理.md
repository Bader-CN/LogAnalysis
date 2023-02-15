## Environment
OBM 2020.x

## Situation 
如何删除 OBM Bus 的缓存 (Cache)

## Resolution
1. 停止所有的 DPS 服务器 (先停止 Backup DPS, 再停止 Active DPS)
    ```shell
    # Linux
    /opt/HP/BSM/opr/support/opr-support-utils.sh -stop bus
    # Windows
    C:\HPBSM\opr\support\opr-support-utils.bat -stop bus
    ```

2. 删除下列文件夹里面的内容 (需要保留文件夹)
    ```shell
    %TOPAZ_HOME%\bus\bindings
    %TOPAZ_HOME%\bus\journal
    %TOPAZ_HOME%\bus\large-messages
    %TOPAZ_HOME%\bus\paging 
    ```

3. 启动所有的 DPS 服务器 (先启动 Active DPS, 再启动 Backup DPS)
    ```shell
    # Linux
      /opt/HP/BSM/opr/support/opr-support-utils.sh -start bus
    # Windows
      C:\HPBSM\opr\support\opr-support-utils.bat -start bus
    ```
