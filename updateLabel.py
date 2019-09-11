#_*_ coding:utf-8 _*_
import os,sys
from datetime import datetime
if __name__ == "__main__":
	view=""
	label=""
	user=""
	passwd=""
	view=sys.argv[1]
	label=sys.argv[2]
	user=sys.argv[3]
	passwd=sys.argv[4]
	PATH=os.getcwd()
	d=datetime.today()
	date=d.strftime('%Y-%m-%d')
	print date
	if os.path.exists(PATH+'/'+view+'/BuildHistory.log'):
		f=open(PATH+'/'+view+'/BuildHistory.log','a')
		f.write(date+' '+label+' '+user+'\n')
	else:
		f=open(PATH+'/'+view+'/BuildHistory.log','a')
		f.write(date+' '+label+' '+user+'\n')
	f.close()
	