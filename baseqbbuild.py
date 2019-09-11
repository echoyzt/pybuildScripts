#_*_ coding:utf-8 _*_
import sys,os,shutil,re,time
import ConfigParser
import platform
import ftplib,socket
#python pyqbbuild.py 008A L_008A_EN_CE_BUILD_0.1.25_20190214 yuzt yuzt021zsh DevelopView 
buildType=""  #�������ͣ�������룬ģ����룬ϵͳ����,���Ա���
covType=""
viewType="" #��ͼ����:SysView,DevelopView,MachineView
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
flag_show=1
bool_ci=True
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
dict_prj={'50417':'208005','50417_02':'205003','018manufacture2':'018','504-4.5G_src':'504','SSB500_10M':'203M','SSB500_30':'205','SSB500_25P':'509','SSB545_10':'206'}
#not_cmdb_list='006,506,506A,008,301C,205C,20516'
it_prj_list='018,018A,018manufacture2'
userlist='yanw,chencl,zhaozl,yuech,lujt,yul,zhangwm,yuzt'
sysviews='301C,205C'
tsysview=""
#==============================================================================
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
	file='newbuild.cfg'
	file2='const.cfg'
	publiccfgPath='/home/publiccfg/BuildCfg'
	if os.path.exists(PATH):
		print  PATH +' is already exist.====='
		if os.path.exists((os.sep).join([PATH,'XINCBAK'])):
			print  (os.sep).join([PATH,'XINCBAK']) +' is already exist.====='
		else:
			os.mkdir((os.sep).join([PATH,'XINCBAK']))
			if os.path.exists((os.sep).join([PATH,'XINCBAK'])):
				print  (os.sep).join([PATH,'XINCBAK']) +' is already exist.====='
	else:
		os.mkdir(PATH)
		os.mkdir((os.sep).join([PATH,'XINCBAK']))
		if os.path.exists(PATH):
			print '=====dir %s create success.' %PATH
		if os.path.exists((os.sep).join([PATH,'XINCBAK'])):
			print  (os.sep).join([PATH,'XINCBAK']) +' is already exist.====='
			
	ftpcfgFile(publiccfgPath,view,file)
	ftpcfgFile(publiccfgPath,'pybuildScripts',file2)
	#shutil.copy(os.getcwd()+'/'+file,PATH+'/'+ file)
	#movefile(os.getcwd()+'/'+file,PATH)
	movefile((os.sep).join([os.getcwd(),file]),(os.sep).join([PATH,file]))
	movefile((os.sep).join([os.getcwd(),file2]),(os.sep).join([PATH,file2]))

def labelAnalyze(view,ostype,PATH,label):
	global tsysview,listLabel,buildType,covType,componentDirList,componentDir,moduleName,subLabel ,componentName,stTestItDir
	
	if not '/' in label:
		listLabel=label.split('_')
		tsysview=listLabel[0]
		if view in dict_prj:
			if listLabel[0] != dict_prj[view]: 
				print '=====The label %s does not match with the project %s' %(label,dict_prj[view])
				sys.exit(1)
		else:
			#ϵͳ��ͼ������ǩ
			if listLabel[0] in sysviews :pass
			else:
				if listLabel[0] != view:
					print '!!!!!The label %s does not match with the project %s' %(label,view)
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

		
		
