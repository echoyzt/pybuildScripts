#_*_ coding:utf-8 _*_
import sys,os,shutil
import ConfigParser
import platform
import ftplib,socket


buildType=""  #编译类型：组件编译COMPONENT，模块编译MODULE，系统编译SYS,测试编译TEST
covType=""
viewType="" #视图类型:SysView,DevelopView,MachineView
moduleName=""
componentDirList=[]
componentDir=""
componentName=""
newStHome=""
newStHome2=""
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
stHome2=""
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
gitRepository=""
#======================================================

def log(str1):
	f=open('buildhistory.log','a+')
	f.write(str1+'\n')
	f.close()
def sys_cmd(cmd):
	#log(cmd)
	if flag_show==1:
		print "=====cmd:%s"%cmd
	else:pass
	#os.environ.update({'LANG':'zh_CN.GB18030'})
	return os.system(cmd)
	#os.environ.update({'LANG':'C'})
def movefile(fileName, dirpath):
	shutil.move(fileName,dirpath)
	
def createprj(view,PATH,ostype):
	#file='newbuild.cfg'
	file2='const.cfg'
	publiccfgPath='/home/publiccfg/BuildCfg/'
	
	if os.path.exists(PATH):
		print  PATH +' is already exist.====='
	else:
		os.mkdir(PATH)
		if os.path.exists(PATH):
			print '=====dir %s create success.' %PATH
	#ftpcfgFile(publiccfgPath,view,file)
	ftpcfgFile(publiccfgPath,'pybuildScripts',file2)

	#movefile((os.sep).join([os.getcwd(),file]),(os.sep).join([PATH,file]))
	movefile((os.sep).join([os.getcwd(),file2]),(os.sep).join([PATH,file2]))


def labelAnalyze(view,ViewType,ostype,PATH,label):
	global listLabel,buildType,covType,componentDirList,componentDir,moduleName,subLabel ,componentName,stTestItDir
	if '/' in label:
		return 0
	

	listLabel=label.split('_')
	print 'listLabel===='
	print listLabel
	if listLabel[1] != view:
		print '!!!!!The label %s does not match with the project %s' %(label,view)
		sys.exit(1)
	print '=====listLabel=%s' %listLabel
	num=len(listLabel)
	if 'BUILD' in label and 'TEST' not in label:
		listLabel.remove('BUILD')
		listLabel.remove('L')
		subLabel='_'.join(listLabel)
		print '=====the version [%s] will be writed in lib...' %subLabel
	if 	'BUILD' in label and 'TEST' in label:
		print '=====the label is invalide.'
		sys.exit(1)	
	if 'DevelopView' == ViewType:
		if 'SYS_TEST' in label:
			if ostype.upper()=='LINUX':
				sys_cmd('bash ./sysTestBuild')
				return 0
		else:
			if 'TEST' in label:
				buildType='TEST'
				listLabel.remove('TEST')
				listLabel.remove('L')
				subLabel='_'.join(listLabel)
				moduleName=listLabel[1]
				componentDirList=listLabel[1:-2]
				stTestItDir=stTestItDir+'/'+componentDirList[-1]
				componentDirList.append('test')
				print '=====stTestItDir=%s' %stTestItDir			
			else:
				if 'SWS' in label:
					print '=====Error Beacuse This is a DevelopView, so Can not sys build!!!.'
					sys.exit(1)
				else:
					moduleName=listLabel[1]
					componentDirList=listLabel[1:-2]
					if 1==len(listLabel[1:-2]):
						buildType='MODULE'
					else:buildType='COMPONENT'
					covType='CC'
	elif 'SysView' == ViewType:
		if 'SWS' in label:
			if (6==num):
				buildType='SYS'
				componentDirList=[""]
				covType='SYS'
			else:
				print ('=====SYS build,the label is invalide.')
				return 1
		else:
			moduleName=listLabel[1]
			componentDirList=listLabel[1:-2]
			if 1==len(listLabel[1:-2]):
				buildType='MODULE'
			else:
				buildType='COMPONENT'
				print '=====Error This is SysView, Can not component build!!!.'
			covType='CC'
	else: #机台视图
		if 'SWS' in label:
			if (6==num):
				buildType='SYS'
				componentDirList=[""]
				covType='SYS'
			else:
				print ('=====SYS build,the label is invalide.')
				return 1
		else:
			moduleName=listLabel[1]
			componentDirList=listLabel[1:-2]
			if 1==len(listLabel[1:-2]):
				buildType='MODULE'
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

