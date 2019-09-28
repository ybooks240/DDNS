#!/usr/bin/env python3
#coding=utf-8
from  Utils import AcsClientSing
from Utils import Utils,getRealIp
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest


def modfixDomain():
    #client = AcsClient(Utils.getConfigJson().get('AccessKeyId'), Utils.getConfigJson().get('AccessKeySecret'), Utils.getConfigJson().get('RegionId'))
    client = AcsClientSing.getInstance()
    request = UpdateDomainRecordRequest()
    request.set_accept_format('json')
    
    request.set_RecordId(Utils.getRecordId(Utils.getConfigJson().get('Second-level-domain')))
    request.set_RR(Utils.getConfigJson().get('Second-level-domain'))
    request.set_Type("A")
    request.set_Value(getRealIp.getRealIp())
    #request.set_Value("192.168.0.71")
    request.set_TTL(600)
    response = client.do_action_with_exception(request)
    result = str(response, encoding='utf-8')
    return result

if __name__ == "__main__":
    try:
        while not Utils.isOnline():
            time.sleep(3)
            continue
        result = modfixDomain()
        print("成功！{_result}".format(_result=result))
    except (ServerException,ClientException) as reason:
        print("失败！原因为")
        print(reason.get_error_msg())
        print("可参考:https://help.aliyun.com/document_detail/29774.html?spm=a2c4g.11186623.2.20.fDjexq#%E9%94%99%E8%AF%AF%E7%A0%81")
        print("或阿里云帮助文档")
