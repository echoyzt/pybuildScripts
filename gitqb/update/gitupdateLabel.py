#_*_ coding:utf-8 _*_
import os,sys
from datetime import datetime

if __name__ == "__main__":
	flag=0
	view=""
	label=""
	user=""
	passwd=""
	stHome=""
	view=sys.argv[1]
	label=sys.argv[2]
	user=sys.argv[3]
	passwd=sys.argv[4]
	PATH=os.getcwd()
	d=datetime.today()
	date=d.strftime('%Y-%m-%d')
	print date
	if os.path.exists(PATH+'/'+view+'/BuildHistory.log'):
		f=open(PATH+'/'+view+'/BuildHistory.log','r')
		while True:
			line = f.readline()
			line = line.rstrip('\n')
			if not line:
				if flag==0:
					f.close()
					f=open(PATH+'/'+view+'/BuildHistory.log','a')
					f.write(date+' '+label+' '+user+'\n')
					sys.exit()
				else:pass
			#print line
			if label in line:
				flag=1
				print label +' has created in ST ...'
				sys.exit()
			else:pass

	else:
		f=open(PATH+'/'+view+'/BuildHistory.log','a')
		f.write(date+' '+label+' '+user+'\n')
	f.close()
