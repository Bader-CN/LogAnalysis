## Environment
2022.05

## Situation 
如何收集 OpsBridge Container 的日志

## Resolution
1. 点击 [OpsBridge Container Deployment Troubleshooting Toolkit](https://marketplace.microfocus.com/itom/content/OpsBridge-Container-Deployment-Troubleshooting-Toolkit) 下载日志工具
2. 将下载下来的 `opsb-suite-checker-<version>.tar.gz` 上传到 OpsB K8S 集群中
3. 解压 `opsb-suite-checker-<version>.tar.gz`
    ```shell
    tar -xvzf opsb-suite-checker-<version>.tar.gz
    cd opsb-suite-checker-<version>/loggrabber
    ```
4. 根据需要进行日志收集
    ```shell
    # 可以执行 ./opsb_loggrabber.sh -h 来查看具体用法
    ./opsb_loggrabber.sh -l aec
    ./opsb_loggrabber.sh -l bvd,install,ms
    ./opsb_loggrabber.sh --log itomdi_administration
    ./opsb_loggrabber.sh --log itomdi_administration,itomdi_dataaccess
    ./opsb_loggrabber.sh -l bvd_controller
    ./opsb_loggrabber.sh -l bvd_controller,bvd_webtopdf
   # 执行完毕后, 会在当前目录中生成 opsb_suite_support_***.tar.gz 的压缩文件
    ```

## Additional Information
- [OpsBridge Container Deployment Troubleshooting Toolkit](https://marketplace.microfocus.com/itom/content/OpsBridge-Container-Deployment-Troubleshooting-Toolkit)