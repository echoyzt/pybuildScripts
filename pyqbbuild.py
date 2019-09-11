#_*_ coding:utf-8 _*_
import sys,os,shutil,re,time
import ConfigParser
import platform
import ftplib,socket
#python pyqbbuild.py 008A L_008A_EN_CE_BUILD_0.1.25_20190214 yuzt yuzt021zsh DevelopView 
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
dict_prj={'50417':'208005','50417_02':'205003','018manufacture2':'018','504-4.5G_src':'504','SSB500_10M':'203M','SSB500_30':'205','SSB500_25P':'509','SSB545_10':'206','S21-17':'007'}
# SIT/bin/fireware, 是默认的规范路径，逻辑分支如下
#prj----|------SIT
#		|		|---fireware
#		|		|---Dfirmware
#		|
#		|-------IT
#		|		|---fireware
#				|---Dfirmware
it_prj_list='018,018manufacture2,018A,00614,EE16,EE3,404001,404002,404003,404004'
SIT_dfirmware='613001,613002,006A,613003'
IT_dfirmware='00614,EE16,EE3,404001,404002,404003,404004'

userlist='yanw,chencl,zhaozilong,yuech,lujt,yul,zhangwm,yuzt'
sysviews='301C,205C'
win64_prj='012500,012600,012B,012C,012D,012E,701001,701002,701003,701004,701005,701006,701007,701FFF'
#'配置管理真他妈的随意，混乱，狗屎。。。'
#1.需求:项目名称和标签中的一致,dict_prj 中的没有做到一致
#2.需求:项目产品目录SIT, 实际有SIT,IT,firmware,Dfirmware，windows64,windows-64,windows_64...
#3.vs 有32,64 版本，在win64 服务器上编译32 位版本库，记得正确的版本。
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
	#file='newbuild.cfg'
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
			
	#ftpcfgFile(publiccfgPath,view,file)
	ftpcfgFile(publiccfgPath,'pybuildScripts',file2)

	#movefile((os.sep).join([os.getcwd(),file]),(os.sep).join([PATH,file]))
	movefile((os.sep).join([os.getcwd(),file2]),(os.sep).join([PATH,file2]))

