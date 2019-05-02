#!/bin/bash
dir=/share/Codes
cd /ts20/code/build
for file in $dir/*; do
	if [ ${file##*.} == "cpp" ];then
   		echo "$file"
    		cp -v $file /ts20/code/player-only/src/player.cpp
    		make
    		cp -v /ts20/code/build/player-only/libAI.so "${file%.*}.so"
	fi
done