def checkoutfile(PATH,system,label,gitqbType):
	print 'Starteam project:%s' %stHome
	os.environ.update({'LANG':'zh_CN.GB18030'})
	os.chdir(PATH)
	print "先删除后台目录文件，再重新初始化 git 仓库..."
	try:
		if os.path.exists(PATH+'/'+stSrcDir):
			for pwd, dirs, files in os.walk(PATH+'/'+stSrcDir,topdown=False):
				for name in files:
					#print 'files='+os.path.join(pwd,name)
					os.remove(os.path.join(pwd,name))
				for name in dirs:
					#print 'dirs='+os.path.join(pwd,name)
					os.rmdir(os.path.join(pwd,name))
		else:pass
		#os.mkdir((os.sep).join([PATH,stSrcDir]))
	except :
		if "WINDOWS" in system :
			os.system('rd /S /Q %s\%s>>nul' %(PATH,stSrcDir))

	cmd='git init'
	sys_cmd(cmd)
	print "git clone prjmake,xinc, from bitbucket Develop..."
	cmd='git clone http://'+userName+':'+userPassword+gitRepository+'prjmake.git ' + PATH+'/'+stSrcDir
	rtn=sys_cmd(cmd)
	if rtn != 0:
		print 'git clone prjmake.git failed...'
		sys.exit(-1)
	os.chdir((os.sep).join([PATH,stSrcDir]))
	cmd='git checkout -B develop origin/develop'
	sys_cmd(cmd)
	cmd='git branch -a'
	sys_cmd(cmd)
	
	
	cmd='git clone http://'+userName+':'+userPassword+gitRepository+'xinc.git '+  PATH+'/'+stSrcDir+'/TXINC'
	
	sys_cmd(cmd)
	os.chdir((os.sep).join([PATH,stSrcDir,'TXINC']))
	cmd='git checkout -B develop origin/develop'
	sys_cmd(cmd)
	cmd='git branch -a'
	sys_cmd(cmd)
	
	#os.system('mv %s/%s/TXINC/*  %s/%s' %(PATH,stSrcDir,PATH,stSrcDir))
	movefile((os.sep).join([PATH,stSrcDir,'TXINC/export']),(os.sep).join([PATH,stSrcDir]))
	movefile((os.sep).join([PATH,stSrcDir,'TXINC/xinc']),(os.sep).join([PATH,stSrcDir]))
	movefile((os.sep).join([PATH,stSrcDir,'TXINC/export_t']),(os.sep).join([PATH,stSrcDir]))
	#os.system('rm -rf %s/%s/TXINC' %(PATH,stSrcDir))
	try:
		print 'rm TXINC...1'
		shutil.rmtree((os.sep).join([PATH,stSrcDir,'TXINC']))
	except BaseException,e:
		print `e`
		if "WINDOWS" in system :
			print 'rm TXINC...2'
			os.system('rd /S /Q %s\%s\TXINC>>nul' %(PATH,stSrcDir))
	print 	'buildType='+buildType
	if buildType == "SYS":
		print 'git clone all modules from bitbucket develop ... '
		tPath=(os.sep).join([PATH,stSrcDir])
		os.chdir(tPath)
		tModulelist=re.sub(r'\s+',',',modulelist)
		for PRJ in tModulelist.split(','):
			if os.path.exists((os.sep).join([PATH,stSrcDir,PRJ])):
				shutil.rmtree((os.sep).join([PATH,stSrcDir,PRJ]))
			cmd='git clone -b develop http://'+userName+':'+userPassword+gitRepository+PRJ+'.git '+  PATH+'/'+stSrcDir+'/'+PRJ
			sys_cmd(cmd)
			os.chdir((os.sep).join([PATH,stSrcDir,PRJ]))
			cmd='git branch -a'
			sys_cmd(cmd)
		for dir in os.listdir((os.sep).join([PATH,stSrcDir])):
			if dir != "export" or dir != "export_t" or dir != "xinc":
				print '===== checking dir %s has the label.c ?' %dir
				if not  os.path.exists(dir/label.c):
					print '===== %s/label.c not exist in ST .Before SYS build, The Module %s Not Compiled.' %(dir,dir)
					return -1
	
	else:
		if gitqbType == "DevelopBuild":
			print '=====git clone %s from bitbucket develop...' %moduleName
			os.chdir((os.sep).join([PATH,stSrcDir]))
			os.system('rm -rf %s/%s/%s' %(PATH,stSrcDir,moduleName))
			#os.rmdir((os.sep).join([PATH,stSrcDir,moduleName]))
			cmd='git clone -b develop  http://'+userName+':'+userPassword+gitRepository+moduleName.lower()+'.git '+ PATH+'/'+stSrcDir+'/'+moduleName
			sys_cmd(cmd)
			os.chdir((os.sep).join([PATH,stSrcDir,moduleName]))
			cmd='git branch -a'
			sys_cmd(cmd)
		else:
			print "git clone %s from bitbucket feature ..." %moduleName
			os.chdir((os.sep).join([PATH,stSrcDir]))
			os.system('rm -rf %s/%s/%s' %(PATH,stSrcDir,moduleName))
			#os.rmdir((os.sep).join([PATH,stSrcDir,moduleName]))
				
			cmd='git clone -b feature/'+featureName +' http://'+userName+':'+userPassword+gitRepository+moduleName.lower()+'.git '+ PATH+'/'+stSrcDir+'/'+moduleName
			sys_cmd(cmd)
			os.chdir((os.sep).join([PATH,stSrcDir,moduleName]))
			cmd='git branch -a'
			sys_cmd(cmd)
		if buildType == 'TEST':
			print '=====Checking out %s from ST...' %stTestItDir
			cmd='%s delete-local -p %s/%s"  -fp %s/%s -filter "N" -x -nologo' %(STCMD,newStHome,stTestItDir,PATH,stTestItDir)
			sys_cmd(cmd)
			cmd='%s co           -p %s/%s"  -fp %s/%s -filter "MGIOU" -x -o -nologo' %(STCMD,newStHome,stTestItDir,PATH,stTestItDir)
			sys_cmd(cmd)

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
	if 	'SYS'==buildType:	
		for item in os.listdir((os.sep).join([PATH,stSrcDir])):
			if os.path.isfile((os.sep).join([PATH,stSrcDir,item])):
				if "Makefile_win" == item:
					winBuild=1
				else:pass
			else:pass
	else:
		if os.path.exists((os.sep).join([PATH,stSrcDir,componentDir,'Makefile_win'])):
			winBuild=1	
	print '=====vwBuild=%s,fwBuild=%s,winBuild=%s\n' %(vwBuild,fwBuild,winBuild)
	if 0==vwBuild and 0==fwBuild and 0==winBuild:
		print "=====there is no vxworks, fw,windows build..."
		sys.exit()
		