def labelAnalyze(view,ViewType,ostype,PATH,label):
	global tsysview,listLabel,buildType,covType,componentDirList,componentDir,moduleName,subLabel ,componentName,stTestItDir
	
	if not '/' in label:
		listLabel=label.split('_')
		tsysview=listLabel[1]
		if view in dict_prj:
			if listLabel[1] != dict_prj[view]: 
				print '=====The label %s does not match with the project %s' %(label,dict_prj[view])
				sys.exit(1)
		else:
			#系统视图不检查标签
			if listLabel[1] in sysviews :pass
			else:
				if listLabel[1] != view:
					print '!!!!!The label %s does not match with the project %s' %(label,view)
					sys.exit(1)
		print '=====listLabel=%s' %listLabel
		num=len(listLabel)
		if 'BUILD' in label and 'TEST' not in label:
			listLabel.remove('BUILD')
			del listLabel[0]
			#listLabel.remove('L')
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
					del listLabel[0]
					#listLabel.remove('L')
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
					print ('=====this is a SYS build,the label is invalide.')
					sys.exit(1)
			else:
				moduleName=listLabel[1]
				componentDirList=listLabel[1:-2]
				if 1==len(listLabel[1:-2]):
					buildType='MODULE'
				else:
					buildType='COMPONENT'
					print '=====Error becase This is a SysView, so Can not component build!!!.'
					sys.exit(1)
				covType='CC'
		else: #机台视图
			if 'SWS' in label:
				if (6==num):
					buildType='SYS'
					componentDirList=[""]
					covType='SYS'
				else:
					print ('=====this is SYS build,the label is invalide.')
					sys.exit(1)
			else:
				moduleName=listLabel[1]
				componentDirList=listLabel[1:-2]
				if 1==len(listLabel[1:-2]):
					buildType='MODULE'
				else:
					buildType='COMPONENT'
					print '=====Error because This is MachineView, so Can not component build!!!.'
					sys.exit(1)
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
		
		
def checkoutfile(PATH,view,label,user,passwd):
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
					cmd='%s delete-local -p %s:"%s@%s/%s%s" -fp %s/XINCBAK%s -filter "N" -x -nologo' %(STCMD,user,passwd,stHome,stSrcDir,label,PATH,label)
					sys_cmd(cmd)
					cmd='%s co -p %s:"%s@%s/%s%s" -fp %s/XINCBAK%s -x -o -nologo -is' %(STCMD,user,passwd,stHome,stSrcDir,label,PATH,label)
					rtn=sys_cmd(cmd)
					
					cmd='%s delete-local -p %s:"%s@%s/%s%s" -fp %s/%s/%s/xinc -filter "N" -x -nologo' %(STCMD,user,passwd,stHome,stSrcDir,label,PATH,stSrcDir,module)
					sys_cmd(cmd)
					cmd='%s co -p %s:"%s@%s/%s%s" -fp %s/%s/%s/xinc -x -o -nologo -is' %(STCMD,user,passwd,stHome,stSrcDir,label,PATH,stSrcDir,module)
					rtn=sys_cmd(cmd)
					
					if rtn !=0:
						print '______________________________________________________________________________'
						print 'check you password first .'
						print 'the current path must begin with "/".'
						print 'eg: if you want to check out file CE4A_if.h you should like this ---> /EN/xinc'
						print '_______________________________________________________________________________'
						sys.exit(-1)
				else:
					print '______________________________________________________________________________'
					print 'new rule : no permission to check out files from '+label+' contact '+ userlist
					print '______________________________________________________________________________'
					sys.exit(-1)
			else:
				print '_________________________________________________'
				print '1.check if ST has the dir '+label
				print '2.check if the file  newbuild.cfg has the module '
				print '-------------------------------------------------'
		if flag_xinc==0:
			cmd='%s co -p %s/%s%s" -fp %s/%s%s -x -o -nologo -is' %(STCMD,newStHome,stSrcDir,label,PATH,stSrcDir,label)
			rtn=sys_cmd(cmd)
			print 'rtn='+str(rtn)
			if rtn !=0:
				print 'the current path must begin with "/",eg: if you want to check out file CE4T_if.h you should like this ---> /CE/com/ext/inc'
				sys.exit(-1)
		sys.exit()
	else:
		print "先删除后台目录文件 "+PATH+'/'+stSrcDir+'/'+componentDir+",再重新check out files..."
		#只能删除空文件夹
		#os.rmdir(PATH+'/'+stSrcDir+'/'+componentDir)
		print '====='+(os.sep).join([PATH,stSrcDir,componentDir]) 
		if os.path.exists((os.sep).join([PATH,stSrcDir,componentDir])):
			print 'delete dir '+ (os.sep).join([PATH,stSrcDir,componentDir])
			shutil.rmtree((os.sep).join([PATH,stSrcDir,componentDir]))

		if buildType == "SYS":
			os.mkdir((os.sep).join([PATH,stSrcDir]))
			if ViewType !='DevelopView':
				print '=====this is a SWS build , Checking out %s/' %stSrcDir
				cmd='%s co -p %s/%s/%s" -fp  %s/%s/%s -filter "MGIOU"  -x -o -nologo -is -vl "%s"' %(STCMD,newStHome,stSrcDir,componentDir,PATH,stSrcDir,componentDir,label)
				sys_cmd(cmd)
				
				cmd='%s local-mkdir -p %s/SIT/DB/ImportData" -fp %s/SIT/DB/ImportData  -is' %(STCMD,newStHome,PATH)
				rtn5=sys_cmd(cmd)
				cmd='%s local-mkdir -p %s/SIT/config" -fp %s/SIT/config  -is' %(STCMD,newStHome,PATH)
				rtn6=sys_cmd(cmd)
				if rtn5 !=0  or rtn6 !=0 :
					print '__________________________________________________________________'
					print '| =====Warnning : the dir rule is NOT accord with SMEE ST		|'
					print '|--->connect to [wangq] if the project belong to 200 series.		|'
					print '|--->connect to [jiangjh] if the project belong to other series.	|'
					print '|________________________________________________________________|'
					ftpDir((os.sep).join([PATH,stSrcDir]),'/home/publiccfg/BuildCfg/common/templete301C_2.7')
					bool_ci=False
				else:
					print '=====delete dir '+ (os.sep).join([PATH,'SIT','DB','ImportData'])+','+(os.sep).join([PATH,'SIT','config'])
					if os.path.exists((os.sep).join([PATH,'SIT','DB','ImportData'])):
						shutil.rmtree((os.sep).join([PATH,'SIT','DB','ImportData']))
					if os.path.exists((os.sep).join([PATH,'SIT','config'])):
						shutil.rmtree((os.sep).join([PATH,'SIT','config']))
					ftpDir((os.sep).join([PATH,stSrcDir]),'/home/publiccfg/BuildCfg/common/templeteCMDBConfig')
					bool_ci=True

			print "sys=====sys=====sys"
			print (os.sep).join([PATH,stSrcDir])
			for dir in os.listdir((os.sep).join([PATH,stSrcDir])):
				print '-----'+dir
				if os.path.isdir((os.sep).join([PATH,stSrcDir,dir])):
					if (dir != "export") and (dir != "export_t"):
						print '===== checking dir %s has the label.c ?' %dir
						if not  os.path.exists((os.sep).join([PATH,stSrcDir,dir,'label.c'])): 
							print '===== %s/label.c not exist in ST .Before SYS build, The Module %s Not Compiled.' %(dir,dir)
							sys.exit(-1)
						else:
							print '===== %s has the label.c'  %dir
							if os.path.exists((os.sep).join([PATH,stSrcDir,dir,dir+'_label.c'])): 
								os.remove((os.sep).join([PATH,stSrcDir,dir,dir+'_label.c']))
				else:
					print '-----'+dir+' is file...'
			print "sys=====sys=====sys"
			
		else:
			print '=====checking out Project_config, Makefile...'
			cmd='%s co -p %s/%s"   -fp  %s/%s -filter "MOIGU"  -x -o -nologo Project_config Makefile' %(STCMD,newStHome,stSrcDir,PATH,stSrcDir)
			sys_cmd(cmd)
			print '=====Checking out %s' %componentDir #源文件，已包含TEST 情况
			cmd='%s co -p %s/%s/%s" -fp  %s/%s/%s -filter "MGIOU"  -x -o -nologo -is -vl "%s"' %(STCMD,newStHome,stSrcDir,componentDir,PATH,stSrcDir,componentDir,label)
			sys_cmd(cmd)
			
			if "True"==bigModule:
				print '=====baking '+moduleName+'/xinc---> '+ (os.sep).join([PATH,'XINCBAK'])
				if os.path.exists((os.sep).join([PATH,'XINCBAK',moduleName,'xinc'])):
					#shutil.rmtree((os.sep).join([PATH,stSrcDir,'xincbak']));
					print '1====='+(os.sep).join([PATH,'XINCBAK',moduleName,'xinc']) +' exists...'
				else:
					print '=====Checking out %s/xinc' %moduleName #源文件，已包含TEST 情况
					if buildType=="MODULE":
						cmd='%s co -p %s/%s/%s/xinc" -fp  %s/XINCBAK/%s/xinc -filter "MGIOU"  -x -o -nologo -is -vl "%s"' %(STCMD,newStHome,stSrcDir,moduleName,PATH,moduleName,label)
						sys_cmd(cmd)
					if buildType=="COMPONENT":
						cmd='%s co -p %s/%s/%s/xinc" -fp  %s/XINCBAK/%s/xinc -filter "MGIOU"  -x -o -nologo -is ' %(STCMD,newStHome,stSrcDir,moduleName,PATH,moduleName)
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
						if os.path.exists((os.sep).join([PATH,'XINCBAK',moduleName,'xinc'])):
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
					print '=====delete dir '+ (os.sep).join([PATH,'SIT','DB','ImportData'])+','+(os.sep).join([PATH,'SIT','config'])
					if os.path.exists((os.sep).join([PATH,'SIT','DB','ImportData'])):
						shutil.rmtree((os.sep).join([PATH,'SIT','DB','ImportData']))
					if os.path.exists((os.sep).join([PATH,'SIT','config'])):
						shutil.rmtree((os.sep).join([PATH,'SIT','config']))
					ftpDir((os.sep).join([PATH,stSrcDir]),'/home/publiccfg/BuildCfg/common/templeteCMDBConfig')
					bool_ci=True
			else:
				ftpDir((os.sep).join([PATH,stSrcDir]),'/home/publiccfg/BuildCfg/common/templete301C_2.7')
				bool_ci=False
			
	# 012500 要求生成pdb后缀的代码库文件。
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
	rtn = 1
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
				cmd=cmd1+ ' && make  -f Makefile55 || (rtn=-1 && goto End)'
				sys_cmd(cmd)
			else:
				cmd=cmd1+' && make MM=%s || (rtn=-1 && goto End)' %(moduleName)
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
				cmd=cmd1+' && gmake -f Makefile55 || (rtn=-1 && goto End)'
				sys_cmd(cmd)
			else :
				cmd=cmd1+' && gmake MM=%s || (rtn=-1 && goto End)' %(moduleName)
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
				cmd=cmd1+' && qmake && nmake MM=%s all || (rtn=-1 && goto End)' %(moduleName)
				sys_cmd(cmd)
			else :
				print( "-----run Makefile_win...")
				cmd=cmd1+' && nmake MM=%s /f Makefile_win || (rtn=-1 && goto End)' %(moduleName)
				sys_cmd(cmd)
		except BaseException,e:
			return -1
	return rtn
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
			rtn=sys_cmd(cmd)
			if rtn !=0:
				print "Memory allocation failed---> ST too busy"
				sys.exit(1)
			cmd='%s add -p %s/%s" -fp %s/%s -is -d "%s:%s" -vl "%s" -nologo' %(STCMD,newStHome,stLibSunDir,PATH,stLibSunDir,userName,label,label)
			sys_cmd(cmd)
			
			cmd='%s ci  -p %s/%s" -fp %s/%s -is -vl "%s" -r "%s:%s" -filter "M" -nologo' %(STCMD,newStHome,stBinSunDir,PATH,stBinSunDir,label,userName,label)
			rtn=sys_cmd(cmd)
			if rtn !=0:
				print "Memory allocation failed---> ST too busy"
				sys.exit(1)
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
					print '+++++++++++++++++++++++update status '+dirlist[i]
					cmd='%s update-status -p %s/%s" -fp %s/%s  -is -nologo' %(STCMD,newStHome,dirlist[i],PATH,dirlist[i])
					sys_cmd(cmd)
					print '++++++++++++++++++++++++++++++++++++++++++++++++++'
					cmd='%s list -p %s/%s" -fp %s/%s  -is   -nologo -filter "CMOUN" >%s/temp.txt' %(STCMD,newStHome,dirlist[i],PATH,dirlist[i],PATH)
					sys_cmd(cmd)
					print '+++++++++++++++++++++++list dir '+dirlist[i]
					cmd='%s list -p %s/%s" -fp %s/%s  -is   -nologo -filter "CMOUN"' %(STCMD,newStHome,dirlist[i],PATH,dirlist[i])
					sys_cmd(cmd)
					print '++++++++++++++++++++++++++++++++++++++++++++++++++'
					fout=open('temp.txt','r')
					while True:
						line=fout.readline()
						if not line:
							break
						lineList= line.split(' ')
						if "Not"==lineList[0] or "Modified"==lineList[0] or "Unknown"==lineList[0] or "Out"==lineList[0]:
							print lineList
							print '--->check in file '+lineList[-1].replace('\n', '')
							cmd='%s add -p  %s/%s" -fp %s/%s -is  -vl "%s"  -d "%s:%s"  -nologo -q %s'  %(STCMD,newStHome,dirlist[i],PATH,dirlist[i],label,userName,moduleName,lineList[-1].replace('\n', ''))
							sys_cmd(cmd)
							cmd='%s ci  -p  %s/%s" -fp %s/%s -is  -vl "%s"  -o -r "%s:%s"  -nologo -q %s' %(STCMD,newStHome,dirlist[i],PATH,dirlist[i],label,userName,moduleName,lineList[-1].replace('\n', ''))
							rtn=sys_cmd(cmd)
							if rtn !=0:
								print "Memory allocation failed---> ST too busy"
								sys.exit(1)
						if "Current"==lineList[0]:
							print lineList
							cmd='%s apply-label  -p  %s/%s" -is -lbl "%s" "%s" ' %(STCMD,newStHome,dirlist[i],label,lineList[-1].replace('\n', ''))
							rtn=sys_cmd(cmd)
							if rtn !=0:
								print "the file %s added the new label %s failed!!!" %(lineList[-1].replace('\n', ''),label)
								sys.exit(1)
				print '=====delete temp file temp.txt'
				os.system('rm -rf %s/temp.txt' %(PATH))
			
			if "SYS" != buildType:
				print "=====check in label.c to ST..."
				cmd='%s add -p %s/%s/%s" -fp %s/%s/%s -d "%s:%s" -vl "%s" -nologo  label.c' %(STCMD,newStHome,stSrcDir,moduleName,PATH,stSrcDir,moduleName,userName,label,label)
				sys_cmd(cmd)
				cmd='%s ci  -p %s/%s/%s" -fp %s/%s/%s -o -vl "%s" -r "%s:%s" -nologo  label.c' %(STCMD,newStHome,stSrcDir,moduleName,PATH,stSrcDir,moduleName,label,userName,label)
				rtn=sys_cmd(cmd)
				if rtn !=0:
					print "Memory allocation failed---> ST too busy"
					sys.exit(1)
		else:
			cmd='%s ci  -p %s/%s" -fp %s/%s -is -vl "%s" -r "%s:%s" -filter "M" -nologo' %(STCMD,newStHome,stTestItDir,PATH,stTestItDir,label,userName,label)
			rtn=sys_cmd(cmd)
			if rtn !=0:
				print "Memory allocation failed---> ST too busy"
				sys.exit(1)
			cmd='%s add -p %s/%s" -fp %s/%s -is -d "%s:%s" -vl "%s" -nologo' %(STCMD,newStHome,stTestItDir,PATH,stTestItDir,userName,label,label)
			sys_cmd(cmd)
	else:
		if "TEST" != buildType:
			if vwBuild==1:
				cmd='%s ci  -p %s/%s" -fp %s/%s -is -vl "%s" -r "%s %s" -filter "M" -nologo' %(STCMD,newStHome,stBinVwDir,PATH,stBinVwDir,label,userName,label)
				rtn=sys_cmd(cmd)
				if rtn !=0:
					print "Memory allocation failed---> ST too busy"
					sys.exit(1)
				cmd='%s add -p %s/%s" -fp %s/%s -is  -vl "%s" -nologo' %(STCMD,newStHome,stBinVwDir,PATH,stBinVwDir,label)
				sys_cmd(cmd)
			if fwBuild==1:
				cmd='%s ci  -p %s/%s" -fp %s/%s -is -vl "%s" -r "%s %s" -filter "M" -nologo' %(STCMD,newStHome,stBinFwDir,PATH,stBinFwDir,label,userName,label)
				rtn=sys_cmd(cmd)
				if rtn !=0:
					print "Memory allocation failed---> ST too busy"
					sys.exit(1)
				cmd='%s add -p %s/%s" -fp %s/%s -is  -vl "%s" -nologo' %(STCMD,newStHome,stBinFwDir,PATH,stBinFwDir,label)
				sys_cmd(cmd)
			if winBuild==1:
				cmd='%s ci -p %s/%s" -fp %s/%s -vl "%s" -r "%s %s" -filter "M" -nologo -is' %(STCMD,newStHome,stBinWinDir,PATH,stBinWinDir,label,userName,label)
				rtn=sys_cmd(cmd)
				if rtn !=0:
					print "Memory allocation failed--->ST is too busy"
					sys.exit(1)
				cmd='%s add -p %s/%s" -fp %s/%s  -vl "%s" -nologo -is' %(STCMD,newStHome,stBinWinDir,PATH,stBinWinDir,label)
				sys_cmd(cmd)
				cmd='%s ci -p %s/%s" -fp %s/%s -vl "%s" -r "%s %s" -filter "M" -nologo -is' %(STCMD,newStHome,stLibWinDir,PATH,stLibWinDir,label,userName,label)
				rtn=sys_cmd(cmd)
				if rtn !=0:
					print "Memory allocation failed--->ST is too busy"
					sys.exit(1)
				cmd='%s add -p %s/%s" -fp %s/%s  -vl "%s" -nologo -is' %(STCMD,newStHome,stLibWinDir,PATH,stLibWinDir,label)
				sys_cmd(cmd)
		else:
			cmd='%s ci  -p %s/%s" -fp %s/%s -is -vl "%s" -r "%s:%s" -filter "M" -nologo' %(STCMD,newStHome,stTestItDir,PATH,stTestItDir,label,userName,label)
			rtn=sys_cmd(cmd)
			if rtn !=0:
				print "Memory allocation failed--->ST is too busy... wait...wait...wait..."
				sys.exit(1)
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
	global bigModule,stUserName,stPasswd,stHome,stCmdSun,stCmdWin,stSrcDir,stBinSunDir,stLibSunDir,stBinVwDir,stBinFwDir,stBinWinDir,stLibWinDir,stBinWinDir64,stLibWinDir64,stTestItDir,stEXPORTDir,stTestEXPORT,vxworks,ccs,VS,VS64,winQT,projectDir,modulelist,it_prj_list,IT_dfirmware,SIT_dfirmware
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
			if view in IT_dfirmware:
				stBinFwDir='IT/bin/Dfirmware'
		else:
			if view in SIT_dfirmware:
				stBinFwDir='SIT/bin/Dfirmware'
		
		
		print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
		print " stUserName=%s\n stPasswd=%s\n  stCmdSun=%s\n stCmdWin=%s\n stSrcDir=%s\n stBinSunDir=%s\n stLibSunDir=%s\n stBinLinuxDir=%s\n stBinLinuxDir=%s\n stBinVwDir=%s\n stBinFwDir=%s\n stBinWinDir=%s\n stLibWinDir=%s\n stBinWinDir64=%s\n stLibWinDir64=%s\n stTestItDir=%s\n stEXPORTDir=%s\n stTestEXPORT=%s\n vxworks=%s\n ccs=%s\n VS=%s\n VS64=%s\n winQT=%s\n bigModule=%s\n modulelist=%s\n stHome=%s\n" \
			%(stUserName,stPasswd,stCmdSun,stCmdWin,stSrcDir,stBinSunDir,stLibSunDir,stBinLinuxDir,stBinLinuxDir,stBinVwDir,stBinFwDir,stBinWinDir,stLibWinDir,stBinWinDir64,stLibWinDir64,stTestItDir,stEXPORTDir,stTestEXPORT,vxworks,ccs,VS,VS64,winQT,bigModule,modulelist,stHome)
		print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
		# 上下位机编译配置，无需判断路径，os.getcwd() 替换LOCAL_DIR
		projectDir=PATH
		
	except BaseException,e:
		print `e`
		print 'read file '+scriptPath+', '+scriptPath2 +' failed'
		#os.chdir(drive) #!!!
		ftpcfgFile('/home/publiccfg/BuildCfg','pybuildScripts','updatepyqb.py')
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
			stBinSunDir='IT/bin/sun'
			stLibSunDir='IT/lib/sun'
		else:
			stBinSunDir='SIT/bin/sun'
			stLibSunDir='SIT/lib/sun'

	elif 'WINDOWS32' in ostype:
		#STCMD=stCmdWin
		STCMD="stcmd"
		print 'VS=%s\n' %VS
	else:
		STCMD="stcmd"
		if view in win64_prj:
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
	#切换远程目录
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
	if os.path.exists(cmd):
		os.remove(cmd)

