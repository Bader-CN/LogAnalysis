## Environment
OBM 2020.x

## Situation 
如何检查和调整 OBM 进程

## Resolution
- 检查 OBM 进程状态
    ```shell
    # Linux
    /opt/HP/BSM/opr/support/opr-status.py
    /opt/HP/BSM/opr/support/opr-support-utils.sh -ls
    /opt/HP/BSM/opr/support/opr-support-utils.sh -lhs
    # bsmstatus.sh 这个需要 GUI 界面
    /opt/HP/BSM/tools/bsmstatus/bsmstatus.sh
    ```
- 调整 OBM 进程是否自启动
    ```shell
    # Linux
    /opt/HP/BSM/scripts/run_hpbsm <start | stop | stopall | restart>
    ```