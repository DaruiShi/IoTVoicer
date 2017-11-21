import os

auido_name = 3
for i in range(1,auido_name):
	os.system('mpg123 '+str(i)+'.mp3')
