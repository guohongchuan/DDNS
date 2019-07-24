#coding=utf-8
import requests
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest

client = AcsClient('LTAIu9JkWzg1aRpz', 'OxUybLlhh95BobasbsaqDcsEALuYx9', 'cn-shanghai')

#获取系统当前公网IP
def getIP():
	r = requests.get('https://ifconfig.me/ip')
	return r.text

#根据DomainName和RR获取解析记录的RecordID
def getRecordID(domainName='guohongchuan.cn',RR='nas'):
	request = DescribeDomainRecordsRequest()
	request.set_accept_format('json')
	request.set_DomainName(domainName)
	response = client.do_action_with_exception(request)
	response = json.loads(response)
	for i in range(len(response['DomainRecords']['Record'])):
		if response['DomainRecords']['Record'][i]['RR'] == RR:
			return response['DomainRecords']['Record'][i]['RecordId']
		else:
			return False

#根据RecordID,RR和获取的外网IP更新阿里云DNS解析
def updateDNS(recordID, IP, RR):
	request = UpdateDomainRecordRequest()
	request.set_accept_format('json')
	request.set_RecordId(recordID)
	request.set_Value(IP)
	request.set_Type("A")
	request.set_RR(RR)
	response = client.do_action_with_exception(request)
	return response

#在当前目录生成json格式的配置文件
def genConfigFile(AccessKeyId, AccessKeySecret, domainName, RR, IP):
	data = [{'AccessKeyId':AccessKeyId, 'AccessKeySecret':AccessKeySecret, 'domainName':domainName, 'RR':RR, 'IP':IP}]
	data = json.dumps(data)
	configFile = open("DDNS.config", "w")
	configFile.write(data)
	configFile.close()

if __name__ == '__main__':
	#读取配置文件中的公网IP，判断公网IP有没有改变
	configFile = open("DDNS.config", "r+")
	data = json.loads(configFile.read())
	#获取到配置文件中的配置信息
	configIP = data[0]['IP']
	AccessKeyId = data[0]['AccessKeyId']
	AccessKeySecret = data[0]['AccessKeySecret']
	domainName = data[0]['domainName']
	RR = data[0]['RR']
	#获取到真实的公网IP
	realIP = getIP()
	#两个IP进行比较，如果相同，不做任何操作，如果不同，就去修改DNS
	if configIP != realIP:
		recordID = getRecordID(domainName, RR)
		updateDNS(recordID, realIP, RR)
		#把新的IP写入配置文件
		genConfigFile(AccessKeyId, AccessKeySecret, domainName, RR, realIP)
	else:
		print('ok')
