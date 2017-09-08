#!/bin/bash 
export  $1
#filename='/etc/password'
#echo $test
if [ ! -f "$filename" ]
then
    echo "noexist"
    exit
fi 

fact_file=/tmp/myfact.txt
if [ ! -f "$fact_file" ]; then
   touch "$fact_file"
fi

fact_exist="`grep $filename /tmp/myfact.txt`"


if [ -z "$fact_exist" ]
then
    md5value=`md5sum $filename | awk '{print $1}'`
    echo "$filename:$md5value" >> /tmp/myfact.txt
    echo "register"
else
    md5sum_old=`grep $filename $fact_file | awk -F":" '{print $2}'`
    md5sum_new=`md5sum $filename| awk '{print $1}'`
    #echo  $md5sum_old $md5sum_new
    if [ "$md5sum_old" == "$md5sum_new" ]
    then
        echo "unmodified"
    else
        sed -i "s#$filename.*#$filename:$md5sum_new#g" $fact_file
        echo "modified"
    fi    
fi
