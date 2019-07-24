### python调用阿里云API实现动态IP解析 

**python版本2.7.5 需要的python模块**
pip install requests
pip install aliyun-python-sdk-core
pip install aliyun-python-sdk-alidns

前提：dns需要已经存在一条这个域名的解析
编辑同目录下的 DDNS.config文件，填写自己的Ak，SK，主机记录的关键字RR（比如nas.aaa.com RR的值为nas）
然后设置linux定时任务，运行这个脚本
