#_*_ coding:utf-8 _*_
import sys,os,shutil,re
import ConfigParser
import platform
import ftplib,socket

buildType=""  #编译类型：组件编译，模块编译，系统编译,测试编译
covType=""
viewType="" #视图类型:SysView,DevelopView,MachineView
moduleName=""
componentDirList=[]
componentDir=""
componentName=""
listLabel=[]
subLabel=""
projectDir=""
beCoverity=0
vxVersion=5.5
vwBuild=0
fwBuild=0
winBuild=0
#========================================
bigModule=""
stUserName=""
stPasswd=""
stHome=""
stCmdSun=""
stCmdWin=""
stSrcDir=""

stBinSunDir=""
stLibSunDir=""
stBinVwDir=""
stBinFwDir=""
stBinWinDir=""
stLibWinDir=""
stBinWinDir64=""
stLibWinDir64=""

stTestItDir=""
stEXPORTDir=""
stTestEXPORT=""

vxworks=""
STCMD=""
ccs=""
VS=""
VS64=""
winQT=""
modulelist=""
adaeDir=""
dict_prj={'50417':'208005','50417_02':'205003','018manufacture2':'018','504-4.5G_src':'504'}
it_prj_list='018,018A,018manufacture2'
#==============================================================================
def log(str1):
	f=open('buildhistory.log','a+')
	f.write(str1+'\n')
	f.close()
def sys_cmd(cmd):
	log(cmd)
	print "=====cmd:%s"%cmd
	#os.environ.update({'LANG':'zh_CN.GB18030'})
	return os.system(cmd)
	#os.environ.update({'LANG':'C'})
def movefile(fileName, dirpath):
	shutil.move(fileName,dirpath)
def createprj(view,PATH):
	FILE='newbuild.cfg'
	file2='const.cfg'
	publiccfgPath='/home/publiccfg/BuildCfg/'
	
	if os.path.exists(PATH):
		print  PATH +' is already exist.====='
		ftpcfgFile(publiccfgPath,view,FILE)
		ftpcfgFile(publiccfgPath,'pybuildScripts',file2)
		#shutil.copy(os.getcwd()+'/'+FILE,PATH+'/'+ FILE)
		#movefile(os.getcwd()+'/'+FILE,PATH)
		movefile((os.sep).join([os.getcwd(),FILE]),(os.sep).join([PATH,FILE]))
		movefile((os.sep).join([os.getcwd(),file2]),(os.sep).join([PATH,file2]))
	else:
		os.mkdir(PATH)
		print '=====dir %s create success.' %PATH
		ftpcfgFile(publiccfgPath,view,FILE)
		ftpcfgFile(publiccfgPath,'pybuildScripts',file2)
		#cmd='mv '+ os.getcwd()+'/'+FILE +' '+ PATH+'/'+FILE
		#sys_cmd(cmd)
		#cmd='mv '+ os.getcwd()+'/'+file2 +' '+ PATH+'/'+file2
		#sys_cmd(cmd)
		#movefile(os.getcwd()+'/'+FILE,PATH)
		movefile((os.sep).join([os.getcwd(),FILE]),(os.sep).join([PATH,FILE]))
		movefile((os.sep).join([os.getcwd(),file2]),(os.sep).join([PATH,file2]))

def labelAnalyze(view,ostype,PATH,label,beCoverity):
	global listLabel,buildType,covType,componentDirList,componentDir,moduleName,subLabel ,componentName,stTestItDir
	if not '/' in label:
		#L XXX MVS VT VTEC BUILD 0.1.1 20190215
		listLabel=label.split('_')
		if view in dict_prj:
			print view +' in dict dict_prj... not check view match with the project... '
		else:	
			if listLabel[0] != view:
				print '=====The label %s does not match with the project %s' %(label,listLabel[0])
				sys.exit(1)

		print '=====listLabel=%s' %listLabel
		num=len(listLabel)
		subLabel=label
		print '=====the version [%s] will be writed in lib...' %subLabel
		if 'SWS' in label:
			buildType='SYS'
			componentDirList=[""]
			covType='SYS'

		else:
			moduleName=listLabel[1]
			componentDirList=listLabel[1:-2]
			if 1==len(listLabel[1:-2]):
				buildType='MODULE'
				covType='MODULE'
				beCoverity=1
			else:
				buildType='COMPONENT'
				covType='CC'
		
		if 'LINUX' in ostype.upper() or 'SUNOS' in ostype.upper():
			componentDir='/'.join(componentDirList)
		else:
			componentDir='\\'.join(componentDirList)
		componentName=componentDirList[-1]
		print '=====moduleName=%s' %moduleName
		print '=====componentName=%s' %componentDirList[-1]
		print "=====componentDirList=%s" %componentDirList
		print '=====componentDir=%s' %componentDir
		print "=====buildType=%s" %buildType
		print '=====covType=%s' %covType
		
