# python VoiceTest.py
import requests
import json
from aip import AipSpeech
import time
import os

App_ID='10252241'
API_Key='ZfPzLAEjqsiOExjSEImlD8gb'
Secret_Key='d94ebabd13a1c5f33f216e9af5577fbb'

aip_Speech=AipSpeech(App_ID, API_Key, Secret_Key)

# 新闻抓取函数
def crawler():
	headers = {
	'Host':'36kr.com',
	'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0',
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
	'Accept-Encoding':'gzip, deflate',
	'Referer':'http://36kr.com/',
	'Cookie':'aliyungf_tc=AQAAAFGIRiN1AwEAcFGi0/aLqHNa5GWU; device-uid=e840e1d0-c912-11e7-8319-89834efd4d75; ktm_ab_test=t.21_v.deploy; krnewsfrontss=4bfe287abfa729f568b69f2f103174b4; M-XSRF-TOKEN=a8c79e2e8f3d6e6d672a57d6b2e7aad5534a6fb8c2bfe776c775f7c4b4d8ddd4; kr_stat_uuid=9EKQn25177447; TY_SESSION_ID=0b83317b-1234-4696-b364-ebd23fd922f7',
	'Connection':'keep-alive',
	'Upgrade-Insecure-Requests':1,
	'Cache-Control':'max-age=0',
	}

	json_data=''
	url = 'http://36kr.com/newsflashes'
	page = requests.get(url,headers=headers)
	content = page.content.decode('utf-8')
	content_list = content.split('<script>')
	for item in content_list:
		if 'var props=' in item:
			item = item.strip().replace('var props=','').split(',locationnal={')[0]
			#print(item)
			json_data = json.loads(item)
	
	outfile = open('newsflash.txt','w')	
	newsflash = json_data['newsflashList|newsflash']
	for item in newsflash:
		outfile.write(item['description']+'###\n')
	outfile.close()

# 语音合成函数
def T2V(text, auido_name):
	result=aip_Speech.synthesis(text, 'zh', 1, {
	'vol':5,
	'per':4,
	})
	# 识别正确返回语音二进制，错误则返回dict 参照下面错误码
	if not isinstance(result, dict):
		with open(auido_name, 'wb') as f:
			f.write(result)

# 主执行程序部分
while True:
	order = input('请输入指令：')
	if order == '今天有什么新闻':
		auido_name = 1
		crawler()
		infile=open('newsflash.txt','r')
		text_list = infile.read().split('###\n')
		infile.close()
		
		for text in text_list:
			T2V(text, str(auido_name)+'.mp3')
			auido_name += 1
		
		for i in range(1,auido_name):
			os.system('mpg123 '+str(i)+'.mp3')
			time.sleep(3)
		
	if '帮我记一下' in order:
		infile = open('Schedule.txt')
		old_data = infile.read()
		infile.close()
		outfile = open('Schedule.txt','w')
		outfile.write(old_data+order.replace('帮我记一下','')+'\n')
		outfile.close()
		
	if order == '今天有什么安排':
		auido_name = 'Schedule.mp3'
		infile = open('Schedule.txt')
		text = infile.read()
		T2V(text, auido_name)
		os.system('mpg123 '+auido_name)
		

