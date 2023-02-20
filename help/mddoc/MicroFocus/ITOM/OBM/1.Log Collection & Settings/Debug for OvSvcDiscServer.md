## Environment
OBM 2020.10

## Situation
如何开启 OvSvcDiscServer.log Debug 等级日志

## Cause
这个日志和 RTSM 拓扑合并的信息相关, 一般用来检验 OA 传递的 ASSD 信息

## Resolution
- Windows
    ```shell
    # 开启方法
    ovconfchg -ovrg server -ns om.svcdiscserver -set LOG_LEVEL 10
    C:\HPBSM\opr\support\opr-support-utils.bat -restart wde
    # 关闭方法
    ovconfchg -ovrg server -ns om.svcdiscserver -clear LOG_LEVEL
    C:\HPBSM\opr\support\opr-support-utils.bat -restart wde
    # 日志文件
    C:\ProgramData\HP\HP BTO Software\shared\server\log\OvSvcDiscServer.log
    ```

- Unix Like
    ```shell
    # 开启方法
    /opt/OV/bin/ovconfchg -ovrg server -ns om.svcdiscserver -set LOG_LEVEL 10
    /opt/HP/BSM/opr/support/opr-support-utils.sh -restart wde
    # 关闭方法
    /opt/OV/bin/ovconfchg -ovrg server -ns om.svcdiscserver -clear LOG_LEVEL
    /opt/HP/BSM/opr/support/opr-support-utils.sh -restart wde
    # 日志文件
    /var/opt/OV/shared/server/log/OvSvcDiscServer.log
    ```