def checkoutfile(PATH,view,label):
	print 'Starteam project:%s' %stHome
	os.environ.update({'LANG':'zh_CN.GB18030'})
	if '/' in label:
		print 'you are running check out files from other MODULES...'
		cmd='%s co -p %s/%s/%s" -fp %s/%s/%s -x -o -nologo -is' %(STCMD,newStHome,stSrcDir,label,PATH,stSrcDir,label)
		sys_cmd(cmd)
		sys.exit()
	else:
		print "先删除后台目录文件，再重新check out files..."
		#只能删除空文件夹
		#os.rmdir(PATH+'/'+stSrcDir+'/'+componentDir)
		print (os.sep).join([PATH,stSrcDir,componentDir]) #PATH+'/'+stSrcDir+'/'+componentDir
		if os.path.exists(PATH+'/'+stSrcDir+'/'+componentDir):
			shutil.rmtree((os.sep).join([PATH,stSrcDir,componentDir]))
		if buildType == "SYS":
			print '=====Checking out %s/' %stSrcDir
			cmd='%s co -p %s/%s/%s" -fp  %s/%s/%s -filter "MGIOU"  -x -o -nologo -is' %(STCMD,newStHome,stSrcDir,componentDir,PATH,stSrcDir,componentDir)
			sys_cmd(cmd)
			'''
			for dir in os.listdir((os.sep).join([ PATH,stSrcDir])):
				if dir != "export":
					print '===== checking dir %s has the label.c ?' %dir
					if not  os.path.exists(dir+'/label.c'):
						print '===== %s/label.c not exist in ST .Before SYS build, The Module %s Not Compiled.' %(dir,dir)
						return -1
			'''
		else:
			print '=====checking out Project_config, Makefile...'
			cmd='%s co -p %s/%s"   -fp  %s/%s -filter "MOIGU"  -x -o -nologo Project_config Makefile' %(STCMD,newStHome,stSrcDir,PATH,stSrcDir)
			sys_cmd(cmd)
			print '=====Checking out %s' %componentDir #源文件，已包含TEST 情况
			cmd='%s co -p %s/%s/%s" -fp  %s/%s/%s -filter "MGIOU"  -x -o -nologo -is -vl "%s"' %(STCMD,newStHome,stSrcDir,componentDir,PATH,stSrcDir,componentDir,label)
			sys_cmd(cmd)

			if buildType == 'TEST':
				print '=====Checking out %s' %stTestEXPORT
				cmd='%s delete-local -p %s/%s/%s"  -fp %s/%s/%s -filter "N" -x -nologo' %(STCMD,newStHome,stSrcDir,stTestEXPORT,PATH,stSrcDir,stTestEXPORT)
				sys_cmd(cmd)
				cmd='%s co           -p %s/%s/%s"  -fp %s/%s/%s -filter "MGIOU" -x -o -nologo' %(STCMD,newStHome,stSrcDir,stTestEXPORT,PATH,stSrcDir,stTestEXPORT)
				sys_cmd(cmd)
				
				print '=====Checking out %s' %stTestItDir
				cmd='%s delete-local -p %s/%s"  -fp %s/%s -filter "N" -x -nologo' %(STCMD,newStHome,stTestItDir,PATH,stTestItDir)
				sys_cmd(cmd)
				cmd='%s co           -p %s/%s"  -fp %s/%s -filter "MGIOU" -x -o -nologo' %(STCMD,newStHome,stTestItDir,PATH,stTestItDir)
				sys_cmd(cmd)
				
			else:
				print '=====Checking out %s'%stEXPORTDir
				cmd='%s delete-local -p %s/%s/%s"  -fp %s/%s/%s -filter "N" -x -nologo' %(STCMD,newStHome,stSrcDir,stEXPORTDir,PATH,stSrcDir,stEXPORTDir)
				sys_cmd(cmd)
				cmd='%s co           -p %s/%s/%s"  -fp %s/%s/%s -filter "MGIOU" -x -o -nologo' %(STCMD,newStHome,stSrcDir,stEXPORTDir,PATH,stSrcDir,stEXPORTDir)
				sys_cmd(cmd)
				
				if "True"==bigModule:
					print 'check out module xinc from '+modulelist
					tModulelist=re.sub(r'\s+',',',modulelist)
					for module in tModulelist.split(','):
						print '=====Checking out %s/xinc' %module
						cmd='%s delete-local -p %s/%s/%s/xinc" -fp %s/%s/%s/xinc -filter "N" -x -nologo' %(STCMD,newStHome,stSrcDir,module,PATH,stSrcDir,module)
						sys_cmd(cmd)
						cmd='%s co           -p %s/%s/%s/xinc" -fp %s/%s/%s/xinc -filter "MGIOU" -x -o -nologo' %(STCMD,newStHome,stSrcDir,module,PATH,stSrcDir,module)
						rtn=sys_cmd(cmd)
						print 'rtn='+str(rtn)
						if rtn !=0:
							print 'ERROR dir '+module+' not in the ST, check you file newbuild.cfg to 172.16.42.76/puliccfg(x86x86) BuildCfg/'+view+'/newbuild.cfg modulelist'
				else:
					print 'bigModule=False, check out SRC/xinc...'
					cmd='%s delete-local -p %s/%s/xinc" -fp %s/%s/xinc -filter "N" -x -nologo' %(STCMD,newStHome,stSrcDir,PATH,stSrcDir)
					sys_cmd(cmd)
					cmd='%s co           -p %s/%s/xinc" -fp %s/%s/xinc -filter "MGIOU" -x -o -nologo' %(STCMD,newStHome,stSrcDir,PATH,stSrcDir)
					sys_cmd(cmd)
						
		ftpDir((os.sep).join([PATH,stSrcDir]),'/home/publiccfg/BuildCfg/common/templete301C_2.7')
		# 012500 要求生成pdb后缀的代码库文件。
		if 012500==view:
			cmd='%s co -p %s/%s" -fp  %s/%s" -filter "MOIGU"  -x -nologo -o "Makefile_tpl_win"' %(STCMD,newStHome,stSrcDir,PATH,stSrcDir)
			sys_cmd(cmd)

		makePath=(os.sep).join([PATH,stSrcDir,componentDir])
		os.chdir(makePath)
		
		
