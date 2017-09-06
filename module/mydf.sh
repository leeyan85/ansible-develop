#!/bin/bash
set -ex 
#mountpoint='/'
export $1
result=`df -P -k $mountpoint | tail -1`

read total used used_percent <<< `echo $result | awk '{print $2,$3,$5}'`

echo "{\"mountpoint\":\"$mountpoint\",\"used_percent\":\"$used_percent\",\"total\":\"$total\",\"used\": \"$used\"}"
