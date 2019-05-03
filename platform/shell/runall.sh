#!/bin/bash
cd /ts20
order=(45 60 30 37 39 40 41 50 51 52 54 58 64 70 71 68)
for i in ${order[@]};do
	echo "run $i"
	python3 /share/clear.py
	rm AI/* log/* playback/*
	python3 /share/run.py $i 
	./platform >/dev/null
	cp team.json "/share/Codes/result/team${i}.json"
	cp log/*.txt "/share/Codes/result/log${i}.txt"
	cp playback/*.pb "/share/Codes/result/${i}.pb"
	cp playback/*.json "/share/Codes/result/score${i}.pb"
done