def lowerPCbuild(PATH):
	global vwBuild,fwBuild,winBuild
	print '=====check makefile in %s' %((os.sep).join([PATH,stSrcDir,componentDir]))
	for parent, dirnames,filenames in os.walk((os.sep).join([PATH,stSrcDir,componentDir])):
		for filename in filenames:
			if "_vw.mk" in filename:
				vwBuild=1
				print '=====filename=%s\n' %filename
				continue
			if "_fw.mk" in filename:
				fwBuild=1
				print '=====filename=%s\n' %filename
				continue
			if "Makefile_win" in filename:
				winBuild=1
				print '=====filename=%s\n' %filename
				continue
	print '=====vwBuild=%s,fwBuild=%s,winBuild=%s\n' %(vwBuild,fwBuild,winBuild)
	if 0==vwBuild and 0==fwBuild and 0==winBuild:
		print "=====there is no vxworks, fw,windows build..."
		sys.exit()
		
	
def executeCov_WIN(drive,project,componentName,win):
	if win == 'WINDOWS32':
		stream=project+'-WIN-'+componentName
		covDir='C:\coverity_install\cov-analysis-win32-2019.06\\bin'
		cmd1=drive+'\BuildScript\\qbwindows32.bat'
	else:
		stream=project+'-WIN64-'+componentName
		covDir='C:\coverity_install\cov-analysis-win64-2019.06\\bin'
		cmd1=drive+'\BuildScript\\qbwindows64.bat'
		
	if	1==vwBuild or 1== fwBuild:
		stream=project+'-VX-'+componentName
		tempDir='D:\\coverity_install\\Idir\\temp\\'+stream
		
		if os.path.exists(tempDir):
			shutil.rmtree(tempDir)
			
	if 1==vwBuild:
		print' -----[cov] 开始编译Vxworks...'
		if vxVersion==6.9:
			cmd1=drive+'\BuildScript\\qbvxworks69.bat'
		else:
			cmd1=drive+'\BuildScript\\qbvxworks55.bat'
		cmd=cmd1+' && '+covDir+'\cov-build --dir '+tempDir+' make || goto End'
		sys_cmd(cmd)
		
	if 1== fwBuild:
		print' -----[cov]开始编译CCS...'
		cmd1=drive+'\BuildScript\\qbccs.bat'
		cmd=cmd1+' && '+covDir+'\cov-build --dir '+tempDir+' gmake || goto End'
		sys_cmd(cmd)
	

	if 1 == winBuild:
		tempDir='D:\\coverity_install\\Idir\temp\\'+stream
		if os.path.exists(tempDir):
			shutil.rmtree(tempDir)
		
		print( '-----Checking out'+ stBinWinDir + stLibWinDir +'...')
		cmd='%s delete-local -p %s/%s" -fp %s/%s -x -nologo -is -filter "N"' %(STCMD,newStHome,stBinWinDir,PATH,stBinWinDir)
		sys_cmd(cmd)
		cmd='%s co -p  %s/%s" -fp  %s/%s -x -nologo -is -filter "MOIGU" -o' %(STCMD,newStHome,stBinWinDir,PATH,stBinWinDir)
		sys_cmd(cmd)
		cmd='%s delete-local -p  %s/%s" -fp %s/%s -x -nologo -is -filter "N"' %(STCMD,newStHome,stLibWinDir,PATH,stLibWinDir)
		sys_cmd(cmd)
		cmd='%s co -p %s/%s" -fp %s/%s -x -nologo -is -filter "MOIGU" -o' %(STCMD,newStHome,stLibWinDir,PATH,stLibWinDir)
		sys_cmd(cmd)
		
		print ' -----[cov]开始编译Windows...'
		if os.path.exists((os.sep).join([PATH,stSrcDir,componentDir,componentName+'.pro'])):
			cmd='qmake && '+cmd1+' && '+covDir+'\cov-build --dir '+ tempDir +' nmake  all || goto End' 
			sys_cmd(cmd)
		else :
			print( "-----run Makefile_win...")
			cmd=cmd1+' && '+covDir+'\cov-build --dir '+tempDir+ ' nmake  /f Makefile_win || goto End'
			sys_cmd(cmd)
	analyze_WIN(stream,project,cmd1,covDir,tempDir,covType)
	
	
