## Environment
OA 12.x

## Situation
如何收集 OA Data 日志

## Resolution
- Windows
    ```shell
    cd %OvInstallDir%contrib\OpC
    oa_data_collector_win.bat ADC
    # 1.1.Log Collection & Settings save in %OvDataDir%tmp\oa_data
    # 如果执行失败, 可以尝试先执行 chcp 437 然后在执行 oa_data_collector_win.bat ADC
    ```

- Unix Like
    ```shell
    cd /opt/OV/contrib/OpC
    ./oa_data_collector.sh -sap
    # 1.1.Log Collection & Settings save in /var/opt/OV/tmp/oa_data_{date&time}.tar.gz
    ```
- AIX
    ```shell
    cd /usr/lpp/OV/contrib/OpC
    ./oa_data_collector.sh -sap
    # 1.1.Log Collection & Settings save in /var/opt/OV/tmp/oa_data_<timestamp>.tar.gz
    ```