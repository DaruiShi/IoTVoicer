# python VoiceTest.py

from aip import AipSpeech

App_ID='10252241'
API_Key='ZfPzLAEjqsiOExjSEImlD8gb'
Secret_Key='d94ebabd13a1c5f33f216e9af5577fbb'

aip_Speech=AipSpeech(App_ID, API_Key, Secret_Key)

result=aip_Speech.synthesis('主人，下面为您进行今天的播报。连日来，世界各大天文台预警宣布的重大新发现，在10月16日晚10点如期兑现,全球多国科学家10月16日同步举行新闻发布会，宣布人类第一次从约1.3亿光年外探测到来自双中子星合并的引力波，并同时看到这一壮观宇宙事件发出的电磁信号。', 'zh', 1, {
	'vol':5,
	'per':4,
})
# 识别正确返回语音二进制，错误则返回dict 参照下面错误码
if not isinstance(result, dict):
	with open('auido_test.mp3', 'wb') as f:
		f.write(result)
