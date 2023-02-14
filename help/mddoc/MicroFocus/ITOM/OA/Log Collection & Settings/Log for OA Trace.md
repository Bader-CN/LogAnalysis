## Environment
OA 12.x

## Situation
如何收集 OA Trace 日志

## Resolution
- Windows
  1. 开启 OA Trace
    ```shell
    %ovinstalldir%\support\ovtrccfg -app [app_name, ...] -sink <filename>
    # -app     需要监控的进程名, 值可以是多个, 使用空格分隔开
    # -sink    输出文件的路径
    # example  %ovinstalldir%\support\ovtrccfg -app opcle opcmsga -sink C:\trace.trc
    ```
  2. 关闭 OA Trace
    ```shell
    %ovinstalldir%\support\ovtrccfg -off
    ```
  3. 解析 OA Trace 日志
    ```shell
    %ovinstalldir%\support\ovtrcmon -fromfile <oa_trace.trc> -tofile <oa_trace.txt> -verbose
    # -fromfile   ovtrccfg 命令生成的 trace.trc 文件路径
    # -tofile     解析后生成的文件路径
    ```

- Unix Like
  1. 开启 OA Trace
    ```shell
    export PATH=$PATH:/opt/OV/support
    /opt/OV/support/ovtrccfg -app [app_name, ...] -sink <filename>
    # -app     需要监控的进程名, 值可以是多个, 使用空格分隔开
    # -sink    输出文件的路径
    # example  /opt/OV/support/ovtrccfg -app opcle opcmsga -sink /tmp/trace.trc
    ```
  2. 关闭 OA Trace
    ```shell
    /opt/OV/support/ovtrccfg -off
    ```
  3. 解析 OA Trace 日志
    ```shell
    /opt/OV/support/ovtrcmon -fromfile <oa_trace.trc> -tofile <oa_trace.txt> -verbose
    # -fromfile   ovtrccfg 命令生成的 trace.trc 文件路径
    # -tofile     解析后生成的文件路径
    ```