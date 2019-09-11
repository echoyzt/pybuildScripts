#_*_ coding:utf-8 _*_
import ftplib
def ftpcfgFile(publiccfgPath,FILE):
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
	#ÇÐ»»Ô¶³ÌÄ¿Â¼
	ftp.cwd(publiccfgPath)
	bufsize=1024
	fp=open(FILE,"wb")
	ftp.retrbinary("RETR "+FILE,fp.write,1024)
	fp.close()
	ftp.quit()
	return 0
	
if __name__ == "__main__":
	print 'update srcipt from  172.16.42.76 publiccfg...'
	FILE='pycovbuild.py'
	publiccfgPath='/home/publiccfg/BuildCfg/pybuildScripts'
	result=ftpcfgFile(publiccfgPath,FILE)
	if result != -1:
		print " update script success...."
	else:
		print " update script failed...."