def executeMakeUnix(PATH):
	rtn = 1
	if not 'TEST'==buildType:
		print '=====Checking out %s' %stLibSunDir 
		cmd='%s delete-local -p %s/%s"  -fp %s/%s -filter "N" -x -nologo' %(STCMD,newStHome,stLibSunDir,PATH,stLibSunDir)
		sys_cmd(cmd)
		cmd='%s co           -p %s/%s"  -fp %s/%s -filter "MGIOU" -x -o -nologo' %(STCMD,newStHome,stLibSunDir,PATH,stLibSunDir)
		sys_cmd(cmd)
				
		print '=====Checking out %s' %stBinSunDir 
		cmd='%s delete-local -p %s/%s"  -fp %s/%s -filter "N" -x -nologo' %(STCMD,newStHome,stBinSunDir,PATH,stBinSunDir)
		sys_cmd(cmd)
		cmd='%s co           -p %s/%s"  -fp %s/%s -filter "MGIOU" -x -o -nologo' %(STCMD,newStHome,stBinSunDir,PATH,stBinSunDir)
		sys_cmd(cmd)
	
	
	
	os.environ.update({'LANG':'C'})
	makePath=(os.sep).join([PATH,stSrcDir,componentDir])
	os.chdir(makePath) #!!!
	filepath=(os.sep).join([PATH,stSrcDir,componentDir,componentName+'.pro'])
	print 'filepath=%s' %filepath
	try:
		if os.path.exists(filepath):
			cmd='qmake && gmake MM=%s && gmake clean || (rtn=-1 && exit -1)' %(moduleName)
			sys_cmd(cmd)
		else:
			if "SYS" != buildType:
				cmd='gmake MM=%s && gmake clean || (rtn=-1 && exit -1)' %(moduleName)
				sys_cmd(cmd)

			else:
				cmd='gmake && gmake clean || (rtn=-1 && exit -1)'
				sys_cmd(cmd)
	except BaseException,e:
		print `e`
		return -1
	return rtn
def executeMakeWin(drive,PATH):
	os.environ.update({'LANG':'C'})
	makePath=(os.sep).join([PATH,stSrcDir,componentDir])
	os.chdir(makePath) #!!!
	print '=====current dir=%s' %os.getcwd()
		
	if 1==vwBuild:
		print(' -----开始编译Vxworks...-----')
		print(' -----Checking out '+stBinVwDir+'-----')
		cmd='%s delete-local -p  %s/%s" -fp %s/%s -x -nologo -is -filter "N"' %(STCMD,newStHome,stBinVwDir,PATH,stBinVwDir)
		sys_cmd(cmd)
		cmd='%s co           -p  %s/%s" -fp %s/%s -x -nologo -is -filter "MOIGU" -o' %(STCMD,newStHome,stBinVwDir,PATH,stBinVwDir)
		sys_cmd(cmd)
		try:
			if vxVersion==6.9:
				cmd1=drive+'\BuildScript\\qbvxworks69.bat'
			else:
				cmd1=drive+'\BuildScript\\qbvxworks55.bat'
				
			if os.path.exists((os.sep).join([PATH,stSrcDir,"Makefile55"])) and 'SYS'==buildType and  vxVersion == 5.5 :
				cmd=cmd1+ ' && make  -f Makefile55 || goto End'
				sys_cmd(cmd)
			else:
				cmd=cmd1+' && make MM=%s || goto End' %(moduleName)
				sys_cmd(cmd)
		except BaseException,e:
			return -1
	if 1==fwBuild:
		print(' -----开始编译CCS...-----')
		print(' -----Checking out '+stBinFwDir +'...')
		cmd='%s delete-local -p %s/%s" -fp %s/%s -x -nologo -is -filter "N"' %(STCMD,newStHome,stBinFwDir,PATH,stBinFwDir)
		sys_cmd(cmd)
		cmd='%s co           -p %s/%s" -fp %s/%s -x -nologo -is -filter "MOIGU" -o' %(STCMD,newStHome,stBinFwDir,PATH,stBinFwDir)
		sys_cmd(cmd)
		cmd1=drive+'\BuildScript\\qbccs.bat'
		try:
			if os.path.exists((os.sep).join([PATH,stSrcDir,"Makefile55"])) and 'SYS'==buildType and vxVersion == 5.5 :
				cmd=cmd1+' && gmake -f Makefile55 || goto End'
				sys_cmd(cmd)
			else :
				cmd=cmd1+' && gmake MM=%s || goto End' %(moduleName)
				sys_cmd(cmd)
		except BaseException,e:
			return -1
	if 1 == winBuild:
		print(' -----开始编译Windows...')
		print( '-----Checking out'+ stBinWinDir + stLibWinDir +'...')
		cmd='%s delete-local -p %s/%s" -fp %s/%s -x -nologo -is -filter "N"' %(STCMD,newStHome,stBinWinDir,PATH,stBinWinDir)
		sys_cmd(cmd)
		cmd='%s co -p  %s/%s" -fp  %s/%s -x -nologo -is -filter "MOIGU" -o' %(STCMD,newStHome,stBinWinDir,PATH,stBinWinDir)
		sys_cmd(cmd)
		cmd='%s delete-local -p  %s/%s" -fp %s/%s -x -nologo -is -filter "N"' %(STCMD,newStHome,stLibWinDir,PATH,stLibWinDir)
		sys_cmd(cmd)
		cmd='%s co -p %s/%s" -fp %s/%s -x -nologo -is -filter "MOIGU" -o' %(STCMD,newStHome,stLibWinDir,PATH,stLibWinDir)
		sys_cmd(cmd)
		try:
			if 'WINDOWS32' in system.upper():
				cmd1=drive+'\BuildScript\\qbwindows32.bat'
			else:
				cmd1=drive+'\BuildScript\\qbwindows64.bat'
			print '====='+(os.sep).join([PATH,stSrcDir,componentDir,componentName+'.pro'])
			if os.path.exists((os.sep).join([PATH,stSrcDir,componentDir,componentName+'.pro'])):
				cmd=cmd1+' && qmake && nmake MM=%s all || goto End' %(moduleName)
				sys_cmd(cmd)
			else :
				print( "-----run Makefile_win...")
				cmd=cmd1+' && nmake MM=%s /f Makefile_win || goto End' %(moduleName)
				sys_cmd(cmd)
		except BaseException,e:
			return -1


