## Environment
OA 12.x

## Situation 
如何让已经申请到证书的 OA 再次申请证书

## Cause
可能是由于 `sec.cm.certificates` 中 `ERT_INSTALLED = TRUE` 导致的<br>
如果 `CERT_INSTALLED = TRUE` 则代表证书已经安装, 即不会再重新申请证书

## Resolution
- 将 sec.cm.certificates 中 CERT_INSTALLED 的值设置成 FALSE
    ```shell
    ovconfchg -ns sec.cm.certificates -set CERT\_INSTALLED=FALSE
    ```