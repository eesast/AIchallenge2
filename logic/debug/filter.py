with open('out.txt','r') as fp:
    lines = fp.readlines()
with open('out2.txt','w') as fp:
    for line in lines:
        if line.find('but') == -1:
            fp.write(line)
