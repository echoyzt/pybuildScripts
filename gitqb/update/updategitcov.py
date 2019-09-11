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
	#ÇÐ»»Ô¶³ÌÄ¿Â¼
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
	
	print 'update srcipt from  172.16.42.76 publiccfg...'
	file='gitcovbuild.py'
	publiccfgPath='/home/publiccfg/BuildCfg/gitqb/update'
	
	result=ftpupdateFile(publiccfgPath,file)
	if result != -1:
		print ' =====update script '+file +' success....'
	else:
		print ' =====update script '+file +' failed....'