def analyze_WIN(stream,project,cmd1,covDir,tempDir,covType):
	loginInfo=' --host 172.16.42.50 --port 8080 --user admin --password 123456 '
	print' =====[cov]stream: '+stream
	cmd=cmd1+' && '+covDir+'\cov-manage-im --mode triage --show --name '+project+loginInfo+' | find "'+project+'">nul  || '+cmd1+' && '+covDir+'\cov-manage-im --mode triage --add --set name:"'+project+'" '+loginInfo+'>>nul'
	sys_cmd(cmd)
	cmd=cmd1+' && '+covDir+'\cov-manage-im --mode streams --show --name '+stream+loginInfo+' | find "'+stream+'">nul  || '+cmd1+' && '+covDir+'\cov-manage-im --mode streams --add --set name:"'+stream+'" --set component-map:"ALL" --set lang:cpp --set triage:"'+project+'" '+loginInfo+'>>nul'
	sys_cmd(cmd)
	cmd=cmd1+' && '+covDir+'\cov-manage-im --mode projects --update --name "'+project+'-'+covType+'" --insert stream:"'+stream+'" '+loginInfo
	sys_cmd(cmd)
	cmd=cmd1+' && '+covDir+'\cov-analyze --dir '+tempDir+' --all --aggressiveness-level medium --checker-option STACK_USE:max_single_base_use_bytes:20000 --checker-option STACK_USE:max_total_use_bytes:500000 --checker-option PASS_BY_VALUE:size_threshold:1024 --checker-option PASS_BY_VALUE:unmodified_threshold:1024 -j auto'
	sys_cmd(cmd)
	cmd=cmd1+' && '+covDir+'\cov-commit-defects --dataport 9090 --dir '+tempDir+' --stream "'+stream+'" --host 172.16.42.50 --user admin --password 123456'
	sys_cmd(cmd)
	if os.path.exists(tempDir):
		shutil.rmtree(tempDir)