def checkinfile(PATH,ostype,label,userName):
	global newStHome,newStHome2,stTestItDir
	print '=====checkinfile====='
	os.environ.update({'LANG':'zh_CN.GB18030'})
	print '====='+ostype
	os.chdir(PATH)
	if 'LINUX' in ostype.upper() or 'SUNOS' in ostype.upper():
		cmd='%s update-status -p %s/%s" "*"' %(STCMD,newStHome,stLibSunDir)
		sys_cmd(cmd)
		cmd='%s update-status -p %s/%s" "*"' %(STCMD,newStHome,stBinSunDir)
		sys_cmd(cmd)
		cmd='%s apply-label -p %s/%s" -is -filter "M" -lbl "%s"' %(STCMD,newStHome,stLibSunDir,label)
		sys_cmd(cmd)
		cmd='%s apply-label -p %s/%s" -is -filter "M" -lbl "%s"' %(STCMD,newStHome,stBinSunDir,label)
		sys_cmd(cmd)
		print "Starting to check in lib and bin files to StarTeam..."
		
		if gitqbType =="DevelopBuild":
			if "TEST" != buildType:
				cmd='%s ci  -p %s/%s" -fp %s/%s -is -vl "%s" -r "%s:%s" -filter "M" -nologo' %(STCMD,newStHome,stLibSunDir,PATH,stLibSunDir,label,userName,label)
				sys_cmd(cmd)
				cmd='%s add -p %s/%s" -fp %s/%s -is -d "%s:%s" -vl "%s" -nologo' %(STCMD,newStHome,stLibSunDir,PATH,stLibSunDir,userName,label,label)
				sys_cmd(cmd)
				cmd='%s ci  -p %s/%s" -fp %s/%s -is -vl "%s" -r "%s:%s" -filter "M" -nologo' %(STCMD,newStHome,stBinSunDir,PATH,stBinSunDir,label,userName,label)
				sys_cmd(cmd)
				cmd='%s add -p %s/%s" -fp %s/%s -is -d "%s:%s" -vl "%s" -nologo' %(STCMD,newStHome,stBinSunDir,PATH,stBinSunDir,userName,label,label)
				sys_cmd(cmd)
				print "git 编译，无需 label.c 上传 ST,但要commit 到 bitbucket,用户需要push develop 分支权限"
				'''
				git 编译，无需 label.c 上传 ST,但要commit 到 bitbucket,用户需要push develop 分支权限
				if "SYS" != buildType:
					print "=====check in label.c to ST..."
					cmd='%s add -p %s/%s/%s" -fp %s/%s/%s -d "%s:%s" -vl "%s" -nologo  label.c' %(STCMD,newStHome,stSrcDir,moduleName,PATH,stSrcDir,moduleName,userName,label,label)
					sys_cmd(cmd)
					cmd='%s ci  -p %s/%s/%s" -fp %s/%s/%s -o -vl "%s" -r "%s:%s" -nologo  label.c' %(STCMD,newStHome,stSrcDir,moduleName,PATH,stSrcDir,moduleName,label,userName,label)
					sys_cmd(cmd)
				'''
			else:
				cmd='%s update-status -p %s/%s" "*"' %(STCMD,newStHome,stTestItDir)
				sys_cmd(cmd)
				cmd='%s apply-label -p %s/%s"  -is  -filter "M" -lbl "%s"' %(STCMD,newStHome,stTestItDir,label)
				sys_cmd(cmd)
				print "Starting to check in lib and bin files to StarTeam..."
				cmd='%s ci  -p %s/%s" -fp %s/%s -is -vl "%s" -r "%s:%s" -filter "M" -nologo' %(STCMD,newStHome,stTestItDir,PATH,stTestItDir,label,userName,label)
				sys_cmd(cmd)
				cmd='%s add -p %s/%s" -fp %s/%s -is -d "%s:%s" -vl "%s" -nologo' %(STCMD,newStHome,stTestItDir,PATH,stTestItDir,userName,label,label)
				sys_cmd(cmd)
		else:
			lineList=[]
			cmd='%s list -p %s/%s" -fp %s/%s  -is   -nologo -filter "MN">%s/temp.txt' %(STCMD,newStHome,stLibSunDir,PATH,stLibSunDir,PATH)
			sys_cmd(cmd)
			cmd='%s list -p %s/%s" -fp %s/%s  -is   -nologo -filter "MN"' %(STCMD,newStHome,stLibSunDir,PATH,stLibSunDir)
			sys_cmd(cmd)
			
			fout=open('temp.txt')
			while True:
				line=fout.readline()
				if not line:
					break
				lineList= line.split(' ')
				print lineList
				if "Not" == lineList[0]:
					cmd='%s add -p  %s/%s" -fp %s/%s -is  -vl "%s"  -d "%s:%s"  -nologo %s'  %(STCMD,newStHome2,stLibSunDir,PATH,stLibSunDir,label,userName,moduleName,lineList[-1].replace('\n', ''))
					sys_cmd(cmd)
					cmd='%s ci  -p  %s/%s" -fp %s/%s -is  -vl "%s"  -o -r "%s:%s"  -nologo %s' %(STCMD,newStHome2,stLibSunDir,PATH,stLibSunDir,label,userName,moduleName,lineList[-1].replace('\n', ''))
					sys_cmd(cmd)
				if "Modified" == lineList[0]:
					cmd='%s add -p  %s/%s" -fp %s/%s -is  -vl "%s"  -d "%s:%s"  -nologo %s'  %(STCMD,newStHome2,stLibSunDir,PATH,stLibSunDir,label,userName,moduleName,lineList[-1].replace('\n', ''))
					sys_cmd(cmd)
					cmd='%s ci  -p  %s/%s" -fp %s/%s -is  -vl "%s"  -o -r "%s:%s"  -nologo %s' %(STCMD,newStHome2,stLibSunDir,PATH,stLibSunDir,label,userName,moduleName,lineList[-1].replace('\n', ''))
					sys_cmd(cmd)
		
			cmd='%s list -p %s/%s" -fp %s/%s  -is   -nologo -filter "MN">%s/temp.txt' %(STCMD,newStHome,stBinSunDir,PATH,stBinSunDir,PATH)
			sys_cmd(cmd)
			cmd='%s list -p %s/%s" -fp %s/%s  -is   -nologo -filter "MN"' %(STCMD,newStHome,stBinSunDir,PATH,stBinSunDir)
			sys_cmd(cmd)
			
			fout=open('temp.txt')
			while True:
				line=fout.readline()
				if not line:
					break
				lineList= line.split(' ')
				print lineList
				if "Not" == lineList[0]:
					cmd='%s add -p  %s/%s" -fp %s/%s -is  -vl "%s"  -d "%s:%s"  -nologo %s'  %(STCMD,newStHome2,stBinSunDir,PATH,stBinSunDir,label,userName,moduleName,lineList[-1].replace('\n', ''))
					sys_cmd(cmd)
					cmd='%s ci  -p  %s/%s" -fp %s/%s -is  -vl "%s"  -o -r "%s:%s"  -nologo %s' %(STCMD,newStHome2,stBinSunDir,PATH,stBinSunDir,label,userName,moduleName,lineList[-1].replace('\n', ''))
					sys_cmd(cmd)
				if "Modified" == lineList[0]:
					cmd='%s add -p  %s/%s" -fp %s/%s -is  -vl "%s"  -d "%s:%s"  -nologo %s'  %(STCMD,newStHome2,stBinSunDir,PATH,stBinSunDir,label,userName,moduleName,lineList[-1].replace('\n', ''))
					sys_cmd(cmd)
					cmd='%s ci  -p  %s/%s" -fp %s/%s -is  -vl "%s"  -o -r "%s:%s"  -nologo %s' %(STCMD,newStHome2,stBinSunDir,PATH,stBinSunDir,label,userName,moduleName,lineList[-1].replace('\n', ''))
					sys_cmd(cmd)
		
		print '=====delete temp file temp.txt'
		os.system('rm -rf %s/temp.txt' %(PATH))
			
				
				
	else:
		if vwBuild==1:
			if gitqbType == "FeatureBuild" :
				lineList=[]
				cmd='%s update-status -p %s/%s" ' %(STCMD,newStHome,stBinVwDir)
				sys_cmd(cmd)
				cmd='%s list -p %s/%s" -fp %s/%s -is -nologo -filter "MN">%s\\tempVW.txt' %(STCMD,newStHome,stBinVwDir,PATH,stBinVwDir,PATH)
				sys_cmd(cmd)
				cmd='%s list -p %s/%s" -fp %s/%s -is -nologo -filter "MN"' %(STCMD,newStHome,stBinVwDir,PATH,stBinVwDir)
				sys_cmd(cmd)
				
				fout=open('tempVW.txt')
				while True:
					line=fout.readline()
					if not line:
						break
					lineList= line.split(' ')
					print lineList
					if "Not" == lineList[0]:
						cmd='%s add -p  %s/%s" -fp %s/%s -is  -vl "%s"  -d "%s:%s"  -nologo %s'  %(STCMD,newStHome2,stBinVwDir,PATH,stBinVwDir,label,userName,moduleName,lineList[-1].replace('\n', ''))
						sys_cmd(cmd)
						cmd='%s ci  -p  %s/%s" -fp %s/%s -is  -vl "%s"  -o -r "%s:%s"  -nologo %s' %(STCMD,newStHome2,stBinVwDir,PATH,stBinVwDir,label,userName,moduleName,lineList[-1].replace('\n', ''))
						sys_cmd(cmd)
					if "Modified" == lineList[0]:
						cmd='%s add -p  %s/%s" -fp %s/%s -is  -vl "%s"  -d "%s:%s"  -nologo %s'  %(STCMD,newStHome2,stBinVwDir,PATH,stBinVwDir,label,userName,moduleName,lineList[-1].replace('\n', ''))
						sys_cmd(cmd)
						cmd='%s ci  -p  %s/%s" -fp %s/%s -is  -vl "%s"  -o -r "%s:%s"  -nologo %s' %(STCMD,newStHome2,stBinVwDir,PATH,stBinVwDir,label,userName,moduleName,lineList[-1].replace('\n', ''))
						sys_cmd(cmd)
				fout.close()	
			else :
				cmd='%s update-status -p %s/%s" "*"' %(STCMD,newStHome,stBinVwDir)
				sys_cmd(cmd)
				cmd='%s apply-label -p %s/%s" -is  -filter "M" -lbl "%s"' %(STCMD,newStHome,stBinVwDir,label)
				sys_cmd(cmd)
				cmd='%s ci  -p %s/%s" -fp %s/%s -is -vl "%s" -r "%s %s" -filter "M" -nologo' %(STCMD,newStHome,stBinVwDir,PATH,stBinVwDir,label,userName,label)
				sys_cmd(cmd)
				cmd='%s add -p %s/%s" -fp %s/%s -is  -vl "%s" -nologo' %(STCMD,newStHome,stBinVwDir,PATH,stBinVwDir,label)
				sys_cmd(cmd)
		
		
		
		if fwBuild==1:
			if gitqbType == "FeatureBuild" :
				lineList=[]
				cmd='%s update-status -p %s/%s" ' %(STCMD,newStHome,stBinFwDir)
				sys_cmd(cmd)
				cmd='%s list -p %s/%s" -fp %s/%s -is -nologo -filter "MN">%s\\tempFW.txt' %(STCMD,newStHome,stBinFwDir,PATH,stBinFwDir,PATH)
				sys_cmd(cmd)
				cmd='%s list -p %s/%s" -fp %s/%s -is -nologo -filter "MN"' %(STCMD,newStHome,stBinFwDir,PATH,stBinFwDir)
				sys_cmd(cmd)
				
				fout2=open('tempFW.txt')
				while True:
					line=fout2.readline()
					if not line:
						break
					lineList= line.split(' ')
					print lineList
					if "Not" == lineList[0]:
						cmd='%s add -p  %s/%s" -fp %s/%s -is  -vl "%s"  -d "%s:%s"  -nologo %s'  %(STCMD,newStHome2,stBinFwDir,PATH,stBinFwDir,label,userName,moduleName,lineList[-1].replace('\n', ''))
						sys_cmd(cmd)
						cmd='%s ci  -p  %s/%s" -fp %s/%s -is  -vl "%s"  -o -r "%s:%s"  -nologo %s' %(STCMD,newStHome2,stBinFwDir,PATH,stBinFwDir,label,userName,moduleName,lineList[-1].replace('\n', ''))
						sys_cmd(cmd)
					if "Modified" == lineList[0]:
						cmd='%s add -p  %s/%s" -fp %s/%s -is  -vl "%s"  -d "%s:%s"  -nologo %s'  %(STCMD,newStHome2,stBinFwDir,PATH,stBinFwDir,label,userName,moduleName,lineList[-1].replace('\n', ''))
						sys_cmd(cmd)
						cmd='%s ci  -p  %s/%s" -fp %s/%s -is  -vl "%s"  -o -r "%s:%s"  -nologo %s' %(STCMD,newStHome2,stBinFwDir,PATH,stBinFwDir,label,userName,moduleName,lineList[-1].replace('\n', ''))
						sys_cmd(cmd)
				fout2.close()
			else:
				cmd='%s update-status -p %s/%s" "*"' %(STCMD,newStHome,stBinFwDir)
				sys_cmd(cmd)
				cmd='%s apply-label -p %s/%s" -is  -filter "M" -lbl "%s"' %(STCMD,newStHome,stBinFwDir,label)
				sys_cmd(cmd)
				cmd='%s ci  -p %s/%s" -fp %s/%s -is -vl "%s" -r "%s %s" -filter "M" -nologo' %(STCMD,newStHome,stBinFwDir,PATH,stBinFwDir,label,userName,label)
				sys_cmd(cmd)
				cmd='%s add -p %s/%s" -fp %s/%s -is  -vl "%s" -nologo' %(STCMD,newStHome,stBinFwDir,PATH,stBinFwDir,label)
				sys_cmd(cmd)
				
		if winBuild==1:
			if gitqbType == "FeatureBuild" :
				lineList=[]
				cmd='%s update-status -p %s/%s" ' %(STCMD,newStHome,stLibWinDir)
				sys_cmd(cmd)
				cmd='%s list -p %s/%s" -fp %s/%s -is -nologo -filter "MN">%s\\templib.txt' %(STCMD,newStHome,stLibWinDir,PATH,stLibWinDir,PATH)
				sys_cmd(cmd)
				cmd='%s list -p %s/%s" -fp %s/%s -is -nologo -filter "MN"' %(STCMD,newStHome,stLibWinDir,PATH,stLibWinDir)
				sys_cmd(cmd)
				cmd='%s update-status -p %s/%s" ' %(STCMD,newStHome,stBinWinDir)
				sys_cmd(cmd)
				cmd='%s list -p %s/%s" -fp %s/%s -is -nologo -filter "MN">%s\\tempbin.txt' %(STCMD,newStHome,stBinWinDir,PATH,stBinWinDir,PATH)
				sys_cmd(cmd)
				cmd='%s list -p %s/%s" -fp %s/%s -is -nologo -filter "MN"' %(STCMD,newStHome,stBinWinDir,PATH,stBinWinDir)
				sys_cmd(cmd)
				fout3=open('templib.txt')
				while True:
					line=fout3.readline()
					if not line:
						break
					lineList= line.split(' ')
					print lineList
					if "Not" == lineList[0]:
						cmd='%s add -p  %s/%s" -fp %s/%s -is  -vl "%s"  -d "%s:%s"  -nologo %s'  %(STCMD,newStHome2,stLibWinDir,PATH,stLibWinDir,label,userName,moduleName,lineList[-1].replace('\n', ''))
						sys_cmd(cmd)
						cmd='%s ci  -p  %s/%s" -fp %s/%s -is  -vl "%s"  -o -r "%s:%s"  -nologo %s' %(STCMD,newStHome2,stLibWinDir,PATH,stLibWinDir,label,userName,moduleName,lineList[-1].replace('\n', ''))
						sys_cmd(cmd)
					if "Modified" == lineList[0]:
						cmd='%s add -p  %s/%s" -fp %s/%s -is  -vl "%s"  -d "%s:%s"  -nologo %s'  %(STCMD,newStHome2,stLibWinDir,PATH,stLibWinDir,label,userName,moduleName,lineList[-1].replace('\n', ''))
						sys_cmd(cmd)
						cmd='%s ci  -p  %s/%s" -fp %s/%s -is  -vl "%s"  -o -r "%s:%s"  -nologo %s' %(STCMD,newStHome2,stLibWinDir,PATH,stLibWinDir,label,userName,moduleName,lineList[-1].replace('\n', ''))
						sys_cmd(cmd)
				fout3.close()		
				
				
				fout4=open('tempbin.txt')
				while True:
					line=fout4.readline()
					if not line:
						break
					lineList= line.split(' ')
					print lineList
					if "Not" == lineList[0]:
						cmd='%s add -p  %s/%s" -fp %s/%s -is  -vl "%s"  -d "%s:%s"  -nologo %s'  %(STCMD,newStHome2,stBinWinDir,PATH,stBinWinDir,label,userName,moduleName,lineList[-1].replace('\n', ''))
						sys_cmd(cmd)
						cmd='%s ci  -p  %s/%s" -fp %s/%s -is  -vl "%s"  -o -r "%s:%s"  -nologo %s' %(STCMD,newStHome2,stBinWinDir,PATH,stBinWinDir,label,userName,moduleName,lineList[-1].replace('\n', ''))
						sys_cmd(cmd)
					if "Modified" == lineList[0]:
						cmd='%s add -p  %s/%s" -fp %s/%s -is  -vl "%s"  -d "%s:%s"  -nologo %s'  %(STCMD,newStHome2,stBinWinDir,PATH,stBinWinDir,label,userName,moduleName,lineList[-1].replace('\n', ''))
						sys_cmd(cmd)
						cmd='%s ci  -p  %s/%s" -fp %s/%s -is  -vl "%s"  -o -r "%s:%s"  -nologo %s' %(STCMD,newStHome2,stBinWinDir,PATH,stBinWinDir,label,userName,moduleName,lineList[-1].replace('\n', ''))
						sys_cmd(cmd)
				fout4.close()		
			else:
				cmd='%s update-status -p %s/%s" "*"' %(STCMD,newStHome,stBinWinDir)
				sys_cmd(cmd)
				cmd='%s apply-label -p %s/%s" -is  -filter "M" -lbl "%s"' %(STCMD,newStHome,stBinWinDir,label)
				sys_cmd(cmd)
				
				cmd='%s update-status -p %s/%s" "*"' %(STCMD,newStHome,stLibWinDir)
				sys_cmd(cmd)
				cmd='%s apply-label -p %s/%s" -is  -filter "M" -lbl "%s"' %(STCMD,newStHome,stLibWinDir,label)
				sys_cmd(cmd)
				
				cmd='%s ci -p %s/%s" -fp %s/%s -vl "%s" -r "%s %s" -filter "M" -nologo -is' %(STCMD,newStHome,stBinWinDir,PATH,stBinWinDir,label,userName,label)
				sys_cmd(cmd)
				cmd='%s add -p %s/%s" -fp %s/%s  -vl "%s" -nologo -is' %(STCMD,newStHome,stBinWinDir,PATH,stBinWinDir,label)
				sys_cmd(cmd)
				cmd='%s ci -p %s/%s" -fp %s/%s -vl "%s" -r "%s %s" -filter "M" -nologo -is' %(STCMD,newStHome,stLibWinDir,PATH,stLibWinDir,label,userName,label)
				sys_cmd(cmd)
				cmd='%s add -p %s/%s" -fp %s/%s  -vl "%s" -nologo -is' %(STCMD,newStHome,stLibWinDir,PATH,stLibWinDir,label)
				sys_cmd(cmd)
				
				
		print "delete temp file tempVW.txt,tempFW.txt, templib.txt,tempbin.txt"
		if os.path.exists(PATH+'\\tempVW.txt'):
			#fout.close()
			os.remove((os.sep).join([PATH,'tempVW.txt']))
		if os.path.exists(PATH+'\\tempFW.txt'):
			#fout2.close()
			os.remove((os.sep).join([PATH,'tempFW.txt']))
		if os.path.exists(PATH+'\\templib.txt'):
			#fout3.close()
			os.remove((os.sep).join([PATH,'templib.txt']))
		if os.path.exists(PATH+'\\tempbin.txt'):
			#fout4.close()
			os.remove((os.sep).join([PATH,'tempbin.txt']))


			

			

