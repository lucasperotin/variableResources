import sys

filein=sys.argv[1]
fileout=sys.argv[2]
packs=(int) (sys.argv[3])
start=(int) (sys.argv[4])
window=(int) (sys.argv[5])

file=open(filein,'r')
lines=file.readlines()
file.close()

L=[]
totArea=0

for line in lines:
    line=line.split(" ")
    arrival=(int) (line[1])
    length=(int) (line[2])
    if(length>604800):
        length=604800
    if(length>0):
        procs=(int) (line[3])
        L.append([length,procs])
        totArea+=length*procs
    
L.sort()
c=1/packs
ci=1
tempArea=0

file2=open(fileout,'w')
for i in range(len(L)):
    tempArea+=L[i][0]*L[i][1]
    while (tempArea>c*totArea):
        file2.write((str) (L[i][0])+"\n")
        c+=1/packs
        ci+=1
file2.close()
