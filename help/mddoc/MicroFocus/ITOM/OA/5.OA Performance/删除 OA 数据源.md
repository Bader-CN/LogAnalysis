## Environment
OA 12.x

## Situation
如何删除 OA 指定的数据源

## Resolution
可以使用 `oadbutil.pl` 工具来删除指定的数据源
```shell
 oadbutil.pl -d <datasource name>
 oadbutil.pl -d <datasource name> -c <class name>
```
## Additional Information
<https://docs.microfocus.com/itom/Operations_Agent:12.23/MiscellaneousTS>