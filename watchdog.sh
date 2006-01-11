MAXTHREADS=100
DELAY=10

while (true);do A=$(netstat -atlnp  2>/dev/null |grep python|grep -c CLOSE_WAIT); if (($A > $MAXTHREADS ));then (printf "warning too many threads"|mail -s "WARNING freeviz" sleon) ; fi;sleep $DELAY;done