def checkoutfile(PATH,view,label,user):
	global bool_ci
	flag_xinc=0
	print 'Starteam project:%s' %stHome
	os.environ.update({'LANG':'zh_CN.GB18030'})
	if '/' in label:
		print '=====you are running check out files from other MODULES... --->'+stSrcDir+label
		tModulelist=re.sub(r'\s+',',',modulelist)
		for module in tModulelist.split(','):
			if label == '/'+module+'/xinc':
				flag_xinc=1
				if user in userlist:
					cmd='%s co -p %s/%s%s" -fp %s/XINCBAK%s -x -o -nologo -is' %(STCMD,newStHome,stSrcDir,label,PATH,label)
					rtn=sys_cmd(cmd)
					if rtn !=0:
						print 'the current path must begin with "/",eg: if you want to check out file CE4A_if.h you should like this ---> /EN/xinc'
						sys.exit(-1)
				else:
					print 'new rule : no permission to check out files from '+label+' contact '+ userlist
					sys.exit(-1)
			else:pass
		if flag_xinc==0:
			cmd='%s co -p %s/%s%s" -fp %s/%s%s -x -o -nologo -is' %(STCMD,newStHome,stSrcDir,label,PATH,stSrcDir,label)
			rtn=sys_cmd(cmd)
			print 'rtn='+str(rtn)
			if rtn !=0:
				print 'the current path must begin with "/",eg: if you want to check out file CE4T_if.h you should like this ---> /CE/com/ext/inc'
				sys.exit(-1)
		sys.exit()
	else:
		if "True"==bigModule:
			print '=====baking '+moduleName+'/xinc... to '+ (os.sep).join([PATH,'XINCBAK'])
			if os.path.exists((os.sep).join([PATH,'XINCBAK',moduleName,'xinc'])):
				#shutil.rmtree((os.sep).join([PATH,stSrcDir,'xincbak']));
				print '1====='+(os.sep).join([PATH,'XINCBAK',moduleName,'xinc']) +' exists...'
			else:
				print '=====Checking out %s/xinc' %moduleName #Դ�ļ����Ѱ���TEST ���
				if buildType=="MODULE":
					cmd='%s co -p %s/%s/%s/xinc" -fp  %s/XINCBAK/%s/xinc -filter "MGIOU"  -x -o -nologo -is -vl "%s"' %(STCMD,newStHome,stSrcDir,moduleName,PATH,moduleName,label)
					sys_cmd(cmd)
				if buildType=="COMPONENT":
					cmd='%s co -p %s/%s/%s/xinc" -fp  %s/XINCBAK/%s/xinc -filter "MGIOU"  -x -o -nologo -is ' %(STCMD,newStHome,stSrcDir,moduleName,PATH,moduleName)
					sys_cmd(cmd)

		print "��ɾ����̨Ŀ¼�ļ� "+PATH+'/'+stSrcDir+'/'+componentDir+",������check out files..."
		#ֻ��ɾ�����ļ���
		#os.rmdir(PATH+'/'+stSrcDir+'/'+componentDir)
		print (os.sep).join([PATH,stSrcDir,componentDir]) #PATH+'/'+stSrcDir+'/'+componentDir
		if os.path.exists(PATH+'/'+stSrcDir+'/'+componentDir):
			shutil.rmtree((os.sep).join([PATH,stSrcDir,componentDir]))

		if buildType == "SYS":
			print '=====this is a SWS build , Checking out %s/' %stSrcDir
			cmd='%s co -p %s/%s/%s" -fp  %s/%s/%s -filter "MGIOU"  -x -o -nologo -is -vl "%s"' %(STCMD,newStHome,stSrcDir,componentDir,PATH,stSrcDir,componentDir,label)
			sys_cmd(cmd)
			'''
			for dir in os.listdir((os.sep).join([ PATH,stSrcDir])):
				if os.path.isdir(dir):
					if dir != "export" or dir != "export_t":
						print '===== checking dir %s has the label.c ?' %dir
						if not  os.path.exists(dir/label.c):
							print '===== %s/label.c not exist in ST .Before SYS build, The Module %s Not Compiled.' %(dir,dir)
							return -1
				else: pass
			'''
		else:
			print '=====checking out Project_config, Makefile,Makefile55...'
			cmd='%s co -p %s/%s"   -fp  %s/%s -filter "MOIGU"  -x -o -nologo Project_config Makefile Makefile55' %(STCMD,newStHome,stSrcDir,PATH,stSrcDir)
			sys_cmd(cmd)
			print '=====Checking out %s' %componentDir #Դ�ļ����Ѱ���TEST ���
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
				if "True"==bigModule:
					print '=====Checking out %s'%stEXPORTDir
					cmd='%s delete-local -p %s/%s/%s"  -fp %s/%s/%s -filter "N" -x -nologo' %(STCMD,newStHome,stSrcDir,stEXPORTDir,PATH,stSrcDir,stEXPORTDir)
					sys_cmd(cmd)
					cmd='%s co           -p %s/%s/%s"  -fp %s/%s/%s -filter "MGIOU" -x -o -nologo' %(STCMD,newStHome,stSrcDir,stEXPORTDir,PATH,stSrcDir,stEXPORTDir)
					sys_cmd(cmd)
					print '=====xincbak--->xinc'
					if os.path.exists((os.sep).join([PATH,stSrcDir,moduleName,'xinc'])):
						shutil.rmtree((os.sep).join([PATH,stSrcDir,moduleName,'xinc']))
					try:
						shutil.copytree((os.sep).join([PATH,'XINCBAK',moduleName,'xinc']),(os.sep).join([PATH,stSrcDir,moduleName,'xinc']));
					except BaseException,e:
						print '2=====shutil.copytree'
						print `e`

				else:
					print 'bigModule=False, check out SRC/xinc...'
					cmd='%s delete-local -p %s/%s/xinc" -fp %s/%s/xinc -filter "N" -x -nologo' %(STCMD,newStHome,stSrcDir,PATH,stSrcDir)
					sys_cmd(cmd)
					cmd='%s co           -p %s/%s/xinc" -fp %s/%s/xinc -filter "MGIOU" -x -o -nologo' %(STCMD,newStHome,stSrcDir,PATH,stSrcDir)
					sys_cmd(cmd)
		'''
		if ViewType !='DevelopView':
			cmd='%s local-mkdir -p %s/SIT/DB" -fp %s/SIT/DB  -is' %(STCMD,newStHome,PATH)
			rtn2=sys_cmd(cmd)
			cmd='%s local-mkdir -p %s/SIT/config" -fp %s/SIT/config  -is' %(STCMD,newStHome,PATH)
			rtn4=sys_cmd(cmd)
			if rtn2 !=0  or rtn4 !=0 :
				print '__________________________________________________________________'
				print '| =====Warnning : the dir rule is NOT accord with SMEE ST		|'
				print '|--->connect to [wangq] if the project belong to 200 series.		|'
				print '|--->connect to [jiangjh] if the project belong to other series.	|'
				print '|________________________________________________________________|'
				ftpDir((os.sep).join([PATH,stSrcDir]),'/home/publiccfg/BuildCfg/common/templete301C_2.7')
				bool_ci=False
			else:
				ftpDir((os.sep).join([PATH,stSrcDir]),'/home/publiccfg/BuildCfg/common/templeteCMDBConfig')
				bool_ci=True
		else:
			ftpDir((os.sep).join([PATH,stSrcDir]),'/home/publiccfg/BuildCfg/common/templete301C_2.7')
			bool_ci=False
		'''
	ftpDir((os.sep).join([PATH,stSrcDir]),'/home/publiccfg/BuildCfg/common/templete301C_2.7')
	bool_ci=False
	# 012500 Ҫ������pdb��׺�Ĵ�����ļ���
	if 012500==view:
		cmd='%s co -p %s/%s" -fp  %s/%s" -filter "MOIGU"  -x -nologo -o "Makefile_tpl_win"' %(STCMD,newStHome,stSrcDir,PATH,stSrcDir)
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
	os.environ.update({'LANG':'zh_CN.GB18030'})
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
	print '====='+makePath
	os.chdir(makePath) #!!!
	print '=====current dir=%s' %os.getcwd()
		
	if 1==vwBuild:
		print(' -----��ʼ����Vxworks...-----')
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
		print(' -----��ʼ����CCS...-----')
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
		print(' -----��ʼ����Windows...')
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
	global bool_ci
	print '=====checkinfile====='
	os.environ.update({'LANG':'zh_CN.GB18030'})
	print '====='+ostype
	os.chdir(PATH)
	if 'LINUX' in ostype.upper() or 'SUNOS' in ostype.upper():
		if "TEST" != buildType:
			################################################
			cmd='%s ci  -p %s/%s" -fp %s/%s -is -vl "%s" -r "%s:%s" -filter "M" -nologo' %(STCMD,newStHome,stLibSunDir,PATH,stLibSunDir,label,userName,label)
			sys_cmd(cmd)
			cmd='%s add -p %s/%s" -fp %s/%s -is -d "%s:%s" -vl "%s" -nologo' %(STCMD,newStHome,stLibSunDir,PATH,stLibSunDir,userName,label,label)
			sys_cmd(cmd)
			cmd='%s ci  -p %s/%s" -fp %s/%s -is -vl "%s" -r "%s:%s" -filter "M" -nologo' %(STCMD,newStHome,stBinSunDir,PATH,stBinSunDir,label,userName,label)
			sys_cmd(cmd)
			cmd='%s add -p %s/%s" -fp %s/%s -is -d "%s:%s" -vl "%s" -nologo' %(STCMD,newStHome,stBinSunDir,PATH,stBinSunDir,userName,label,label)
			sys_cmd(cmd)
			########################## DB Config ######################
			
			dirlist=['SIT/DB/ImportData','SIT/config']
			for i in range(len(dirlist)):
				if os.path.exists((os.sep).join([ PATH,dirlist[i]])):pass
				else:
					bool_ci=False
			print '=====bool_ci='+str(bool_ci)
			if bool_ci:
				for i in range(len(dirlist)):
					lineList=[]
					cmd='%s update-status -p %s/%s" -fp %s/%s  -is   -nologo' %(STCMD,newStHome,dirlist[i],PATH,dirlist[i])
					cmd='%s list -p %s/%s" -fp %s/%s  -is   -nologo -filter "MNU">%s/temp.txt' %(STCMD,newStHome,dirlist[i],PATH,dirlist[i],PATH)
					sys_cmd(cmd)
					cmd='%s list -p %s/%s" -fp %s/%s  -is   -nologo -filter "MNU"' %(STCMD,newStHome,dirlist[i],PATH,dirlist[i])
					sys_cmd(cmd)
					
					fout=open('temp.txt','r')
					while True:
						line=fout.readline()
						if not line:
							break
						lineList= line.split(' ')
						print lineList
						if "Not" == lineList[0]:
							cmd='%s add -p  %s/%s" -fp %s/%s -is  -vl "%s"  -d "%s:%s"  -nologo -q %s'  %(STCMD,newStHome,dirlist[i],PATH,dirlist[i],label,userName,moduleName,lineList[-1].replace('\n', ''))
							sys_cmd(cmd)
							cmd='%s ci  -p  %s/%s" -fp %s/%s -is  -vl "%s"  -o -r "%s:%s"  -nologo -q %s' %(STCMD,newStHome,dirlist[i],PATH,dirlist[i],label,userName,moduleName,lineList[-1].replace('\n', ''))
							sys_cmd(cmd)
						if "Modified" == lineList[0]:
							cmd='%s add -p  %s/%s" -fp %s/%s -is  -vl "%s"  -d "%s:%s"  -nologo -q %s'  %(STCMD,newStHome,dirlist[i],PATH,dirlist[i],label,userName,moduleName,lineList[-1].replace('\n', ''))
							sys_cmd(cmd)
							cmd='%s ci  -p  %s/%s" -fp %s/%s -is  -vl "%s"  -o -r "%s:%s"  -nologo -q %s' %(STCMD,newStHome,dirlist[i],PATH,dirlist[i],label,userName,moduleName,lineList[-1].replace('\n', ''))
							sys_cmd(cmd)
						if "Unknown" == lineList[0]:
							cmd='%s add -p  %s/%s" -fp %s/%s -is  -vl "%s"  -d "%s:%s"  -nologo -q %s'  %(STCMD,newStHome,dirlist[i],PATH,dirlist[i],label,userName,moduleName,lineList[-1].replace('\n', ''))
							sys_cmd(cmd)
							cmd='%s ci  -p  %s/%s" -fp %s/%s -is  -vl "%s"  -o -r "%s:%s"  -nologo -q %s' %(STCMD,newStHome,dirlist[i],PATH,dirlist[i],label,userName,moduleName,lineList[-1].replace('\n', ''))
							sys_cmd(cmd)
				print '=====delete temp file temp.txt'
				os.system('rm -rf %s/temp.txt' %(PATH))
			
			if "SYS" != buildType:
				print "=====check in label.c to ST..."
				cmd='%s add -p %s/%s/%s" -fp %s/%s/%s -d "%s:%s" -vl "%s" -nologo  label.c' %(STCMD,newStHome,stSrcDir,moduleName,PATH,stSrcDir,moduleName,userName,label,label)
				sys_cmd(cmd)
				cmd='%s ci  -p %s/%s/%s" -fp %s/%s/%s -o -vl "%s" -r "%s:%s" -nologo  label.c' %(STCMD,newStHome,stSrcDir,moduleName,PATH,stSrcDir,moduleName,label,userName,label)
				sys_cmd(cmd)
		else:
			cmd='%s ci  -p %s/%s" -fp %s/%s -is -vl "%s" -r "%s:%s" -filter "M" -nologo' %(STCMD,newStHome,stTestItDir,PATH,stTestItDir,label,userName,label)
			sys_cmd(cmd)
			cmd='%s add -p %s/%s" -fp %s/%s -is -d "%s:%s" -vl "%s" -nologo' %(STCMD,newStHome,stTestItDir,PATH,stTestItDir,userName,label,label)
			sys_cmd(cmd)
	else:
		if "TEST" != buildType:
			if vwBuild==1:
				cmd='%s ci  -p %s/%s" -fp %s/%s -is -vl "%s" -r "%s %s" -filter "M" -nologo' %(STCMD,newStHome,stBinVwDir,PATH,stBinVwDir,label,userName,label)
				sys_cmd(cmd)
				cmd='%s add -p %s/%s" -fp %s/%s -is  -vl "%s" -nologo' %(STCMD,newStHome,stBinVwDir,PATH,stBinVwDir,label)
				sys_cmd(cmd)
			if fwBuild==1:
				cmd='%s ci  -p %s/%s" -fp %s/%s -is -vl "%s" -r "%s %s" -filter "M" -nologo' %(STCMD,newStHome,stBinFwDir,PATH,stBinFwDir,label,userName,label)
				sys_cmd(cmd)
				cmd='%s add -p %s/%s" -fp %s/%s -is  -vl "%s" -nologo' %(STCMD,newStHome,stBinFwDir,PATH,stBinFwDir,label)
				sys_cmd(cmd)
			if winBuild==1:
				cmd='%s ci -p %s/%s" -fp %s/%s -vl "%s" -r "%s %s" -filter "M" -nologo -is' %(STCMD,newStHome,stBinWinDir,PATH,stBinWinDir,label,userName,label)
				sys_cmd(cmd)
				cmd='%s add -p %s/%s" -fp %s/%s  -vl "%s" -nologo -is' %(STCMD,newStHome,stBinWinDir,PATH,stBinWinDir,label)
				sys_cmd(cmd)
				cmd='%s ci -p %s/%s" -fp %s/%s -vl "%s" -r "%s %s" -filter "M" -nologo -is' %(STCMD,newStHome,stLibWinDir,PATH,stLibWinDir,label,userName,label)
				sys_cmd(cmd)
				cmd='%s add -p %s/%s" -fp %s/%s  -vl "%s" -nologo -is' %(STCMD,newStHome,stLibWinDir,PATH,stLibWinDir,label)
				sys_cmd(cmd)
		else:
			cmd='%s ci  -p %s/%s" -fp %s/%s -is -vl "%s" -r "%s:%s" -filter "M" -nologo' %(STCMD,newStHome,stTestItDir,PATH,stTestItDir,label,userName,label)
			sys_cmd(cmd)
			cmd='%s add -p %s/%s" -fp %s/%s -is -d "%s:%s" -vl "%s" -nologo' %(STCMD,newStHome,stTestItDir,PATH,stTestItDir,userName,label,label)
			sys_cmd(cmd)
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
	