def stringslabel(PATH):
	fileLabel=open((os.sep).join([ PATH,stSrcDir,moduleName,'label.c']),'wt')
	fileLabel.write('#include "string.h"\n')
	fileLabel.write('void label(){\n')
	fileLabel.write('static char *lbl="LABEL:'+subLabel+'";\n')
	fileLabel.write('char *lbl2=NULL;\n')
	fileLabel.write('lbl2=lbl;\n')
	fileLabel.write('lbl=lbl2;\n')
	fileLabel.write('lbl=NULL;\n')
	fileLabel.write('lbl2=NULL;\n')
	fileLabel.write('return;\n')
	fileLabel.write('}\n')
def readConfigFile(PATH):
	print "run readConfigFile"
	global bigModule,stUserName,stPasswd,stHome,stHome2,stCmdSun,stCmdWin,stSrcDir,stBinSunDir,stLibSunDir,stBinVwDir,stBinFwDir,stBinWinDir,stLibWinDir,stBinWinDir64,stLibWinDir64,stTestItDir,stEXPORTDir,stTestEXPORT,vxworks,ccs,VS,VS64,winQT,projectDir,modulelist,gitRepository
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
		
		stHome=cf2.get("GLOBAL_CONFIG", "stHome")
		stHome2=cf2.get("GLOBAL_CONFIG", "stHome2")
		bigModule=cf2.get("GLOBAL_CONFIG", "bigModule")
		modulelist=cf2.get("GLOBAL_CONFIG", "modulelist")
		stSrcDir=cf2.get("GLOBAL_CONFIG", "stSrcDir")
		vxworks=cf2.get("GLOBAL_CONFIG", "vxworks")
		ccs=cf2.get("GLOBAL_CONFIG", "ccs")
		gitRepository=cf2.get("GLOBAL_CONFIG", "gitRepository")
		print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
		print " stUserName=%s\n stPasswd=%s\n stHome=%s\n stHome2=%s\n stCmdSun=%s\n stCmdWin=%s\n stSrcDir=%s\n stBinSunDir=%s\n stLibSunDir=%s\n stBinVwDir=%s\n stBinFwDir=%s\n stBinWinDir=%s\n stLibWinDir=%s\n stBinWinDir64=%s\n stLibWinDir64=%s\n stTestItDir=%s\n stEXPORTDir=%s\n stTestEXPORT=%s\n vxworks=%s\n ccs=%s\n VS=%s\n VS64=%s\n winQT=%s\n modulelist=%s\n gitRepository=%s\n" \
			%(stUserName,stPasswd,stHome,stHome2,stCmdSun,stCmdWin,stSrcDir,stBinSunDir,stLibSunDir,stBinVwDir,stBinFwDir,stBinWinDir,stLibWinDir,stBinWinDir64,stLibWinDir64,stTestItDir,stEXPORTDir,stTestEXPORT,vxworks,ccs,VS,VS64,winQT,modulelist,gitRepository)
		print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
		# 上下位机编译配置，无需判断路径，os.getcwd() 替换LOCAL_DIR
		projectDir=PATH
		
	except BaseException,e:
		print `e`
		print 'read file '+scriptPath+', '+scriptPath2 +' failed'
		ftpcfgFile('/home/publiccfg/BuildCfg/gitqb/','update','updategitqb.py')
		sys.exit(1)

