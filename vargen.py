import random
import sys

filename=sys.argv[1]
ini=(int) (sys.argv[2])
maxi=ini+(int) (sys.argv[3])
mini=ini-(int) (sys.argv[3])
step=(int) (sys.argv[4])
pas=(int) (sys.argv[3])//4
fin=(int) (sys.argv[5])

file=open(filename,'w')
t=0
mach=ini
file.write((str)(mach)+'\n')
while (t<fin):
    a=random.randint(1,2)
    if(a==1):
        mach=mach+pas
    else:
        mach=mach-pas
    if (mach<mini):
        mach=mini
    if(mach>maxi):
        mach=maxi
    t+=step
    file.write((str)(t)+' '+(str)(mach)+'\n')
file.close()
