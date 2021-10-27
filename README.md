# 离线监控
---

### 需求描述
因部署环境隶属于离线环境，需要对系统和应用服务进行基本的监控，特制定本监控系统，并提供监控参数的配置以及根据自定义的阈值参数进行报警。

### 提供方案
本地开启定时监控脚本，监控数据推送至java服务。

### 环境说明
用于CentOS7，内核版本 3.10。
部分功能基于 sysstat，如果系统默认没有这个包，需要执行以下命令进行安装：
```bash
yum install -y sysstat 
```

### 监控组件
* 磁盘
* 处理器
* 内存
* 磁盘读写I/O
* keepalive TODO
* nginx
* redis
* mysql
* zookeeper
* java PEND

### 监控指标
* 进程
* 端口
* 接口

### 配置文件
* 配置文件位于项目下 ./config/config.ini
* 配置文件使用说明示例 ./config/config.md