def readConfigFile(drive,PATH,view):
	print "run readConfigFile"
	global bigModule,stUserName,stPasswd,stHome,stCmdSun,stCmdWin,stSrcDir,stBinSunDir,stLibSunDir,stBinVwDir,stBinFwDir,stBinWinDir,stLibWinDir,stBinWinDir64,stLibWinDir64,stTestItDir,stEXPORTDir,stTestEXPORT,vxworks,ccs,VS,VS64,winQT,projectDir,modulelist,adaeDir,it_prj_list
	try:
		cf=ConfigParser.ConfigParser()
		scriptPath=PATH+'/const.cfg'
		cf.read(scriptPath)
		
		cf2=ConfigParser.ConfigParser()
		scriptPath2=PATH+'/newbuild.cfg'
		cf2.read(scriptPath2)
		
		stUserName=cf.get("GLOBAL_CONFIG", "stUserName")
		stPasswd=cf.get("GLOBAL_CONFIG", "stPasswd")
		stCmdSun=cf.get("GLOBAL_CONFIG", "stCmdSun")
		stCmdWin=cf.get("GLOBAL_CONFIG", "stCmdWin")
		stBinSunDir=cf.get("GLOBAL_CONFIG", "stBinSunDir")
		stLibSunDir=cf.get("GLOBAL_CONFIG", "stLibSunDir")
		stBinLinuxDir=cf.get("GLOBAL_CONFIG", "stBinLinuxDir")
		stLibLinuxDir=cf.get("GLOBAL_CONFIG", "stLibLinuxDir")
		stBinVwDir=cf.get("GLOBAL_CONFIG", "stBinVwDir")
		stBinFwDir=cf.get("GLOBAL_CONFIG", "stBinFwDir")
		stBinWinDir=cf.get("GLOBAL_CONFIG", "stBinWinDir")
		stLibWinDir=cf.get("GLOBAL_CONFIG", "stLibWinDir")
		stBinWinDir64=cf.get("GLOBAL_CONFIG", "stBinWinDir64")
		stLibWinDir64=cf.get("GLOBAL_CONFIG", "stLibWinDir64")
		stTestItDir=cf.get("GLOBAL_CONFIG", "stTestItDir")
		stEXPORTDir=cf.get("GLOBAL_CONFIG", "stEXPORTDir")
		stTestEXPORT=cf.get("GLOBAL_CONFIG", "stTestEXPORT")
		
		VS=cf.get("GLOBAL_CONFIG", "VS")
		VS64=cf.get("GLOBAL_CONFIG", "VS64")
		winQT=cf.get("GLOBAL_CONFIG", "winQT")
		
		stHome=cf2.get("GLOBAL_CONFIG",'stHome')
		bigModule=cf2.get("GLOBAL_CONFIG","bigModule")
		modulelist=cf2.get("GLOBAL_CONFIG","modulelist")
		stSrcDir=cf2.get("GLOBAL_CONFIG","stSrcDir")
		adaeDir=cf2.get("GLOBAL_CONFIG","adaeDir")
		vxworks=cf2.get("GLOBAL_CONFIG", "vxworks")
		ccs=cf2.get("GLOBAL_CONFIG", "ccs")

		if view in it_prj_list:
			stBinLinuxDir='IT/bin/linux'
			stLibLinuxDir='IT/lib/linux'
			stBinSunDir='IT/lib/sun'
			stLibSunDir='IT/lib/sun'
			stBinVwDir='IT/bin/vxworks'
			stBinFwDir='IT/bin/firmware'
			stBinWinDir='IT/bin/windows'
			stLibWinDir='IT/lib/windows'
			stBinWinDir64='IT/bin/windows-64'
			stLibWinDir64='IT/lib/windows-64'
			
		print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
		print " stUserName=%s\n stPasswd=%s\n  stCmdSun=%s\n stCmdWin=%s\n stSrcDir=%s\n stBinSunDir=%s\n stLibSunDir=%s\n stBinLinuxDir=%s\n stBinLinuxDir=%s\n stBinVwDir=%s\n stBinFwDir=%s\n stBinWinDir=%s\n stLibWinDir=%s\n stBinWinDir64=%s\n stLibWinDir64=%s\n stTestItDir=%s\n stEXPORTDir=%s\n stTestEXPORT=%s\n vxworks=%s\n ccs=%s\n VS=%s\n VS64=%s\n winQT=%s\n bigModule=%s\n modulelist=%s\n stHome=%s\n adaeDir=%s\n " \
			%(stUserName,stPasswd,stCmdSun,stCmdWin,stSrcDir,stBinSunDir,stLibSunDir,stBinLinuxDir,stBinLinuxDir,stBinVwDir,stBinFwDir,stBinWinDir,stLibWinDir,stBinWinDir64,stLibWinDir64,stTestItDir,stEXPORTDir,stTestEXPORT,vxworks,ccs,VS,VS64,winQT,bigModule,modulelist,stHome,adaeDir)
		print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
		# 上下位机编译配置，无需判断路径，os.getcwd() 替换LOCAL_DIR
		projectDir=PATH
		
	except BaseException,e:
		print `e`
		print 'read file '+scriptPath+', '+scriptPath2 +' failed'
		sys.exit(1)
		
