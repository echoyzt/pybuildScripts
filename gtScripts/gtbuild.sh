#!/bin/sh
LANG=zh_CN.GB18030
export LANG
STCMD="$HOME/StarTeamCP_2005r2/bin/stcmd"
RM=/bin/rm
COPY=/bin/cp
localbase=$HOME/Star_src

. prjconfig.cfg
source prjconfig.cfg

cd
current_date=`date +%y-%m-%d`
echo "view=$1 "
echo $#
newprj="_"$1
eval temp=$(echo \$$newprj)
case $# in
	5)
		PROSON=$4:$5${temp}
		echo '11111111111111111111111'
		;;
	6)
		PROSON=$5:$6${temp}
		echo '22222222222222222222222'
		;;
	*)
		;;
esac
echo $PROSON

if [ "$1" != "GEM300" ];then
	$STCMD co -p "$PROSON/export" -fp $localbase/export -o -ts -nologo
	$STCMD co -p "$PROSON/BASE/xinc" -fp $localbase/BASE/xinc -o -ts -nologo
	$COPY -rf $localbase/export/* SRC/xinc
	$COPY -rf $localbase/BASE/xinc/* SRC/xinc
fi

case $# in
	5)
		echo "Start Gen 5paras"
		cd
		$RM -rf $localbase/$2/$3/*
 		$RM   -rf $localbase/$2/xinc
 		$STCMD local-mkdir -p "$PROSON/$2/$3/com" -fp $localbase/$2/$3/com -is -nologo
 		$STCMD co -p "$PROSON/$2/xinc" -fp $localbase/$2/xinc -o -ts -nologo
 		$STCMD co -p "$PROSON/$2/$3/com/ext/inc" -fp $localbase/$2/$3/com/ext/inc -o -ts -nologo
 		$STCMD co -p "$PROSON/$2/$3/com/ext/typ" -fp $localbase/$2/$3/com/ext/typ -o -ts -nologo
 		$COPY -rf $localbase/$2/xinc/*.h $localbase/$2/$3/com/ext/inc
 		$COPY -rf $localbase/$2/xinc/*.h $localbase/$2/$3/com/ext/typ
 		if [ -d $localbase/$2/$3/com/com ];then
 			$STCMD co -p "$PROSON/$2/$3/com/com/ext/inc" -fp $localbase/$2/$3/com/com/ext/inc -o -ts -nologo
 			$STCMD co -p "$PROSON/$2/$3/com/com/ext/typ" -fp $localbase/$2/$3/com/com/ext/typ -o -ts -nologo
 		fi
 		$STCMD local-mkdir -p "$PROSON/$2/gen" -fp $localbase/$2/gen
 		$STCMD co -p "$PROSON/$2/gen" -fp $localbase/$2/gen -o -ts -nologo
 		$RM   -rf SRC/$3
 		$COPY -rf $localbase/$2/$3 SRC/$3
 		$COPY -rf $localbase/$2/$3/com/ext/inc/* SRC/xinc
 		$COPY -rf $localbase/$2/$3/com/ext/typ/* SRC/xinc
 		$COPY -rf $localbase/$2/$3/com/ext/inc/*.h SRC/xinc
		$COPY -rf $localbase/$2/xinc/* SRC/PARSE/xinc
		$COPY -rf $localbase/$2/xinc/* SRC/xinc
 		cd SRC
 		LANG=C
 		export LANG
 					
 		InterfaceGen -C $3 -F
 		if [ $? -ne 0 ];then
 			exit 1
 		fi
 					
 		if [ ! -f $3/com/ext/lib/$34I.c ];then
 			ls  $3/com/com/ext/lib/*4I.c
 			if [ $? -ne 0 ];then
 				exit 1
 			fi
 		fi
 		$RM -rf $localbase/$2/gen/*
 		tar cf $localbase/$2/gen/$3.tar $3
 		if [ $? -ne 0 ];then
 			exit 1
 		fi

		cd
		LANG=zh_CN.GB18030
		export LANG
		$STCMD ci -p  "$PROSON/$2/gen" -fp $localbase/$2/gen -is -filter "M" -nologo
		$STCMD add -p "$PROSON/$2/gen" -fp $localbase/$2/gen  -nologo
		echo InterfaceGen $2 finish!
		;;
	6)
		echo "Start Gen 6paras"
		case $3 in
			RC )
			cd
 			$RM   -rf $localbase/$2/$3/$4/*
 			$RM   -rf $localbase/$2/xinc
 			$STCMD local-mkdir -p "$PROSON/$2/$3/$4/com" -fp $localbase/$2/$3/$4/com -is -nologo
 			$STCMD co -p "$PROSON/$2/xinc" -fp $localbase/$2/xinc -o -ts -nologo
 			$STCMD co -p "$PROSON/$2/$3/$4/com/ext/inc" -fp $localbase/$2/$3/$4/com/ext/inc -o -ts -nologo
 			$STCMD co -p "$PROSON/$2/$3/$4/com/ext/typ" -fp $localbase/$2/$3/$4/com/ext/typ -o -ts -nologo

 			if [ -d $localbase/$2/$3/$4/com/com ];then
				$STCMD co -p "$PROSON/$2/$3/$4/com/com/ext/inc" -fp $localbase/$2/$3/$4/com/com/ext/inc -o -ts -nologo
 				$STCMD co -p "$PROSON/$2/$3/$4/com/com/ext/typ" -fp $localbase/$2/$3/$4/com/com/ext/typ -o -ts -nologo
 			fi
 			$STCMD local-mkdir -p "$PROSON/$2/gen" -fp $localbase/$2/gen
 			$STCMD co -p "$PROSON/$2/gen" -fp $localbase/$2/gen -o -ts -nologo
					
 			$RM   -rf SRC/$4
			mkdir -p SRC/$4
 			$COPY -rf $localbase/$2/$3/$4/* 	SRC/$4
 			$COPY -rf $localbase/$2/$3/$4/com/ext/inc/* SRC/xinc
 			$COPY -rf $localbase/$2/$3/$4/com/ext/typ/* SRC/xinc
					
 			cd SRC
 			LANG=C
 			export LANG
 			InterfaceGen -C $4 -F

 			if [ $? -ne 0 ];then
 				exit 1
 			fi

 			$RM -rf $localbase/$2/gen/*
 			tar cf $localbase/$2/gen/$4.tar $4
 			if [ $? -ne 0 ];then
 				exit 1
 			fi

			cd
			LANG=zh_CN.GB18030
			export LANG
			$STCMD ci -p  "$PROSON/$2/gen" -fp $localbase/$2/gen -is -filter "M" -nologo
			$STCMD add -p "$PROSON/$2/gen" -fp $localbase/$2/gen  -nologo
			echo InterfaceGen $2 finish!
			;;
			OI )
			cd
			$RM   -rf $localbase/$2/$3/$4/*
			$RM   -rf $localbase/$2/xinc
			$STCMD local-mkdir -p "$PROSON/$2/$3/$4/com" -fp $localbase/$2/$3/$4/com -is -nologo
			$STCMD co -p "$PROSON/$2/xinc" -fp $localbase/$2/xinc -o -ts -nologo
			$STCMD co -p "$PROSON/$2/$3/$4/com/ext/inc" -fp $localbase/$2/$3/$4/com/ext/inc -o -ts -nologo
			$STCMD co -p "$PROSON/$2/$3/$4/com/ext/typ" -fp $localbase/$2/$3/$4/com/ext/typ -o -ts -nologo
			$COPY -rf $localbase/$2/xinc/*.h $localbase/$2/$3/com/ext/inc
			$COPY -rf $localbase/$2/xinc/*.h $localbase/$2/$3/com/ext/typ
			if [ -d $localbase/$2/$3/$4/com/com ];then
				$STCMD co -p "$PROSON/$2/$3/$4/com/com/ext/inc" -fp $localbase/$2/$3/$4/com/com/ext/inc -o -ts -nologo
				$STCMD co -p "$PROSON/$2/$3/$4/com/com/ext/typ" -fp $localbase/$2/$3/$4/com/com/ext/typ -o -ts -nologo
			fi
			$STCMD local-mkdir -p "$PROSON/$2/gen" -fp $localbase/$2/gen
			$STCMD co -p "$PROSON/$2/gen" -fp $localbase/$2/gen -o -ts -nologo
			$RM   -rf SRC/$3/$4
			$COPY -rf $localbase/$2/$3/$4 SRC/$3/$4
			$COPY -rf $localbase/$2/$3/$4/com/ext/inc/* SRC/xinc
			$COPY -rf $localbase/$2/$3/$4/com/ext/typ/* SRC/xinc
			$COPY -rf $localbase/$2/$3/$4/com/ext/inc/*4T_if.h SRC/xinc
			$COPY -rf $localbase/$2/xinc/* SRC/PARSE/xinc
			$COPY -rf $localbase/$2/xinc/* SRC/xinc
					
			cd SRC
					
			LANG=C
			export LANG
			if [ $4 != OIMA ];then
				mkdir -p OI/$4/$4DM
				InterfaceGen -C $4 -F
			else
				mkdir -p OI/$4/$4SM
				InterfaceGen -C $4 -F
			fi
					
					
			if [ $? -ne 0 ];then
				exit 1
			fi
					
			if [ ! -f $3/$4/com/ext/lib/$44I.c ];then
				ls  $3/$4/com/com/ext/lib/*4I.c
				if [ $? -ne 0 ];then
					exit 1
				fi
			fi
					
			$RM -rf $localbase/$2/gen/*
			tar cf $localbase/$2/gen/$4.tar OI/$4
			if [ $? -ne 0 ];then
				exit 1
			fi

			cd
			LANG=zh_CN.GB18030
			export LANG
			$STCMD ci -p  "$PROSON/$2/gen" -fp $localbase/$2/gen -is -filter "M" -nologo
			$STCMD add -p "$PROSON/$2/gen" -fp $localbase/$2/gen  -nologo
			echo InterfaceGen $2 finish!
			;;
		esac
		;;
esac	