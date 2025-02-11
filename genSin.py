import random
import sys

def randCore(): #Define tjh number of core
    a=random.uniform(0,1)
    if(a<1/6):
        return(1)
    elif(a<1/2):
        return(2)
    elif(a<5/6):
        return(4)
    else:
        return(8)

def sinUni(filename,step,fin,avL,synLoad):
    file=open(filename,'w')
    t=step #release date
    i=0
    while (t<fin):
        a=random.randint(1,2*avL) #length
        c=randCore() #number of cores
        file.write((str) (i)+ ' '+(str)(t)+' '+(str)(a)+" "+(str) (c)+" release \n")
        t+=step
        i+=1
    file.close()


def sin3(filename,step,fin,avL,synLoad):
    avL=avL*13//27
    file=open(filename,'w')
    t=step
    i=0
    while (t<fin):
        a=random.randint(1,13)
        if(a<10):
            a=avL
        elif(a<13):
            a=3*avL
        else:
            a=9*avL
        c=randCore()
        b=random.uniform(0,1)
        b=(b-0.5)/10
        a=(int) (a*(1+b))
        file.write((str) (i)+ ' '+(str)(t)+' '+(str)(a)+" "+(str) (c)+" release \n")
        t+=step
        i+=1
    file.close()

def sinLog(filename,step,fin,avL,synLoad):
    file=open(filename,'w')
    t=step
    i=0
    while (t<fin):
        a=random.randint(1,4)
        if(a<2):
            a=random.randint(100,500)
        elif(a<3):
            a=random.randint(500,2500)
        elif(a<4):
            a=random.randint(2500,12500)
        else:
            a=random.randint(12500,62500)
        a=(int) (a/19120*avL)
        c=randCore()
        file.write((str) (i)+ ' '+(str)(t)+' '+(str)(a)+" "+(str) (c)+" release \n")
        t+=step
        i+=1
    file.close()

def sinLog2(filename,step,fin,avL,synLoad):
    file=open(filename,'w')
    t=step
    i=0
    while (t<fin):
        a=random.randint(1,15)
        if(a<9):
            a=random.randint(100,500)
        elif(a<13):
            a=random.randint(500,2500)
        elif(a<15):
            a=random.randint(2500,12500)
        else:
            a=random.randint(12500,62500)
        a=(int) (a/4061*avL)
        c=randCore()
        c=4
        file.write((str) (i)+' '+(str)(t)+' '+(str)(a)+" "+(str) (c)+" release \n")
        t+=step
        i+=1
    file.close()

def sinLog4(filename,step,fin,avL,synLoad):
    file=open(filename,'w')
    t=step
    i=0
    while (t<fin):
        a=random.randint(1,85)
        if(a<65):
            a=random.randint(100,500)
        elif(a<81):
            a=random.randint(500,2500)
        elif(a<85):
            a=random.randint(2500,12500)
        else:
            a=random.randint(12500,62500)
        a=(int) (a/1300*avL)
        c=randCore()
        file.write((str) (i)+ ' '+(str)(t)+' '+(str)(a)+" "+(str) (c)+" release \n")
        t+=step
        i+=1
    file.close()

typ=sys.argv[1]
filename=sys.argv[2]
nJ=(int) (sys.argv[3])
synLoad=(int) (sys.argv[4])
fin=(int) (sys.argv[5])
step=fin//nJ
nJ=fin//step
avL=(fin*synLoad)//(4*nJ)
if(typ=="syntUni"):
    sinUni(filename,step,fin,avL,synLoad)
elif(typ=="synt3"):
    sin3(filename,step,fin,avL,synLoad)
elif(typ=="syntLog"):
    sinLog(filename,step,fin,avL,synLoad)
elif(typ=="syntLog2"):
    sinLog2(filename,step,fin,avL,synLoad)
elif(typ=="syntLog4"):
    sinLog4(filename,step,fin,avL,synLoad)