def globalVariables(ostype):
	global STCMD,newStHome,VS ,vxVersion,stBinWinDir,stLibWinDir,stBinSunDir,stLibSunDir,it_prj_list
	newStHome='"smeebuilder:smeebuilder@'+stHome
	if 'LINUX' in ostype :
		STCMD=stCmdSun
		if view in it_prj_list:
			stBinSunDir='IT/bin/linux'
			stLibSunDir='IT/lib/linux'
		else:
			stBinSunDir='SIT/bin/linux'
			stLibSunDir='SIT/lib/linux'
			
	elif 'SUNOS' in ostype:
		STCMD=stCmdSun
		if view in it_prj_list:
			stBinSunDir='SIT/bin/sun'
			stLibSunDir='SIT/lib/sun'
		else:
			stBinSunDir='SIT/bin/sun'
			stLibSunDir='SIT/lib/sun'
		
	elif 'WINDOWS32' in ostype:
		#STCMD=stCmdWin
		STCMD="stcmd"
		print 'VS=%s\n' %VS
	else:
		STCMD="stcmd"
		stBinWinDir=stBinWinDir64
		stLibWinDir=stLibWinDir64
		VS=VS64
		print 'VS=%s\n' %VS
	if "vxworks-6.9" in vxworks:
		vxVersion=6.9
	print '=====STCMD=%s' %STCMD
	print '=====vxVersion=%s' %vxVersion
	print '=====stBinWinDir=%s' %stBinWinDir
	print '=====stLibWinDir=%s' %stLibWinDir

def ftpcfgFile(publiccfgPath,view,FILE):
	try:
		ftp=ftplib.FTP()
		ftp.connect('172.16.42.76',21)
	except BaseException,e:
		log(`e`)
		return -1
	try:
		ftp.login('publiccfg','x86x86')
	except BaseException,e:
		log(`e`)
		return -1
	#切换远程目录
	try:
		ftp.cwd(publiccfgPath+view)
	except BaseException,e:
		print `e`
		print 'No dir in /home/publiccfg/BuildCfg/'+view+' ,please create dir '+view+' in /home/publiccfg/BuildCfg/     [172.16.42.76/publiccfg/(x86x86)]'
		sys.exit(1)
		
	bufsize=1024
	fp=open(FILE,"wb")
	ftp.retrbinary("RETR "+FILE,fp.write,1024)
	fp.close()
	ftp.quit()
	
