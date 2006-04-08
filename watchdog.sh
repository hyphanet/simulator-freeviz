#! /bin/bash
PSCMD="ps -C circo -o time,pid --no-headers"

function kgen {
	echo killing generator proccess
	kill -9 $(ps -e -o pid,cmd|grep python|grep gen|grep -E  -o  "^[[:space:]]*[[:digit:]]+")
}

PROCESSES=$($PSCMD)
OIFS=$IFS;IFS=
for i in $PROCESSES;do
	IFS=$OIFS
	LINE=($i)
	IFS=
	PID=${LINE[1]}
	DATA=${LINE[0]}
	IFS=:
	TIME=($DATA)
	IFS=

	#echo $PID $DATA DEBUG
	#echo ${TIME[@]:0} DEBUG

	if [ "${TIME[0]}" != "00" ];then
		echo killing $PID , runs for several hours already
		kill -9 $PID
		kgen
	fi
	
	if (( "${TIME[1]}" > 3 ));then
		echo killing $PID, runs more then 3 minutes
		kill -9 $PID
		kgen
	fi
done

IFS=$OIFS