def readConfigFile(PATH,view):
	print "run readConfigFile"
	global bigModule,stUserName,stPasswd,stHome,stCmdSun,stCmdWin,stSrcDir,stBinSunDir,stLibSunDir,stBinVwDir,stBinFwDir,stBinWinDir,stLibWinDir,stBinWinDir64,stLibWinDir64,stTestItDir,stEXPORTDir,stTestEXPORT,vxworks,ccs,VS,VS64,winQT,projectDir,modulelist,it_prj_list
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
		print " stUserName=%s\n stPasswd=%s\n  stCmdSun=%s\n stCmdWin=%s\n stSrcDir=%s\n stBinSunDir=%s\n stLibSunDir=%s\n stBinLinuxDir=%s\n stBinLinuxDir=%s\n stBinVwDir=%s\n stBinFwDir=%s\n stBinWinDir=%s\n stLibWinDir=%s\n stBinWinDir64=%s\n stLibWinDir64=%s\n stTestItDir=%s\n stEXPORTDir=%s\n stTestEXPORT=%s\n vxworks=%s\n ccs=%s\n VS=%s\n VS64=%s\n winQT=%s\n bigModule=%s\n modulelist=%s\n stHome=%s\n" \
			%(stUserName,stPasswd,stCmdSun,stCmdWin,stSrcDir,stBinSunDir,stLibSunDir,stBinLinuxDir,stBinLinuxDir,stBinVwDir,stBinFwDir,stBinWinDir,stLibWinDir,stBinWinDir64,stLibWinDir64,stTestItDir,stEXPORTDir,stTestEXPORT,vxworks,ccs,VS,VS64,winQT,bigModule,modulelist,stHome)
		print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
		# ����λ���������ã������ж�·����os.getcwd() �滻LOCAL_DIR
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
	tview=""
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
	#�л�Զ��Ŀ¼
	try:
		if '301C' in view or '205C' in view :
			tview=view.replace('\\','/')
			print 'change dir to '+('/').join([publiccfgPath,tview])
			ftp.cwd(('/').join([publiccfgPath,tview]))
		else:
			print 'change dir to '+('/').join([publiccfgPath,view])
			ftp.cwd(('/').join([publiccfgPath,view]))
	except BaseException,e:
		print `e`
		print 'No dir in /home/publiccfg/BuildCfg/'+view+' ,please create dir '+view+' in /home/publiccfg/BuildCfg/     [172.16.42.76/publiccfg/(x86x86)]'
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
	#�л�Զ��Ŀ¼
	ftp.cwd(remotePath)
	subItems=ftp.nlst(remotePath) #��ȡĿ¼�µ��ļ�
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
	else:
		os.mkdir(drive+'\BuildScript')
		if os.path.exists(drive+'\BuildScript'):
			ftpDir(drive+'\BuildScript','/home/publiccfg/BuildCfg/BuildScript')
		else:
			print "=====BuildScript is not exist..."
			sys.exit(1)