def ftpDir(localPath,remotePath):
	try:
		ftp=ftplib.FTP()
		ftp.connect('172.16.42.76',21)
	except BaseException,e:
		log(`e`)
		return -1
	try:
		ftp.login('publiccfg','x86x86')
	except BaseException,e:
		log(`e`)
		return -1
	#切换远程目录
	ftp.cwd(remotePath)
	subItems=ftp.nlst(remotePath) #获取目录下的文件
	print 'subItems=%s' %subItems
	for subItem in subItems:
		bufsize=8192
		localItem=subItem.split('/')[-1]
		print 'localItem=%s' %localItem
		fp=open((os.sep).join([localPath,localItem]),"wb")
		print 'checking out %s in %s' %(localItem,remotePath)
		ftp.retrbinary("RETR "+localItem,fp.write,8192)
	fp.close()
	ftp.quit()

def renameVW(PATH):
	if vxVersion==6.9:
		if os.path.exists((os.sep).join([PATH,stSrcDir,"Makefile_tpl_vw69"])):
			shutil.copy((os.sep).join([PATH,stSrcDir,"Makefile_tpl_vw69"]),(os.sep).join([PATH,stSrcDir,"Makefile_tpl_vw"]))
	else:
		if os.path.exists((os.sep).join([PATH,stSrcDir,"Makefile_tpl_vw55"])):
			shutil.copy((os.sep).join([PATH,stSrcDir,"Makefile_tpl_vw55"]),(os.sep).join([PATH,stSrcDir,"Makefile_tpl_vw"]))
def verify_BuildScript(drive):
	if os.path.exists(drive+'\BuildScript'):
		print "=====BuildScript has exist..."
	else:
		os.mkdir(drive+'\BuildScript')
		if os.path.exists(drive+'\BuildScript'):
			ftpDir(drive+'\BuildScript','/home/publiccfg/BuildCfg/BuildScript')
		else:
			print "=====BuildScript is not exist..."
			sys.exit(1)

def analyze_UNIX(stream,tempDir,project):
	global covType
	loginInfo=' --host 172.16.42.50 --port 8080 --user admin --password 123456 '
	print '=====stream: '+stream
	cmd='cov-analyze --dir '+tempDir +' --all --aggressiveness-level medium --disable UNUSED_VALUE --checker-option STACK_USE:max_single_base_use_bytes:20000 --checker-option STACK_USE:max_total_use_bytes:500000 --checker-option PASS_BY_VALUE:size_threshold:1024 --checker-option PASS_BY_VALUE:unmodified_threshold:1024 -j auto'
	sys_cmd(cmd)
	cmd='cov-manage-im --mode triage --add --set name:"'+project+'"'+loginInfo +'1>/dev/null 2>/dev/null'
	sys_cmd(cmd)
	cmd='cov-manage-im --mode streams --add --set name:"'+stream+'" --set component-map:"ALL" --set triage:"'+project+'"'+loginInfo+' 1>/dev/null 2>/dev/null'
	sys_cmd(cmd)
	cmd='cov-manage-im --mode projects --update --name "'+project+'-'+covType+'" --insert stream:"'+stream+'"'+loginInfo
	sys_cmd(cmd)
	cmd='cov-commit-defects --dataport 9090 --dir '+tempDir+' --host 172.16.42.50 --stream "'+stream+'" --user admin --password 123456'
	sys_cmd(cmd)
	if os.path.exists(tempDir):
		shutil.rmtree(tempDir)
		
