LANG=zh_CN.gb18030
export LANG

project=$1 #20516test
buildType=$2
if [ $buildType = "DevelopBuild" ];then
	if [ $# -ne 6 ];then
		echo "the buildType is DevelopBuild,there is NO FeatureName!!! Try Again"
		exit 1
	fi
	label=$3
	repositoryName=$4
	userName=$5
	userPassword=$6
else 
	echo ----$#
	if [ $# -ne 7 ];then
		echo "the buildType is FeatureBuild,The FeatureName must fill in!!!"
		exit 1
	fi
	featureName=$3
	label=$4
	repositoryName=$5
	userName=$6
	userPassword=$7
fi

stCmdSun="$HOME/StarTeamCP_2005r2/bin/stcmd"

if [ -f "$HOME/$project/BuildHistory.log" ];then
	echo "BuildHistory.log..."
	list=`grep "$label" $HOME/$project/BuildHistory.log`
	echo list=$list
	arr=(${list// / })
	#标签已经在st创建
	if [ 0 -ne ${#arr[@]} ];then
	    echo  Label $label has existd in ST .
	else
		echo "...create a new label"
		LANG=zh_CN.gb18030
		export LANG
		$stCmdSun label -p "smeebuilder:smeebuilder@172.16.200.12:49208/张网焊接设备（009 009A）" -nl $label -r
		#descripetion=`date "+20%y/%m/%d %H:%M"` " $userName  $label"
		echo `date "+20%y/%m/%d %H:%M"` " $userName  $label">>$HOME/$project/BuildHistory.log
	fi
	
else
	echo "create a new label..."
	LANG=zh_CN.gb18030
	export LANG
	$stCmdSun label -p "smeebuilder:smeebuilder@172.16.200.12:49208/张网焊接设备（009 009A）" -nl $label -r 
	#descripetion=`date "+20%y/%m/%d %H:%M"` " $userName $label"
	echo `date "+20%y/%m/%d %H:%M"` " $userName  $label">>$HOME/$project/BuildHistory.log
fi
exit 0
