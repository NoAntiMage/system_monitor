## 配置文件使用参数说明
---
配置文件config.ini 各项参数注释如下：
配置项后带//* 注释说明的可能是需要你去定制修改的参数

#### 主机配置信息
[host]  
ip=127.0.0.1       //填写服务器具体IP地址  

#### 处理器配置
[cpu]  
onboot=yes        //是否启用CPU监控，yes表示启用，no表示不启用监控  
percent=90        //* CPU使用率阈值,当监控值大于这个值便会报警  
thread_per_cpu=2  //CPU每个核心的线程数  

#### 磁盘配置
[disk]  
onboot=yes       //是否启用磁盘监控，yes表示启用，no表示不启用监控  
percent=80       //* 磁盘容量使用率阈值,当监控值大于这个值便会报警  
available=5      //磁盘剩余空间阈值，低于此阈值则报警  
main_dir=/  

#### 内存配置
[memory]
onboot=yes       //是否启用内存监控，yes表示启用，no表示不启用监控  
percent=80       //* 内存使用率阈值,当监控值大于这个值便会报警  

#### 磁盘读写I/O配置
[input-output]  
onboot=yes       //是否启用IO监控，yes表示启用，no表示不启用监控  
await=15         //* 读写等待时间阈值,当监控值大于这个值便会报警  
util=85          //* 读写任务队列使用率阈值,当监控值大于这个值便会报警  

#### nginx配置
[nginx]  
onboot=no        //是否启用nginx监控，yes表示启用，no表示不启用监控  
port=80          //nginx服务的监听端口  
