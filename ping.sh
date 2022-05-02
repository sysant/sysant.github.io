#!/bin/bash
# version v1.0 by san at 2012-06-6

net=192.168.1    # ping扫描的网段
for h in `seq 10 254`
do
( echo $h
   if ping -c 1 $net.$h
   then
        echo "$net.$h OK"
   else
        echo "$net.$h NO"
   fi
)&
done
wait