def biji(drive,view):
	print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
	print '1.NEW RULE: must update MODULE files before compile, if files in MODULE modified '
	print '2.Memory allocation failed--->huangwei--->restart ST'
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
	print '301,203M,205,EE14--->the compile script themself...'
if __name__ == "__main__":
	view=""
	label=""
	user=""
	passwd=""
	#sys.argv[0] 脚本名，sys.argv[1] 第一个参数
	print "=====len(sys.argv)=%d" %len(sys.argv)
	if len(sys.argv)==6:
		view=sys.argv[1]
		label=sys.argv[2]
		user=sys.argv[3]
		passwd=sys.argv[4]
		ViewType=sys.argv[5]
		print "view=%s\n label=%s\n user=%s\n passwd=%s\n ViewType=%s\n" %(view,label,user,passwd,ViewType)
	else:
		print "argv num is error... [view,label,user,passwd,ViewType]"
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
	labelAnalyze(view,ViewType,system,PATH,label)
	checkoutfile(PATH,view,label,user,passwd)
	rmlabel(PATH,stSrcDir)
	if buildType != "SYS":
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
	print '=====update file updatepyqb.py to '+drive
	os.chdir(drive) #!!!
	ftpcfgFile('/home/publiccfg/BuildCfg/','pybuildScripts','updatepyqb.py')
	
	biji(drive,view)
	time.sleep(2)
	os._exit(0)