#!/bin/bash

ftp -n<<!
open 172.16.42.76
user publiccfg x86x86
binary
prompt
cd BuildCfg/gtScripts
get gtbuild.sh
get prjconfig.cfg
close
by
!

chmod +x gtbuild.sh
echo $@
echo "step1====================="
#传递所有参数
bash ./gtbuild.sh $@

if [ $? != 0 ];then
	exit 1
fi



