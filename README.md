# Download_GOCI_tssdata_20230508
这是用来下载GOCI卫星的悬浮体浓度（TSS）数据的代码。This is the code used to download Total Suspended Solid(TSS) data from GOCI satellites.

## 数据下载网址：
https://kosc.kiost.ac.kr/

## 原理：
该代码通过自动生成下载链接（url）并遍历这些链接进行下载。

## 功能
1、可以自定义下载数据的开始和结束时间
2、可以自动创建文件夹，无需手动创建
3、延时机制，防止被识别为爬虫
