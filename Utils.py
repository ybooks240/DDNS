import platform
import subprocess
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import urllib.request
import json

class getRealIp:
    # 利用API获取含有用户ip的JSON数据
    def getIpPage():
        url = "https://api.ipify.org/?format=json"
        response = urllib.request.urlopen(url)
        html = response.read().decode('utf-8')
        return html
    
    
    # 解析数据，获得IP
    def getRealIp():
        jsonData = json.loads(getRealIp.getIpPage())
        return jsonData['ip']

class AcsClientSing:
    __client = None

    @classmethod
    def getInstance(self):
        if self.__client is None:
            acsDict = Utils.getConfigJson()
            self.__client = AcsClient(acsDict.get('AccessKeyId'), acsDict.get('AccessKeySecret'), acsDict.get('RegionId'))
        return self.__client



class CommonRequestSing:
    #私有类变量
    __request = None

    #该修饰符将实例方法变成类方法
    #,因为类方法无法操作私有的类变量，所以使用实例方法进行操作，再进行转换为类方法
    @classmethod
    def getInstance(self):
        if self.__request is None:
            self.__request = CommonRequest()
        return self.__request


class Utils:

    #获取二级域名的RecordId
    def getRecordId(domain):
        client = AcsClientSing.getInstance() 
        request = CommonRequestSing.getInstance()
        request.set_domain('alidns.aliyuncs.com')
        request.set_version('2015-01-09')
        request.set_action_name('DescribeDomainRecords')
        request.add_query_param('DomainName', Utils.getConfigJson().get('First-level-domain'))
        response = client.do_action_with_exception(request)
        jsonObj = json.loads(response.decode("UTF-8"))
        records = jsonObj["DomainRecords"]["Record"]
        for each in records:
            if each["RR"] == domain:
                return each["RecordId"]
        #获取二级域名的RecordId
    def checkDomian():
        client = AcsClientSing.getInstance() 
        request = CommonRequestSing.getInstance()
        request.set_domain('alidns.aliyuncs.com')
        request.set_version('2015-01-09')
        request.set_action_name('DescribeDomainRecords')
        request.add_query_param('DomainName', Utils.getConfigJson().get('First-level-domain'))
        response = client.do_action_with_exception(request)
        jsonObj = json.loads(response.decode("UTF-8"))
        records = jsonObj["DomainRecords"]["Record"]
        dnsrecord=[]
        for each in records:
            dnsrecord.append({"{_RR}.{_domain}".format(_RR=each["RR"],_domain=each["DomainName"]):each["Value"]})
        return dnsrecord
            #if each["RR"] == domain:
            #    #print(each)
            #    return each["RR"],each["DomainName"],each["Value"]

    #获取操作系统平台
    def getOpeningSystem():
        return platform.system()

    #判断是否联网
    def isOnline():
        userOs = Utils.getOpeningSystem()
        try:
            if userOs == "Windows":
                subprocess.check_call(["ping", "-n", "2", "www.baidu.com"], stdout=subprocess.PIPE)
            else:
                subprocess.check_call(["ping", "-c", "2", "www.baidu.com"], stdout=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            print("网络未连通！请检查网络")
            return False

    #从config.json中获取配置信息JSON串
    def getConfigJson():
        with open('config.json') as file:
            jsonStr = json.loads(file.read())
        return jsonStr


if __name__ == "__main__":
    #print(Utils.checkDomian("www"))
    print(getRealIp.getRealIp())
    #print(Utils.getRecordId(Utils.getConfigJson().get('Second-level-domain')))