def coverity_UNIX(homeDir,project,targetType,stSrcDir,componentName,componentDir):
	global covType
	if covType=='SYS':
		stream=project+'-'+targetType+'-SYS'
	else:
		stream=project+'-'+targetType+'-'+componentName 
	tempDir=homeDir+'/IDR/temp/'+stream
	if os.path.exists(tempDir):
		shutil.rmtree(tempDir)
	if "SYS" == buildType:
		os.chdir(adaeDir)
		cmd='cov-build --dir '+tempDir+' mvn clean install'
		rtn=sys_cmd(cmd)
		print 'rtn='+str(rtn)
		
		if rtn !=0:
			print '=====Build ADAE failed.'
		else:
			print '=====Build ADAE success.'
	os.chdir((os.sep).join([homeDir,project,stSrcDir,componentDir]))
	
	filepath=(os.sep).join([homeDir,project,stSrcDir,componentDir,componentName+'.pro'])
	print 'filepath=%s' %filepath
	if os.path.exists(filepath):
		cmd='qmake'
		sys_cmd(cmd)

	cmd='cov-build --dir '+tempDir +' gmake'
	rtn=sys_cmd(cmd)
	if rtn != 0:
		print '=====Build failed.'
		sys.exit(1)
	analyze_UNIX(stream,tempDir,project)
	
	

def biji():
	print '+++++++++++++++++++++++++++++备注++++++++++++++++++++++++++++++++++++++++++'
	print '前提条件,后台编译服务器家目录下有 updatepyqb.py'
	print '项目src/Project_config文件中的宏 修改为\n SUN_DIR = $(HOME)/对应的视图名称\n QT_DIR  = $$(HOME)/对应的视图名称\n LOCAL_DIR=$(HOME)/对应的视图名称\n'

if __name__ == "__main__":
	view=""
	label=""
	user=""
	passwd=""
	#sys.argv[0] 脚本名，sys.argv[1] 第一个参数
	print "=====len(sys.argv)=%d" %len(sys.argv)
	if len(sys.argv)==5:
		view=sys.argv[1]
		label=sys.argv[2]
		user=sys.argv[3]
		passwd=sys.argv[4]
		#ViewType=sys.argv[5]
		print "view=%s\n label=%s\n user=%s\n passwd=%s\n " %(view,label,user,passwd)
	else:
		print "argv num is error... [view,label,user,passwd]"
		sys.exit()
		
		
	system=platform.system()
	#ip=socket.gethostbyname(socket.gethostname())
	#print 'socket.gethostname()=%s' %socket.gethostname()
	try:
		s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		s.connect(('8.8.8.8',80))
		ip=s.getsockname()[0]
		s.close()
	except BaseException,e:
		print `e`
		ip=socket.gethostbyname(socket.gethostname())
	print "=====ip=%s" %ip
	
	if 'LINUX' in system.upper() or 'SUNOS' in system.upper():
		drive=os.getcwd()
		PATH=os.getcwd()+'/'+view
		if ip =='172.16.42.8':
			beCoverity=1
			
		if ip=='172.16.20.116':
			beCoverity=1
			
		if ip=='172.16.70.162':
			beCoverity=1
			
		if ip=='172.16.70.169':
			beCoverity=1
			
		print '=====you are running coverity build...'
	if 'WINDOWS' in system.upper():
		drive=os.getcwd()
		PATH=os.getcwd()+view
		if ip=='172.16.200.52':
			beCoverity=1
		if ip=='172.16.70.174':
			beCoverity=1
		print '=====you are running coverity build...'
		if os.path.exists('C:\Program Files (x86)'):
			system='WINDOWS64'
		else:system='WINDOWS32'
	
	print '=====System Operation=%s' %system
	print "=====PATH=%s" %PATH
	print '=====ip= '+ ip
	print '=====driver='+drive
	createprj(view,PATH)
	readConfigFile(drive,PATH,view)
	globalVariables(system.upper())
	labelAnalyze(view,system,PATH,label,beCoverity)
	checkoutfile(PATH,view,label)
	
	if 'LINUX' in system.upper() or 'SUNOS' in system.upper():
		if beCoverity==1:
			coverity_UNIX(drive,view,system.upper(),stSrcDir,componentName,componentDir)
		else:
			print 'this is a cov Build script ...'
			sys.exit(1)
	else:
		renameVW(PATH)
		verify_BuildScript(drive)
		lowerPCbuild(PATH)
		executeCov_WIN(drive,view,componentName,system.upper())
	print '=====update file basecovbuild.py to '+drive
	os.chdir(drive) #!!!
	ftpcfgFile('/home/publiccfg/BuildCfg/','pybuildScripts','basecovbuild.py')