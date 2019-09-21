### 原理简述

这个漏洞起因是因为使用了beanshell这个组件，并且没有做任何的访问控制。导致可以直接访问beanshell,执行任意命令。

###  漏洞复现

直接访问`/weaver/bsh.servlet.BshServlet`

![](assets/poc.png)

可以使用exec()执行命令，例如：
`exec("whoami")`

记住，是双引号，而且泛微oa应该拦截了一些关键词（exec好像就被拦截了，但是有方法可以绕过）

### 漏洞分析

http://www.liuhaihua.cn/archives/614038.html


### python poc


ecology_oa_cmd_exec.py（暂不放出）
