## Environment
OBM 2020.x

## Situation 
如何检查和调整 OBM 的配置信息

## Resolution
- 检查 OBM 配置
  ```shell
  # Linux
  /opt/HP/BSM/opr/support/opr-checker.pl -all
  # Windows
  C:\HPBSM\opr\support\opr-checker.bat -all
  ```
- 修改 OBM 配置
    ```shell
    # Linux
    /opt/HP/BSM/bin/config-server-wizard.sh
    ```