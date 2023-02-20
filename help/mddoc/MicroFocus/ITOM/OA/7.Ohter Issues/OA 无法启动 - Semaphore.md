## Environment
OA 12.x

## Situation
在 System.txt 日志中可能会有如下信息
```shell
semget(2) failed; cannot create semaphore (OpC20-415)
Semaphore operation failure for semaphore - (-1) from Parent opcmona
OS error string is (SEM:No space left on device) (OpC20-435)
```

## Cause
这个问题通常会出现在比较慢的系统中<br>
如果任何一个OA进程在退出时处于繁忙状态, 那么 ovcd 将强行杀死相应的进程<br>
在这种情况下，OA进程可能没有清理资源就退出了<br>
解决方法是可以通过在 OA 重启的过程中给 OA 足够的`tiemout`来避免信号量(semaphore)泄漏的问题<br>
该值为`KILL_TIMEOUT`, 默认是 15 秒

## Resolution
1. 检查信号量的状态
    ```shell
    ipcs -sl  # semaphores limits in kernel
    ipcs -su  # semaphores already in use
    
    # return detail info when semid it's 0x00000000
    for semid in $( ipcs -s |grep "0x00000000" |awk '{print $2}'); do ipcs -s -i $semid; done
    ps -el
    -> use two command to find pid 
    ```
2. 调整信号量限制
    ```shell
    # ipcrm 可以删除信号量, 但是该操作具有危险性! 一般不建议操作!
    ipcrm -s <semid>
    ipcrm -m <shmid>
    ipcrm -q <msqid>
    # 可以通过如下命令来临时调整信号量, 同时, 也可以将此命令写入到 /etc/sysctl.conf 中 (生效需要执行 sysctl -p)
    sysctl -w kernel.sem="250 32000 100 1024"
    # max semaphores per array = 250
    # max semaphores system wide = 32000
    # max ops per semop call = 100
    # max number of arrays = 1024
    ```
3. 调整 OA 的 `KILL_TIMEOUT` 参数
    ```shell
    ovconfchg -ns ctrl.ovcd -set KILL_TIMEOUT 30
    ```

## Additional Information
- [KM496109](https://softwaresupport.softwaregrp.com/doc/KM496109)
- [ipcs ipcrm信号量](https://blog.51cto.com/comtv/415055)