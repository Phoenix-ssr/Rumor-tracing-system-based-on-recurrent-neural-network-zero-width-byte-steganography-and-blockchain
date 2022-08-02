with open(r"./rumorid.txt") as f:
    rumorid = f.readline()
    rumorid = int(rumorid)
with open('rumorid.txt','w',encoding='utf-8') as f:
    f.write(str(rumorid+1))
