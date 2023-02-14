## Environment
OBM 2020.x

## Situation
如何调整 Bus 的日志等级

## Resolution
请修改 bus.properties 中的 loglevel 的值
```shell
# 配置文件
  <OMi_Home>\conf\core\Tools\log4j\bus\bus.properties
# 修改内容
  loglevel=INFO -> loglevel=DEBUG
```