def rmlabel(PATH,stSrcDir):
	cmd='%s/%s/label.c' %(PATH,stSrcDir)
	if os.path.exists(cmd):
		os.remove(cmd)

def biji(drive,view):
	print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
	print '_____________________________________________________________'
	print '|				|DevelopView	|MachineView	|	SysView	|'
	print '|CompunentBuild	|	yes			|	no			|	no		|'
	print '|ModuleBuild		|	yes			|	yes			|	yes		|'
	print '|SysBuild		|	no			|	yes			|	yes		|'
	print '|____________________________________________________________|'
	print 'the file updatepyqb.py exist in ---> '+drive
	print  view+'/src/Project_config in ST you must make sure :\n '
	print 'SUN_DIR = $(HOME)/'+view
	print 'QT_DIR  = $$(HOME)/'+view
	print 'LOCAL_DIR=$(HOME)/'+view
	print 'only check out makefile,project_config from ST every time !!!'
	print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
	print '301,203M,205--->the compile script themself...'
if __name__ == "__main__":
	view=""
	label=""
	user=""
	passwd=""
	#sys.argv[0] �ű�����sys.argv[1] ��һ������
	print "=====len(sys.argv)=%d" %len(sys.argv)
	if len(sys.argv)==5:
		view=sys.argv[1]
		label=sys.argv[2]
		user=sys.argv[3]
		passwd=sys.argv[4]
		#ViewType=sys.argv[5]
		print "view=%s\n label=%s\n user=%s\n passwd=%s\n" %(view,label,user,passwd)
	else:
		print "argv num is error... [view,label,user,passwd]"
		sys.exit(1)
	system=platform.system()
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
	readConfigFile(PATH,view)
	globalVariables(system.upper())
	labelAnalyze(view,system,PATH,label)
	checkoutfile(PATH,view,label,user)
	rmlabel(PATH,stSrcDir)
	stringslabel(PATH)
	if 'LINUX' in system.upper() or 'SUNOS' in system.upper():
		rtn=executeMakeUnix(PATH)
		print '=====rtn='+str(rtn)
		if rtn != -1:
			checkinfile(PATH,system,label,user)
	else:
		renameVW(PATH)
		verify_BuildScript(drive)
		lowerPCbuild(PATH)
		rtn=executeMakeWin(drive,PATH)
		print '=====rtn='+str(rtn)
		if rtn !=-1:
			checkinfile(PATH,system,label,user)
	print '=====update file baseqbbuild.py to '+drive
	os.chdir(drive) #!!!
	ftpcfgFile('/home/publiccfg/BuildCfg/','pybuildScripts','baseqbbuild.py')
	
	biji(drive,view)
	time.sleep(2)
	os._exit(0)