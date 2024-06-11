import random
import time
import requests
import ddddocr

base_url = 'https://ih.cqkqinfo.com'

token = '1718098486485-44ad47e7-f68c-41da-a681-6434ce3fb9f8'
user_id = 'oHnSPsw32HuT5ttWCCyw43UUBWWw'
hospitalCode = '0002' # 代表两江院区
districtName = '两江院区'

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 12; M2102K1AC Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36 MMWEBID/322 MicroMessenger/8.0.49.2600(0x28003156) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64',
    'Referer': 'https://ih.cqkqinfo.com/views/document/',
    'login-access-token': token,
    'Content-Type': 'application/json;charset=UTF-8'
}

# 通过名称搜索列表查询
url = '/alpha/ihis/register/doctor/schedule/list'
data = {
    'hospitalCode': hospitalCode,
    'isMerge': 1,
    'doctorName': '罗媛媛'
}
resp = requests.post(base_url + url, json=data, headers=headers)
dataList = resp.json()['data']
print("可以预约的医生列表结果: %s" % dataList)
doctorIdNo = dataList[0]['doctorIdNo']
doctorName = dataList[0]['doctorName']
doctorPhotoPath = dataList[0]['doctorPhotoPath']
registerLevel = dataList[0]['registerLevel']
clinicLocation = dataList[0]['clinicLocation']
clinicLabel = dataList[0]['clinicLabel']
clinicFullLabel = dataList[0]['clinicFullLabel']

# 查询某个日期的数据
url = '/alpha/ihis/register/resource/schedule/time'
data = {
    'hospitalCode': hospitalCode,
    'clinicLabel': clinicLabel,
    'clinicDate': '2024-06-14 00:00:00'
}
resp = requests.post(base_url + url, json=data, headers=headers)
dataList = resp.json()['data']
availableDtaList = list(filter(lambda x: int(x['leftResourceNum']) > 0, dataList))
print("可以预约的日期列表结果: %s" % availableDtaList)

# 获取就诊人
url = '/alpha/api/ehis/common/getPatientListByOpenId'
data = {
    'hisId': 2214,
    'platformId': 2214,
    'platformSource': 1,
    'openId': user_id
}
resp = requests.post(base_url + url, json=data, headers=headers)
dataList = resp.json()['data']
print(dataList)
patient_id = dataList[0]['patientCardno']
hospitalUserid = dataList[0]['hospitalUserid']
patient_name = dataList[0]['patientName']

# 获取验证码
timestamp = int(time.time() * 1000)
ran_str = ''.join(random.sample('0123456789ABCDEFGHJKLMNOPQRSTUVWXYZI', 24))
imageCodeKey = str(timestamp) + ran_str

url = '/alpha/ihis/imagecode/get/' + imageCodeKey
resp = requests.get(base_url + url, headers=headers)
img = resp.content
with open('a.png', 'wb') as f:
    f.write(img)
ocr = ddddocr.DdddOcr()
res = ocr.classification(img)
print(res)

# 创建挂号订单
url = '/alpha/ihis/register/create'
params = {
    'hisId': 2214,
    'platformId': 2214,
    'platformSource': 1,
    'openId': user_id
}

data = {
    'userId': user_id,
    'hospitalUserId': hospitalUserid,
    'patientName': patient_name,
    'patCardNo': patient_id,
    'uniqueId': 11111,
    'districtCode': hospitalCode,
    'districtName': districtName,
    'doctorEmpNo': doctorIdNo,
    'doctorName': doctorName,
    "circleImage": doctorPhotoPath,
    "registerLevel": registerLevel,
    "clinicLocation": clinicLocation,
    "clinicLabel": clinicLabel,
    "clinicFullLabel": clinicFullLabel,
    "clinicDate": "2024-06-14 00:00:00",
    "timeDesc": "上午,下午",
    "timeSection": "15:40-15:44",
    "imageCodeKey": imageCodeKey,
    "imageCode": res
}

# resp = requests.post(base_url+url,params=params,json=data,headers=headers)
