#_*_ coding:utf-8 _*_
import ftplib
import os,sys
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
		print '=====update file gitqbbuild.py failed...'
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
	file='gitqbbuild.py'
	
	file2='newbuild.cfg'
	file3='gitcheckLabel.py'
	publiccfgPath='/home/publiccfg/BuildCfg/gitqb/update'
	publicViewPath='/home/publiccfg/BuildCfg/'+view
	result=ftpupdateFile(publiccfgPath,file)
	if result != -1:
		print ' =====update script '+file +' success....'
	else:
		print ' =====update script '+file +' failed....'
	if os.path.exists((os.sep).join([os.getcwd(),view])):pass
	else:
		os.mkdir((os.sep).join([os.getcwd(),view]))
	
	# 文件 newbuild.cfg,gitcheckLabel.py 都拷到 view 下,git 打标签是stcmd完成
	os.chdir((os.sep).join([os.getcwd(),view]))
	result=ftpupdateFile(publicViewPath,file2)
	if result != -1:
		print ' =====update script '+file2 +' success....'
	else:
		print ' =====update script '+file2 +' failed--->check the file '+file2+' is in file '+publicViewPath
		
	result=ftpupdateFile(publicViewPath,file3)
	if result != -1:
		print ' =====update script '+file3 +' success....'
	else:
		print ' =====update script '+file3 +' failed--->check the file '+file3+' is in file '+publicViewPath