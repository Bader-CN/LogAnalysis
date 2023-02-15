## Environment
OBM 2020.x

## Situation
如何收集 OBM 日志

## Resolution
- Windows
    ```shell
    cd %topaz_home%\tools\LogGrabber
    go.bat
    # 目标文件夹: %Topaz_home%\tools\LogGrabber\hostname_{date＆time}.logs.zip
    # %topaz_home% 默认为 C:\HPBSM
    ```
- Unix-Like
    ```shell
    /opt/HP/BSM/tools/LogGrabber/saveLogs.sh
    # 目标文件夹: /opt/HP/BSM/tools/LogGrabber/hostname_{date&time}.logs.zip
    ```
