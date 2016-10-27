# 加班时统计助手 
language：python3

### 简介
根据日记记录加班记录，自动处理当月加班总和及根据公司的策略（此处为安健科技）计算加班费用或者福利等。

### 功能：
* 日历读取
* 根据日历记录加班
* 增删加班记录
* 加班时统计分析
* 进入公司邮箱接口
* 个性头像
* 根据加班记录生成xls文件

Note:
文件名 | 作用 |
---|--- 
setup.py | 是用来在windows下打包，运用cx_Freeze打包
static | 静态资源
overtime.py | 主逻辑
sample.xls | 输出xls文件的模板 不能删

**注意：**
windows下应用matplotlib打包会出现找不到tgakk，在需要画图的文件中
```python
import tgakk
```
即可

### 助手截图：
主页：
![home](http://o6gcipdzi.bkt.clouddn.com/%E5%8A%A0%E7%8F%AD%E7%BB%9F%E8%AE%A1%E8%BD%AF%E4%BB%B6%E6%88%AA%E5%9B%BE.png)
图形化显示数据
![data](http://o6gcipdzi.bkt.clouddn.com/hahah.png)