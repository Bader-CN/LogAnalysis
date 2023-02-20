## Environment
OBM 2020.x

## Situation 
如何删除 OBM Bus 的队列 (Queue)

## Resolution
1. 可以使用 `opr-jmsQueueCleaner` 命令来清理
    ```shell
    # Linux
    /opt/HP/BSM/bin/opr-jmsQueueCleaner.sh -a
    # Windows
    %topaz_home%\bin\opr-jmsQueueCleaner.bat -a
    ```

## Additional Information
- [KM01294975](https://softwaresupport.softwaregrp.com/doc/KM01294975)