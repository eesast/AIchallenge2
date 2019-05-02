#!/usr/bin/env python3
import os
import json
import shutil
import sys
rootdir = '/share/Codes/output'
targetdir='/ts20/AI'
team=[]
ban_teamid=30
def main():
    files = os.listdir(rootdir)
    i = 0
    for file in files:
        file=os.path.join(rootdir,file)
        if(os.path.isfile(file)):
            file = os.path.basename(file)
            teamid = int(file[0:2])
            if teamid not in team and teamid!=ban_teamid:
                team.append(teamid)
    print(team)
    for i, teamid in enumerate(team):
        for playerid in range(4):
            shutil.copyfile(os.path.join(rootdir, '{}_{}.so'.format(teamid, playerid)), os.path.join(targetdir, 'libAI_{}_{}.so'.format(i, playerid)))
    with open('team.json', 'w') as f:
        json.dump(team,f)
if __name__ == '__main__':
    ban_teamid=int(sys.argv[1])
    main()
        
