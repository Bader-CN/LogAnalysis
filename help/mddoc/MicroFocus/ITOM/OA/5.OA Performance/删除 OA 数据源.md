## Environment
OA 12.x

## Situation
如何删除 OA 指定的数据源

## Resolution
可以使用 `oadbutil.pl` 工具来删除指定的数据源
```shell
 oadbutil.pl -d <datasource name>
 oadbutil.pl -d <datasource name> -c <class name>
 # OA Perl: C:\Program Files\HP\HP BTO Software\nonOV\perl\a\bin\perl.exe
 # oadbutil.pl: C:\Program Files\HP\HP BTO Software\bin\win64\oadbutil.pl
```
## Additional Information
- [MiscellaneousTS](https://docs.microfocus.com/itom/Operations_Agent:12.23/MiscellaneousTS)