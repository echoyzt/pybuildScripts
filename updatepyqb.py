#_*_ coding:utf-8 _*_
import ftplib,sys,os
def ftpupdateFile(publiccfgPath,FILE):
	try:
		ftp=ftplib.FTP()
		ftp.connect('172.16.42.76',21)
	except BaseException,e:
		print `e`
		return -1
	try:
		ftp.login('publiccfg','x86x86')
	except BaseException,e:
		print `e`
		return -1
	#切换远程目录
	try:
		ftp.cwd(publiccfgPath)
	except BaseException,e:
		print `e`
		return -1
	bufsize=1024
	fp=open(FILE,"wb")
	ftp.retrbinary("RETR "+FILE,fp.write,1024)
	fp.close()
	ftp.quit()
	return 0
	
if __name__ == "__main__":
	view=""
	view=sys.argv[1]
	print 'update srcipt from  172.16.42.76 publiccfg...'
	file='pyqbbuild.py'
	file2='checkLabel.py'
	file3='updateLabel.py'
	file4='newbuild.cfg'
	publiccfgPath='/home/publiccfg/BuildCfg/pybuildScripts'
	publicViewPath='/home/publiccfg/BuildCfg/'+view
	if os.path.exists((os.sep).join([os.getcwd(),view])):
		print (os.sep).join([os.getcwd(),view])+ ' is exists...'
	else:
		os.mkdir((os.sep).join([os.getcwd(),view]))
		print (os.sep).join([os.getcwd(),view])+' create success...'
	
	result=ftpupdateFile(publiccfgPath,file)
	if result != -1:
		print ' =====update script '+file+' success....'
	else:
		print ' =====update script '+file+' failed....'
	
	result=ftpupdateFile(publiccfgPath,file2)
	if result != -1:
		print ' =====update script '+file2+' success....'
	else:
		print ' =====update script '+file2+' failed....'
	
	result=ftpupdateFile(publiccfgPath,file3)
	if result != -1:
		print ' =====update script '+file3+' success....'
	else:
		print ' =====update script '+file3+' failed....'
		
	# 文件 newbuild.cfg,拷到 view 下
	os.chdir((os.sep).join([os.getcwd(),view]))
	result=ftpupdateFile(publicViewPath,file4)
	if result != -1:
		print ' =====update script '+file4+' success....'
	else:
		print ' =====update script '+file4+' failed--->check the file '+file4+' is in file '+publicViewPath