def globalVariables(ostype):
	global STCMD,newStHome,newStHome2,VS ,vxVersion,stBinWinDir,stLibWinDir,stBinSunDir,stLibSunDir
	newStHome='"smeebuilder:smeebuilder@'+stHome
	newStHome2='"smeebuilder:smeebuilder@'+stHome2
	if 'LINUX' in ostype :
		STCMD=stCmdSun
		stBinSunDir='SIT/bin/linux'
		stLibSunDir='SIT/lib/linux'
	elif 'SUNOS' in ostype:
		STCMD=stCmdSun
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
		sys.exit(1)
	try:
		ftp.login('publiccfg','x86x86')
	except BaseException,e:
		log(`e`)
		return -1
		sys.exit(1)
	#切换远程目录
	try:
		ftp.cwd(publiccfgPath+view)
	except BaseException,e:
		print `e`
		return -1
		sys.exit(1)
	bufsize=1024
	fp=open(FILE,"wb")
	ftp.retrbinary("RETR "+FILE,fp.write,1024)
	fp.close()
	ftp.quit()
	return 0

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
	return 0

def renameVW(PATH):
	if vxVersion==6.9:
		if os.path.exists((os.sep).join([PATH,stSrcDir,"Makefile_tpl_vw69"])):
			shutil.copy((os.sep).join([PATH,stSrcDir,"Makefile_tpl_vw69"]),(os.sep).join([PATH,stSrcDir,"Makefile_tpl_vw"]))
	else:
		if os.path.exists((os.sep).join([PATH,stSrcDir,"Makefile_tpl_vw55"])):
			shutil.copy((os.sep).join([PATH,stSrcDir,"Makefile_tpl_vw55"]),(os.sep).join([PATH,stSrcDir,"Makefile_tpl_vw"]))
