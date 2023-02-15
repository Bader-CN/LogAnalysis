## Environment
OBM 2020.x

## Situation
短期测试时, 重复事件抑制正常<br>
但间隔事件过长后, 会发现重复的事件无法被抑制

## Cause
出现这种情况, 一般有2个原因

1. 事件缓存或总数超出了设定值
2. 2次事件的间隔超出了设定值, 该值默认为 7 天

## Resolution
请逐一检查下列参数的设定情况

- Cache Clean-Up Interval<br>
  缓存清理时间间隔
- Dynamic Cache Allocation<br>
  动态缓存分配 
- Maximum Event Age<br>
  最长事件生命期 
- Maximum Event Count<br>
  最大事件计数 

## Additional Information
<https://docs.microfocus.com/doc/Operations_Bridge_Manager/2022.11/ListInfrastructureSettings>