from json import *

def t(team):
    new_team=[]
    team.append(new_team)
    new_team.append(0)
    new_team.append(1)

info =\
{
    "comment":
    '''
here give debug level, some import data_file relative path
''',
    "PRINT_DEBUG":10,
    
    "CHARACTER_FILE_PATH" : "./data/character.ini",
    
    "ITEM_FILE_PATH" : "./data/character.ini",
    
    "MAP_FILE_PATH" : "./data/map",
    
    
}
'''
file = open(r"D:/repository/AIchallenge2/logic/config.ini", 'w', encoding='utf-8')
dump(info, file)
file.close()

with open("../config.ini","r",encoding="utf-8") as fp:
    info = load(fp)
print(info)'''


team = []
t(team)
t(team)
print(team)