def verify_BuildScript(drive):
	if os.path.exists(drive+'\BuildScript'):
		print "=====BuildScript is exist..."
		ftpDir(drive+'\BuildScript','/home/publiccfg/BuildCfg/BuildScript')
	else:
		os.mkdir(drive+'\BuildScript')
		if os.path.exists(drive+'\BuildScript'):
			ftpDir(drive+'\BuildScript','/home/publiccfg/BuildCfg/BuildScript')
		else:
			print "=====BuildScript is not exist..."
			sys.exit(1)

def rmlabel(PATH,stSrcDir):
	cmd='%s/%s/label.c' %(PATH,stSrcDir)
	#print '====='+cmd
	if os.path.exists(cmd):
		os.remove(cmd)
					
def biji():
		print 'git pro : 009Agit, 012Dgit, 019git,205B,TL219'
if __name__ == "__main__":
	view=""
	gitqbType=""
	label=""
	userName=""
	userPassword=""
	view=sys.argv[1]
	gitqbType=sys.argv[2]
	if gitqbType == "DevelopBuild" :
		label=sys.argv[3]
		userName=sys.argv[4]
		userPassword=sys.argv[5]
		ViewType=sys.argv[6]
	else:
		featureName=sys.argv[3]
		label=sys.argv[4]
		userName=sys.argv[5]
		userPassword=sys.argv[6]
		ViewType=sys.argv[7]
		print "featureName=%s\n" %(featureName)
	print "view=%s\n gitqbType=%s\n  label=%s\n userName=%s\n userPassword=%s\n ViewType=%s\n" %(view,gitqbType,label,userName,userPassword,ViewType)
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
	flag_show=1
	if 'LINUX' in system.upper() or 'SUNOS' in system.upper():
		drive=os.getcwd()
		PATH=os.getcwd()+'/'+view
	if 'WINDOWS' in system.upper():
		drive=os.getcwd()
		PATH=os.getcwd()+view
		if os.path.exists('C:\Program Files (x86)'):
			system='WINDOWS64'
		else:system='WINDOWS32'
	print '=====System Operation=%s' %system
	print "=====PATH=%s" %PATH
	createprj(view,PATH,system.upper())
	readConfigFile(PATH)
	globalVariables(system.upper())
	labelAnalyze(view,ViewType,system,PATH,label)
	checkoutfile(PATH,system.upper(),label,gitqbType)
	rmlabel(PATH,stSrcDir)
	stringslabel(PATH)
	
	
	if 'LINUX' in system.upper() or 'SUNOS' in system.upper():
		rtn=executeMakeUnix(PATH)
		print '=====rtn='+str(rtn)
		if rtn != -1:
			checkinfile(PATH,system,label,userName)
	else:
		renameVW(PATH)
		verify_BuildScript(drive)
		lowerPCbuild(PATH)
		rtn=executeMakeWin(drive,PATH)
		print '=====rtn='+str(rtn)
		if rtn != -1 :
			checkinfile(PATH,system,label,userName)
	print '=====update file updategitqb.py'
	os.chdir(drive) #!!!

	ftpcfgFile('/home/publiccfg/BuildCfg/gitqb/','update','updategitqb.py')
	biji()
	os._exit(0)