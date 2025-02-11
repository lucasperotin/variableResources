import os
TODO=["fold","var","tra","args","launch"]
#TODO=["plots"]

#######ARGS########

varAv=["20","22","24","26","28"]
vAb="24"
varRange=["4","6","12","16"]
vRb="8"
#Step is vRb/4
varFreq=["400","3600","10800","32400"]
vFb="1200"
nbJobs=["8000","14000","28000","40000"]
nJb="20000"
nbCores=["48","32","16","8"]
varAv2=["12","18","36","72"]
vCb="24"
AlgPar=["7 80 95"]

objectives=["utiltot","avgSt","maxSt","Waste","avgLength","perc"]
#objectives=["utiltot"]
synTraces=["synt3","syntLog","syntLog4","syntUni"]
#synTraces=[]
BorTraces=["borgSO"]
#BorTraces=["borgSO"]
plots=BorTraces+synTraces

TimeSteps=[["864000","1123200","1382400","1468800","1728000","1987200"],["259200","518400","777600","864000","1123200","1382400"]]
#TimeSteps=[["864000"],["259200"]]
synLoad="725"
nbSamples=6
nbVar=30
nbMach="152"
window="604800"
Varlen="3000000"
###################




naLg=len(AlgPar)
varAvT=varAv+[vAb]
varAvT.sort(key=int)
varRangeT=varRange+[vRb]
varRangeT.sort(key=int)
varFreqT=varFreq+[vFb]
varFreqT.sort(key=int)
nbJobsT=nbJobs+[nJb]
nbJobsT.sort(key=int)
nbCoresT=nbCores+[vCb]
nbCoresT.sort(key=int)
window2=(str) (((int) (window))*2)
window3=(str) (((int) (window))*3)
Windows=[window,window2,window3]
version=0

loc="./files/variations/"

##GENERATE FOLDERS##
if("fold" in TODO):
    print("Generate Folders")
    os.chdir(loc)
    os.system("rm -r *")
    os.system("mkdir Av"+vAb+"Ra"+vRb+"Fr"+vFb)
    for i in varAv:
        os.system("mkdir Av"+i+"Ra"+vRb+"Fr"+vFb)
    for i in varRange:
        os.system("mkdir Av"+vAb+"Ra" +i+"Fr"+vFb)
    for i in varFreq:
        os.system("mkdir Av"+vAb+"Ra"+vRb+"Fr"+i)
    for i in range(len(nbCores)):
        os.system("mkdir Av"+varAv2[i]+"Ra"+varRange[i]+"Fr"+vFb)
    os.chdir("../..")

##GENERATE Variation traces##
if("var" in TODO):
    print("Generate Variation traces")
    for j in range(nbVar):
        os.system("python3 vargen.py "+loc+"Av"+vAb+"Ra"+vRb+"Fr"+vFb+"/sample"+(str)(j)+".txt "+vAb+" "+ vRb+" "+" "+vFb+" "+Varlen)
        for i in range(len(nbCores)):
            os.system("python3 vargen.py "+loc+"Av"+varAv2[i]+"Ra"+varRange[i]+"Fr"+vFb+"/sample"+(str)(j)+".txt "+varAv2[i]+" "+ varRange[i]+" "+" "+vFb+" "+Varlen)
        for i in varAv:
            os.system("python3 vargen.py "+loc+"Av"+i+"Ra"+vRb+"Fr"+vFb+"/sample"+(str)(j)+".txt "+i+" "+ vRb+" "+" "+vFb+" "+Varlen)
        for i in varRange:
            os.system("python3 vargen.py "+loc+"Av"+vAb+"Ra"+i+"Fr"+vFb+"/sample"+(str)(j)+".txt "+vAb+" "+ i+" "+" "+vFb+" "+Varlen)
        for i in varFreq:
            os.system("python3 vargen.py "+loc+"Av"+vAb+"Ra"+vRb+"Fr"+i+"/sample"+(str)(j)+".txt "+vAb+" "+ vRb+" "+" "+i+" "+Varlen)
    
##GENERATE Synthetic traces##
if("tra" in TODO):
    print("Generate Synthetic traces")
    os.chdir("./files/traces/")
    os.system("find . -type f -name 'n*' -delete")
    os.chdir("../..")
    for i in synTraces:
        print(i)
        for j in range (nbSamples+1):
            for k in nbJobsT:
                k=k
                os.system("python3 genSin.py "+i+" ./files/traces/"+i+"/n"+k+"_"+(str)(j)+".txt "+(str)(((int)(k))*3)+" "+synLoad+" "+window3)
    for i in synTraces:
        for k in nbJobsT:
            os.system("python3 genData.py ./files/traces/"+i+"/n"+k+"_"+(str)(nbSamples)+".txt ./files/traces/"+i+"/n"+k+"DATA.txt 1000 "+window2+" "+window)
    for i in BorTraces:
        os.system("python3 genData.py ./files/traces/"+i+"/7D_604800.txt ./files/traces/"+i+"/DATA.txt 1000 604800 604800")

#GENERATE args#
if("args" in TODO):
    os.chdir("./files/arguments/")
    os.system("rm *")
    os.chdir("../..")
    print("Generate arguments")
    
    
    for z in range(nbVar):
        for j in range(len(TimeSteps[1])):
            for i in range(len(BorTraces)):   
                folT=BorTraces[i]
                file=open("./files/arguments/args"+(str)(j)+".txt",'a')
                for l in range(len(AlgPar)):
                    al=AlgPar[l]
                    for t in range(version,version+1):
                        file.write("./files/traces/"+folT+"/"+(str)((t+1)*7)+"D_"+TimeSteps[t][j]+".txt "+nbMach+" "+(str)((int)(vAb)-(int)(vRb))+" "+vCb+" "+"./files/variations/Av"+vAb+"Ra"+vRb+"Fr"+vFb+"/sample"+(str)(z)+".txt "+TimeSteps[t][j]+" "+Windows[t]+" algo "+(str)(t+1)+" ./files/traces/"+folT+"/DATA.txt BSS "+al+" ./files/results/"+folT+"/n20000Av"+vAb+"Ra"+vRb+"Fr"+vFb+"Co"+vCb+"a"+(str)(l+len(AlgPar)*t)+"BSS.txt\n")
                        file.write("./files/traces/"+folT+"/"+(str)((t+1)*7)+"D_"+TimeSteps[t][j]+".txt "+nbMach+" "+(str)((int)(vAb)-(int)(vRb))+" "+vCb+" "+"./files/variations/Av"+vAb+"Ra"+vRb+"Fr"+vFb+"/sample"+(str)(z)+".txt "+TimeSteps[t][j]+" "+Windows[t]+" algo "+(str)(t+1)+" ./files/traces/"+folT+"/DATA.txt BP1 "+al+" ./files/results/"+folT+"/n20000Av"+vAb+"Ra"+vRb+"Fr"+vFb+"Co"+vCb+"a"+(str)(l+len(AlgPar)*t)+"BP1.txt\n")
                        file.write("./files/traces/"+folT+"/"+(str)((t+1)*7)+"D_"+TimeSteps[t][j]+".txt "+nbMach+" "+(str)((int)(vAb)-(int)(vRb))+" "+vCb+" "+"./files/variations/Av"+vAb+"Ra"+vRb+"Fr"+vFb+"/sample"+(str)(z)+".txt "+TimeSteps[t][j]+" "+Windows[t]+" algo "+(str)(t+1)+" ./files/traces/"+folT+"/DATA.txt BS1 "+al+" ./files/results/"+folT+"/n20000Av"+vAb+"Ra"+vRb+"Fr"+vFb+"Co"+vCb+"a"+(str)(l+len(AlgPar)*t)+"BS1.txt\n")
                for l in range(2):
                    for t in range(version,version+1):
                        file.write("./files/traces/"+folT+"/"+(str)((t+1)*7)+"D_"+TimeSteps[t][j]+".txt "+nbMach+" "+(str)((int)(vAb)-(int)(vRb))+" "+vCb+" "+"./files/variations/Av"+vAb+"Ra"+vRb+"Fr"+vFb+"/sample"+(str)(z)+".txt "+TimeSteps[t][j]+" "+Windows[t]+" FF "+(str)(t+1)+" "+(str)(l)+" ./files/results/"+folT+"/n20000Av"+vAb+"Ra"+vRb+"Fr"+vFb+"Co"+vCb+"FF"+(str)(l+2*t)+".txt\n")
                for t in range(0):
                    file.write("./files/traces/"+folT+"/"+(str)((t+1)*7)+"D_"+TimeSteps[t][j]+".txt "+nbMach+" "+(str)((int)(vAb)-(int)(vRb))+" "+vCb+" "+"./files/variations/Av"+vAb+"Ra"+vRb+"Fr"+vFb+"/sample"+(str)(z)+".txt "+TimeSteps[t][j]+" "+Windows[t]+" algo2 "+(str)(t+1)+" ./files/traces/"+folT+"/DATA.txt ./files/results/"+folT+"/n20000Av"+vAb+"Ra"+vRb+"Fr"+vFb+"Co"+vCb+"a2"+(str)(t)+".txt\n")
                
                for k in varAv:
                    for l in range(len(AlgPar)):
                        al=AlgPar[l]
                        for t in range(version,version+1):
                            file.write("./files/traces/"+folT+"/"+(str)((t+1)*7)+"D_"+TimeSteps[t][j]+".txt "+nbMach+" "+(str)((int)(k)-(int)(vRb))+" "+vCb+" "+"./files/variations/Av"+k+"Ra"+vRb+"Fr"+vFb+"/sample"+(str)(z)+".txt "+TimeSteps[t][j]+" "+Windows[t]+" algo "+(str)(t+1)+" ./files/traces/"+folT+"/DATA.txt BSS "+al+" ./files/results/"+folT+"/n20000Av"+k+"Ra"+vRb+"Fr"+vFb+"Co"+vCb+"a"+(str)(l+len(AlgPar)*t)+"BSS.txt\n")
                            file.write("./files/traces/"+folT+"/"+(str)((t+1)*7)+"D_"+TimeSteps[t][j]+".txt "+nbMach+" "+(str)((int)(k)-(int)(vRb))+" "+vCb+" "+"./files/variations/Av"+k+"Ra"+vRb+"Fr"+vFb+"/sample"+(str)(z)+".txt "+TimeSteps[t][j]+" "+Windows[t]+" algo "+(str)(t+1)+" ./files/traces/"+folT+"/DATA.txt BP1 "+al+" ./files/results/"+folT+"/n20000Av"+k+"Ra"+vRb+"Fr"+vFb+"Co"+vCb+"a"+(str)(l+len(AlgPar)*t)+"BP1.txt\n")
                            file.write("./files/traces/"+folT+"/"+(str)((t+1)*7)+"D_"+TimeSteps[t][j]+".txt "+nbMach+" "+(str)((int)(k)-(int)(vRb))+" "+vCb+" "+"./files/variations/Av"+k+"Ra"+vRb+"Fr"+vFb+"/sample"+(str)(z)+".txt "+TimeSteps[t][j]+" "+Windows[t]+" algo "+(str)(t+1)+" ./files/traces/"+folT+"/DATA.txt BS1 "+al+" ./files/results/"+folT+"/n20000Av"+k+"Ra"+vRb+"Fr"+vFb+"Co"+vCb+"a"+(str)(l+len(AlgPar)*t)+"BS1.txt\n")
                    for l in range(2):
                        for t in range(version,version+1):
                            file.write("./files/traces/"+folT+"/"+(str)((t+1)*7)+"D_"+TimeSteps[t][j]+".txt "+nbMach+" "+(str)((int)(k)-(int)(vRb))+" "+vCb+" "+"./files/variations/Av"+k+"Ra"+vRb+"Fr"+vFb+"/sample"+(str)(z)+".txt "+TimeSteps[t][j]+" "+Windows[t]+" FF "+(str)(t+1)+" "+(str)(l)+" ./files/results/"+folT+"/n20000Av"+k+"Ra"+vRb+"Fr"+vFb+"Co"+vCb+"FF"+(str)(l+2*t)+".txt\n")
                    for t in range(0):
                        file.write("./files/traces/"+folT+"/"+(str)((t+1)*7)+"D_"+TimeSteps[t][j]+".txt "+nbMach+" "+(str)((int)(k)-(int)(vRb))+" "+vCb+" "+"./files/variations/Av"+k+"Ra"+vRb+"Fr"+vFb+"/sample"+(str)(z)+".txt "+TimeSteps[t][j]+" "+Windows[t]+" algo2 "+(str)(t+1)+" ./files/traces/"+folT+"/DATA.txt ./files/results/"+folT+"/n20000Av"+k+"Ra"+vRb+"Fr"+vFb+"Co"+vCb+"a2"+(str)(t)+".txt\n")
                    
                for k in varRange:
                    for l in range(len(AlgPar)):
                        al=AlgPar[l]
                        for t in range(version,version+1):
                            file.write("./files/traces/"+folT+"/"+(str)((t+1)*7)+"D_"+TimeSteps[t][j]+".txt "+nbMach+" "+(str)((int)(vAb)-(int)(k))+" "+vCb+" "+"./files/variations/Av"+vAb+"Ra"+k+"Fr"+vFb+"/sample"+(str)(z)+".txt "+TimeSteps[t][j]+" "+Windows[t]+" algo "+(str)(t+1)+" ./files/traces/"+folT+"/DATA.txt BSS "+al+" ./files/results/"+folT+"/n20000Av"+vAb+"Ra"+k+"Fr"+vFb+"Co"+vCb+"a"+(str)(l+len(AlgPar)*t)+"BSS.txt\n")
                            file.write("./files/traces/"+folT+"/"+(str)((t+1)*7)+"D_"+TimeSteps[t][j]+".txt "+nbMach+" "+(str)((int)(vAb)-(int)(k))+" "+vCb+" "+"./files/variations/Av"+vAb+"Ra"+k+"Fr"+vFb+"/sample"+(str)(z)+".txt "+TimeSteps[t][j]+" "+Windows[t]+" algo "+(str)(t+1)+" ./files/traces/"+folT+"/DATA.txt BP1 "+al+" ./files/results/"+folT+"/n20000Av"+vAb+"Ra"+k+"Fr"+vFb+"Co"+vCb+"a"+(str)(l+len(AlgPar)*t)+"BP1.txt\n")
                            file.write("./files/traces/"+folT+"/"+(str)((t+1)*7)+"D_"+TimeSteps[t][j]+".txt "+nbMach+" "+(str)((int)(vAb)-(int)(k))+" "+vCb+" "+"./files/variations/Av"+vAb+"Ra"+k+"Fr"+vFb+"/sample"+(str)(z)+".txt "+TimeSteps[t][j]+" "+Windows[t]+" algo "+(str)(t+1)+" ./files/traces/"+folT+"/DATA.txt BS1 "+al+" ./files/results/"+folT+"/n20000Av"+vAb+"Ra"+k+"Fr"+vFb+"Co"+vCb+"a"+(str)(l+len(AlgPar)*t)+"BS1.txt\n")
                    for l in range(2):
                        for t in range(version,version+1):
                            file.write("./files/traces/"+folT+"/"+(str)((t+1)*7)+"D_"+TimeSteps[t][j]+".txt "+nbMach+" "+(str)((int)(vAb)-(int)(k))+" "+vCb+" "+"./files/variations/Av"+vAb+"Ra"+k+"Fr"+vFb+"/sample"+(str)(z)+".txt "+TimeSteps[t][j]+" "+Windows[t]+" FF "+(str)(t+1)+" "+(str)(l)+" ./files/results/"+folT+"/n20000Av"+vAb+"Ra"+k+"Fr"+vFb+"Co"+vCb+"FF"+(str)(l+2*t)+".txt\n")
                    for t in range(0):
                        file.write("./files/traces/"+folT+"/"+(str)((t+1)*7)+"D_"+TimeSteps[t][j]+".txt "+nbMach+" "+(str)((int)(vAb)-(int)(k))+" "+vCb+" "+"./files/variations/Av"+vAb+"Ra"+k+"Fr"+vFb+"/sample"+(str)(z)+".txt "+TimeSteps[t][j]+" "+Windows[t]+" algo2 "+(str)(t+1)+" ./files/traces/"+folT+"/DATA.txt ./files/results/"+folT+"/n20000Av"+vAb+"Ra"+k+"Fr"+vFb+"Co"+vCb+"a2"+(str)(t)+".txt\n")
                     
                for k in varFreq:
                    for l in range(len(AlgPar)):
                        al=AlgPar[l]
                        for t in range(version,version+1):
                            file.write("./files/traces/"+folT+"/"+(str)((t+1)*7)+"D_"+TimeSteps[t][j]+".txt "+nbMach+" "+(str)((int)(vAb)-(int)(vRb))+" "+vCb+" "+"./files/variations/Av"+vAb+"Ra"+vRb+"Fr"+k+"/sample"+(str)(z)+".txt "+TimeSteps[t][j]+" "+Windows[t]+" algo "+(str)(t+1)+" ./files/traces/"+folT+"/DATA.txt BSS "+al+" ./files/results/"+folT+"/n20000Av"+vAb+"Ra"+vRb+"Fr"+k+"Co"+vCb+"a"+(str)(l+len(AlgPar)*t)+"BSS.txt\n")
                            file.write("./files/traces/"+folT+"/"+(str)((t+1)*7)+"D_"+TimeSteps[t][j]+".txt "+nbMach+" "+(str)((int)(vAb)-(int)(vRb))+" "+vCb+" "+"./files/variations/Av"+vAb+"Ra"+vRb+"Fr"+k+"/sample"+(str)(z)+".txt "+TimeSteps[t][j]+" "+Windows[t]+" algo "+(str)(t+1)+" ./files/traces/"+folT+"/DATA.txt BP1 "+al+" ./files/results/"+folT+"/n20000Av"+vAb+"Ra"+vRb+"Fr"+k+"Co"+vCb+"a"+(str)(l+len(AlgPar)*t)+"BP1.txt\n")
                            file.write("./files/traces/"+folT+"/"+(str)((t+1)*7)+"D_"+TimeSteps[t][j]+".txt "+nbMach+" "+(str)((int)(vAb)-(int)(vRb))+" "+vCb+" "+"./files/variations/Av"+vAb+"Ra"+vRb+"Fr"+k+"/sample"+(str)(z)+".txt "+TimeSteps[t][j]+" "+Windows[t]+" algo "+(str)(t+1)+" ./files/traces/"+folT+"/DATA.txt BS1 "+al+" ./files/results/"+folT+"/n20000Av"+vAb+"Ra"+vRb+"Fr"+k+"Co"+vCb+"a"+(str)(l+len(AlgPar)*t)+"BS1.txt\n")
                    for l in range(2):
                        for t in range(version,version+1):
                            file.write("./files/traces/"+folT+"/"+(str)((t+1)*7)+"D_"+TimeSteps[t][j]+".txt "+nbMach+" "+(str)((int)(vAb)-(int)(vRb))+" "+vCb+" "+"./files/variations/Av"+vAb+"Ra"+vRb+"Fr"+k+"/sample"+(str)(z)+".txt "+TimeSteps[t][j]+" "+Windows[t]+" FF "+(str)(t+1)+" "+(str)(l)+" ./files/results/"+folT+"/n20000Av"+vAb+"Ra"+vRb+"Fr"+k+"Co"+vCb+"FF"+(str)(l+2*t)+".txt\n")
                    for t in range(0):
                        file.write("./files/traces/"+folT+"/"+(str)((t+1)*7)+"D_"+TimeSteps[t][j]+".txt "+nbMach+" "+(str)((int)(vAb)-(int)(vRb))+" "+vCb+" "+"./files/variations/Av"+vAb+"Ra"+vRb+"Fr"+k+"/sample"+(str)(z)+".txt "+TimeSteps[t][j]+" "+Windows[t]+" algo2 "+(str)(t+1)+" ./files/traces/"+folT+"/DATA.txt ./files/results/"+folT+"/n20000Av"+vAb+"Ra"+vRb+"Fr"+k+"Co"+vCb+"a2"+(str)(t)+".txt\n")
                    
                for k in range(len(nbCores)):
                    for l in range(len(AlgPar)):
                        al=AlgPar[l]
                        for t in range(version,version+1):
                            file.write("./files/traces/"+folT+"/"+(str)((t+1)*7)+"D_"+TimeSteps[t][j]+".txt "+nbMach+" "+(str)((int)(varAv2[k])-(int)(varRange[k]))+" "+nbCores[k]+" "+"./files/variations/Av"+varAv2[k]+"Ra"+varRange[k]+"Fr"+vFb+"/sample"+(str)(z)+".txt "+TimeSteps[t][j]+" "+Windows[t]+" algo "+(str)(t+1)+" ./files/traces/"+folT+"/DATA.txt BSS "+al+" ./files/results/"+folT+"/n20000Av"+vAb+"Ra"+vRb+"Fr"+vFb+"Co"+nbCores[k]+"a"+(str)(l+len(AlgPar)*t)+"BSS.txt\n")
                            file.write("./files/traces/"+folT+"/"+(str)((t+1)*7)+"D_"+TimeSteps[t][j]+".txt "+nbMach+" "+(str)((int)(varAv2[k])-(int)(varRange[k]))+" "+nbCores[k]+" "+"./files/variations/Av"+varAv2[k]+"Ra"+varRange[k]+"Fr"+vFb+"/sample"+(str)(z)+".txt "+TimeSteps[t][j]+" "+Windows[t]+" algo "+(str)(t+1)+" ./files/traces/"+folT+"/DATA.txt BP1 "+al+" ./files/results/"+folT+"/n20000Av"+vAb+"Ra"+vRb+"Fr"+vFb+"Co"+nbCores[k]+"a"+(str)(l+len(AlgPar)*t)+"BP1.txt\n")
                            file.write("./files/traces/"+folT+"/"+(str)((t+1)*7)+"D_"+TimeSteps[t][j]+".txt "+nbMach+" "+(str)((int)(varAv2[k])-(int)(varRange[k]))+" "+nbCores[k]+" "+"./files/variations/Av"+varAv2[k]+"Ra"+varRange[k]+"Fr"+vFb+"/sample"+(str)(z)+".txt "+TimeSteps[t][j]+" "+Windows[t]+" algo "+(str)(t+1)+" ./files/traces/"+folT+"/DATA.txt BS1 "+al+" ./files/results/"+folT+"/n20000Av"+vAb+"Ra"+vRb+"Fr"+vFb+"Co"+nbCores[k]+"a"+(str)(l+len(AlgPar)*t)+"BS1.txt\n")
                    for l in range(2):
                        for t in range(version,version+1):
                            file.write("./files/traces/"+folT+"/"+(str)((t+1)*7)+"D_"+TimeSteps[t][j]+".txt "+nbMach+" "+(str)((int)(varAv2[k])-(int)(varRange[k]))+" "+nbCores[k]+" "+"./files/variations/Av"+varAv2[k]+"Ra"+varRange[k]+"Fr"+vFb+"/sample"+(str)(z)+".txt "+TimeSteps[t][j]+" "+Windows[t]+" FF "+(str)(t+1)+" "+(str)(l)+" ./files/results/"+folT+"/n20000Av"+vAb+"Ra"+vRb+"Fr"+vFb+"Co"+nbCores[k]+"FF"+(str)(l+2*t)+".txt\n")
                    for t in range(0):
                        file.write("./files/traces/"+folT+"/"+(str)((t+1)*7)+"D_"+TimeSteps[t][j]+".txt "+nbMach+" "+(str)((int)(varAv2[k])-(int)(varRange[k]))+" "+nbCores[k]+" "+"./files/variations/Av"+varAv2[k]+"Ra"+varRange[k]+"Fr"+vFb+"/sample"+(str)(z)+".txt "+TimeSteps[t][j]+" "+Windows[t]+" algo2 "+(str)(t+1)+" ./files/traces/"+folT+"/DATA.txt ./files/results/"+folT+"/n20000Av"+vAb+"Ra"+vRb+"Fr"+vFb+"Co"+nbCores[k]+"a2"+(str)(t)+".txt\n")
                file.close()
        
        for j in range(len(TimeSteps[1])):
            for i in range(len(synTraces)):
                folT=synTraces[i]
                file=open("./files/arguments/args"+(str)(j)+".txt",'a')
                for l in range(len(AlgPar)):
                    al=AlgPar[l]
                    for t in range(version,version+1):
                        file.write("./files/traces/"+folT+"/n"+nJb+"_"+(str)(j)+".txt "+nbMach+" "+(str)((int)(vAb)-(int)(vRb))+" "+vCb+" "+"./files/variations/Av"+vAb+"Ra"+vRb+"Fr"+vFb+"/sample"+(str)(z)+".txt "+Windows[1-t]+" "+Windows[t]+" algo "+(str)(t+1)+" ./files/traces/"+folT+"/n"+nJb+"DATA.txt BSS "+al+" ./files/results/"+folT+"/n"+nJb+"Av"+vAb+"Ra"+vRb+"Fr"+vFb+"Co"+vCb+"a"+(str)(l+len(AlgPar)*t)+"BSS.txt\n")
                        file.write("./files/traces/"+folT+"/n"+nJb+"_"+(str)(j)+".txt "+nbMach+" "+(str)((int)(vAb)-(int)(vRb))+" "+vCb+" "+"./files/variations/Av"+vAb+"Ra"+vRb+"Fr"+vFb+"/sample"+(str)(z)+".txt "+Windows[1-t]+" "+Windows[t]+" algo "+(str)(t+1)+" ./files/traces/"+folT+"/n"+nJb+"DATA.txt BP1 "+al+" ./files/results/"+folT+"/n"+nJb+"Av"+vAb+"Ra"+vRb+"Fr"+vFb+"Co"+vCb+"a"+(str)(l+len(AlgPar)*t)+"BP1.txt\n")
                        file.write("./files/traces/"+folT+"/n"+nJb+"_"+(str)(j)+".txt "+nbMach+" "+(str)((int)(vAb)-(int)(vRb))+" "+vCb+" "+"./files/variations/Av"+vAb+"Ra"+vRb+"Fr"+vFb+"/sample"+(str)(z)+".txt "+Windows[1-t]+" "+Windows[t]+" algo "+(str)(t+1)+" ./files/traces/"+folT+"/n"+nJb+"DATA.txt BS1 "+al+" ./files/results/"+folT+"/n"+nJb+"Av"+vAb+"Ra"+vRb+"Fr"+vFb+"Co"+vCb+"a"+(str)(l+len(AlgPar)*t)+"BS1.txt\n")
                for l in range(2):
                    for t in range(version,version+1):
                        file.write("./files/traces/"+folT+"/n"+nJb+"_"+(str)(j)+".txt "+nbMach+" "+(str)((int)(vAb)-(int)(vRb))+" "+vCb+" "+"./files/variations/Av"+vAb+"Ra"+vRb+"Fr"+vFb+"/sample"+(str)(z)+".txt "+Windows[1-t]+" "+Windows[t]+" FF "+(str)(t+1)+" "+(str)(l)+" ./files/results/"+folT+"/n"+nJb+"Av"+vAb+"Ra"+vRb+"Fr"+vFb+"Co"+vCb+"FF"+(str)(l+2*t)+".txt\n")
                for t in range(0):
                    file.write("./files/traces/"+folT+"/n"+nJb+"_"+(str)(j)+".txt "+nbMach+" "+(str)((int)(vAb)-(int)(vRb))+" "+vCb+" "+"./files/variations/Av"+vAb+"Ra"+vRb+"Fr"+vFb+"/sample"+(str)(z)+".txt "+Windows[1-t]+" "+Windows[t]+" algo2 "+(str)(t+1)+" ./files/traces/"+folT+"/n"+nJb+"DATA.txt ./files/results/"+folT+"/n"+nJb+"Av"+vAb+"Ra"+vRb+"Fr"+vFb+"Co"+vCb+"a2"+(str)(t)+".txt\n")

                for k in varAv:
                    for l in range(len(AlgPar)):
                        al=AlgPar[l]
                        for t in range(version,version+1):
                            file.write("./files/traces/"+folT+"/n"+nJb+"_"+(str)(j)+".txt "+nbMach+" "+(str)((int)(k)-(int)(vRb))+" "+vCb+" "+"./files/variations/Av"+k+"Ra"+vRb+"Fr"+vFb+"/sample"+(str)(z)+".txt "+Windows[1-t]+" "+Windows[t]+" algo "+(str)(t+1)+" ./files/traces/"+folT+"/n"+nJb+"DATA.txt BSS "+al+" ./files/results/"+folT+"/n"+nJb+"Av"+k+"Ra"+vRb+"Fr"+vFb+"Co"+vCb+"a"+(str)(l+len(AlgPar)*t)+"BSS.txt\n")
                            file.write("./files/traces/"+folT+"/n"+nJb+"_"+(str)(j)+".txt "+nbMach+" "+(str)((int)(k)-(int)(vRb))+" "+vCb+" "+"./files/variations/Av"+k+"Ra"+vRb+"Fr"+vFb+"/sample"+(str)(z)+".txt "+Windows[1-t]+" "+Windows[t]+" algo "+(str)(t+1)+" ./files/traces/"+folT+"/n"+nJb+"DATA.txt BP1 "+al+" ./files/results/"+folT+"/n"+nJb+"Av"+k+"Ra"+vRb+"Fr"+vFb+"Co"+vCb+"a"+(str)(l+len(AlgPar)*t)+"BP1.txt\n")
                            file.write("./files/traces/"+folT+"/n"+nJb+"_"+(str)(j)+".txt "+nbMach+" "+(str)((int)(k)-(int)(vRb))+" "+vCb+" "+"./files/variations/Av"+k+"Ra"+vRb+"Fr"+vFb+"/sample"+(str)(z)+".txt "+Windows[1-t]+" "+Windows[t]+" algo "+(str)(t+1)+" ./files/traces/"+folT+"/n"+nJb+"DATA.txt BS1 "+al+" ./files/results/"+folT+"/n"+nJb+"Av"+k+"Ra"+vRb+"Fr"+vFb+"Co"+vCb+"a"+(str)(l+len(AlgPar)*t)+"BS1.txt\n")
                    for l in range(2):
                        for t in range(version,version+1):
                            file.write("./files/traces/"+folT+"/n"+nJb+"_"+(str)(j)+".txt "+nbMach+" "+(str)((int)(k)-(int)(vRb))+" "+vCb+" "+"./files/variations/Av"+k+"Ra"+vRb+"Fr"+vFb+"/sample"+(str)(z)+".txt "+Windows[1-t]+" "+Windows[t]+" FF "+(str)(t+1)+" "+(str)(l)+" ./files/results/"+folT+"/n"+nJb+"Av"+k+"Ra"+vRb+"Fr"+vFb+"Co"+vCb+"FF"+(str)(l+2*t)+".txt\n")
                    for t in range(0):
                        file.write("./files/traces/"+folT+"/n"+nJb+"_"+(str)(j)+".txt "+nbMach+" "+(str)((int)(k)-(int)(vRb))+" "+vCb+" "+"./files/variations/Av"+k+"Ra"+vRb+"Fr"+vFb+"/sample"+(str)(z)+".txt "+Windows[1-t]+" "+Windows[t]+" algo2 "+(str)(t+1)+" ./files/traces/"+folT+"/n"+nJb+"DATA.txt ./files/results/"+folT+"/n"+nJb+"Av"+k+"Ra"+vRb+"Fr"+vFb+"Co"+vCb+"a2"+(str)(t)+".txt\n")

                for k in varRange:
                    for l in range(len(AlgPar)):
                        al=AlgPar[l]
                        for t in range(version,version+1):
                            file.write("./files/traces/"+folT+"/n"+nJb+"_"+(str)(j)+".txt "+nbMach+" "+(str)((int)(vAb)-(int)(k))+" "+vCb+" "+"./files/variations/Av"+vAb+"Ra"+k+"Fr"+vFb+"/sample"+(str)(z)+".txt "+Windows[1-t]+" "+Windows[t]+" algo "+(str)(t+1)+" ./files/traces/"+folT+"/n"+nJb+"DATA.txt BSS "+al+" ./files/results/"+folT+"/n"+nJb+"Av"+vAb+"Ra"+k+"Fr"+vFb+"Co"+vCb+"a"+(str)(l+len(AlgPar)*t)+"BSS.txt\n")
                            file.write("./files/traces/"+folT+"/n"+nJb+"_"+(str)(j)+".txt "+nbMach+" "+(str)((int)(vAb)-(int)(k))+" "+vCb+" "+"./files/variations/Av"+vAb+"Ra"+k+"Fr"+vFb+"/sample"+(str)(z)+".txt "+Windows[1-t]+" "+Windows[t]+" algo "+(str)(t+1)+" ./files/traces/"+folT+"/n"+nJb+"DATA.txt BP1 "+al+" ./files/results/"+folT+"/n"+nJb+"Av"+vAb+"Ra"+k+"Fr"+vFb+"Co"+vCb+"a"+(str)(l+len(AlgPar)*t)+"BP1.txt\n")
                            file.write("./files/traces/"+folT+"/n"+nJb+"_"+(str)(j)+".txt "+nbMach+" "+(str)((int)(vAb)-(int)(k))+" "+vCb+" "+"./files/variations/Av"+vAb+"Ra"+k+"Fr"+vFb+"/sample"+(str)(z)+".txt "+Windows[1-t]+" "+Windows[t]+" algo "+(str)(t+1)+" ./files/traces/"+folT+"/n"+nJb+"DATA.txt BS1 "+al+" ./files/results/"+folT+"/n"+nJb+"Av"+vAb+"Ra"+k+"Fr"+vFb+"Co"+vCb+"a"+(str)(l+len(AlgPar)*t)+"BS1.txt\n")
                    for l in range(2):
                        for t in range(version,version+1):
                            file.write("./files/traces/"+folT+"/n"+nJb+"_"+(str)(j)+".txt "+nbMach+" "+(str)((int)(vAb)-(int)(k))+" "+vCb+" "+"./files/variations/Av"+vAb+"Ra"+k+"Fr"+vFb+"/sample"+(str)(z)+".txt "+Windows[1-t]+" "+Windows[t]+" FF "+(str)(t+1)+" "+(str)(l)+" ./files/results/"+folT+"/n"+nJb+"Av"+vAb+"Ra"+k+"Fr"+vFb+"Co"+vCb+"FF"+(str)(l+2*t)+".txt\n")
                    for t in range(0):
                        file.write("./files/traces/"+folT+"/n"+nJb+"_"+(str)(j)+".txt "+nbMach+" "+(str)((int)(vAb)-(int)(k))+" "+vCb+" "+"./files/variations/Av"+vAb+"Ra"+k+"Fr"+vFb+"/sample"+(str)(z)+".txt "+Windows[1-t]+" "+Windows[t]+" algo2 "+(str)(t+1)+" ./files/traces/"+folT+"/n"+nJb+"DATA.txt ./files/results/"+folT+"/n"+nJb+"Av"+vAb+"Ra"+k+"Fr"+vFb+"Co"+vCb+"a2"+(str)(t)+".txt\n")
                     
                for k in varFreq:
                    for l in range(len(AlgPar)):
                        al=AlgPar[l]
                        for t in range(version,version+1):
                            file.write("./files/traces/"+folT+"/n"+nJb+"_"+(str)(j)+".txt "+nbMach+" "+(str)((int)(vAb)-(int)(vRb))+" "+vCb+" "+"./files/variations/Av"+vAb+"Ra"+vRb+"Fr"+k+"/sample"+(str)(z)+".txt "+Windows[1-t]+" "+Windows[t]+" algo "+(str)(t+1)+" ./files/traces/"+folT+"/n"+nJb+"DATA.txt BSS "+al+" ./files/results/"+folT+"/n"+nJb+"Av"+vAb+"Ra"+vRb+"Fr"+k+"Co"+vCb+"a"+(str)(l+len(AlgPar)*t)+"BSS.txt\n")
                            file.write("./files/traces/"+folT+"/n"+nJb+"_"+(str)(j)+".txt "+nbMach+" "+(str)((int)(vAb)-(int)(vRb))+" "+vCb+" "+"./files/variations/Av"+vAb+"Ra"+vRb+"Fr"+k+"/sample"+(str)(z)+".txt "+Windows[1-t]+" "+Windows[t]+" algo "+(str)(t+1)+" ./files/traces/"+folT+"/n"+nJb+"DATA.txt BP1 "+al+" ./files/results/"+folT+"/n"+nJb+"Av"+vAb+"Ra"+vRb+"Fr"+k+"Co"+vCb+"a"+(str)(l+len(AlgPar)*t)+"BP1.txt\n")
                            file.write("./files/traces/"+folT+"/n"+nJb+"_"+(str)(j)+".txt "+nbMach+" "+(str)((int)(vAb)-(int)(vRb))+" "+vCb+" "+"./files/variations/Av"+vAb+"Ra"+vRb+"Fr"+k+"/sample"+(str)(z)+".txt "+Windows[1-t]+" "+Windows[t]+" algo "+(str)(t+1)+" ./files/traces/"+folT+"/n"+nJb+"DATA.txt BS1 "+al+" ./files/results/"+folT+"/n"+nJb+"Av"+vAb+"Ra"+vRb+"Fr"+k+"Co"+vCb+"a"+(str)(l+len(AlgPar)*t)+"BS1.txt\n")
                    for l in range(2):
                        for t in range(version,version+1):
                            file.write("./files/traces/"+folT+"/n"+nJb+"_"+(str)(j)+".txt "+nbMach+" "+(str)((int)(vAb)-(int)(vRb))+" "+vCb+" "+"./files/variations/Av"+vAb+"Ra"+vRb+"Fr"+k+"/sample"+(str)(z)+".txt "+Windows[1-t]+" "+Windows[t]+" FF "+(str)(t+1)+" "+(str)(l)+" ./files/results/"+folT+"/n"+nJb+"Av"+vAb+"Ra"+vRb+"Fr"+k+"Co"+vCb+"FF"+(str)(l+2*t)+".txt\n")
                    for t in range(0):
                        file.write("./files/traces/"+folT+"/n"+nJb+"_"+(str)(j)+".txt "+nbMach+" "+(str)((int)(vAb)-(int)(vRb))+" "+vCb+" "+"./files/variations/Av"+vAb+"Ra"+vRb+"Fr"+k+"/sample"+(str)(z)+".txt "+Windows[1-t]+" "+Windows[t]+" algo2 "+(str)(t+1)+" ./files/traces/"+folT+"/n"+nJb+"DATA.txt ./files/results/"+folT+"/n"+nJb+"Av"+vAb+"Ra"+vRb+"Fr"+k+"Co"+vCb+"a2"+(str)(t)+".txt\n")
                    
                for k in range(len(nbCores)):
                    for l in range(len(AlgPar)):
                        al=AlgPar[l]
                        for t in range(version,version+1):
                            file.write("./files/traces/"+folT+"/n"+nJb+"_"+(str)(j)+".txt "+nbMach+" "+(str)((int)(varAv2[k])-(int)(varRange[k]))+" "+nbCores[k]+" "+"./files/variations/Av"+varAv2[k]+"Ra"+varRange[k]+"Fr"+vFb+"/sample"+(str)(z)+".txt "+Windows[1-t]+" "+Windows[t]+" algo "+(str)(t+1)+" ./files/traces/"+folT+"/n"+nJb+"DATA.txt BSS "+al+" ./files/results/"+folT+"/n"+nJb+"Av"+vAb+"Ra"+vRb+"Fr"+vFb+"Co"+nbCores[k]+"a"+(str)(l+len(AlgPar)*t)+"BSS.txt\n")
                            file.write("./files/traces/"+folT+"/n"+nJb+"_"+(str)(j)+".txt "+nbMach+" "+(str)((int)(varAv2[k])-(int)(varRange[k]))+" "+nbCores[k]+" "+"./files/variations/Av"+varAv2[k]+"Ra"+varRange[k]+"Fr"+vFb+"/sample"+(str)(z)+".txt "+Windows[1-t]+" "+Windows[t]+" algo "+(str)(t+1)+" ./files/traces/"+folT+"/n"+nJb+"DATA.txt BP1 "+al+" ./files/results/"+folT+"/n"+nJb+"Av"+vAb+"Ra"+vRb+"Fr"+vFb+"Co"+nbCores[k]+"a"+(str)(l+len(AlgPar)*t)+"BP1.txt\n")
                            file.write("./files/traces/"+folT+"/n"+nJb+"_"+(str)(j)+".txt "+nbMach+" "+(str)((int)(varAv2[k])-(int)(varRange[k]))+" "+nbCores[k]+" "+"./files/variations/Av"+varAv2[k]+"Ra"+varRange[k]+"Fr"+vFb+"/sample"+(str)(z)+".txt "+Windows[1-t]+" "+Windows[t]+" algo "+(str)(t+1)+" ./files/traces/"+folT+"/n"+nJb+"DATA.txt BS1 "+al+" ./files/results/"+folT+"/n"+nJb+"Av"+vAb+"Ra"+vRb+"Fr"+vFb+"Co"+nbCores[k]+"a"+(str)(l+len(AlgPar)*t)+"BS1.txt\n")
                    for l in range(2):
                        for t in range(version,version+1):
                            file.write("./files/traces/"+folT+"/n"+nJb+"_"+(str)(j)+".txt "+nbMach+" "+(str)((int)(varAv2[k])-(int)(varRange[k]))+" "+nbCores[k]+" "+"./files/variations/Av"+varAv2[k]+"Ra"+varRange[k]+"Fr"+vFb+"/sample"+(str)(z)+".txt "+Windows[1-t]+" "+Windows[t]+" FF "+(str)(t+1)+" "+(str)(l)+" ./files/results/"+folT+"/n"+nJb+"Av"+vAb+"Ra"+vRb+"Fr"+vFb+"Co"+nbCores[k]+"FF"+(str)(l+2*t)+".txt\n")
                    for t in range(0):
                        file.write("./files/traces/"+folT+"/n"+nJb+"_"+(str)(j)+".txt "+nbMach+" "+(str)((int)(varAv2[k])-(int)(varRange[k]))+" "+nbCores[k]+" "+"./files/variations/Av"+varAv2[k]+"Ra"+varRange[k]+"Fr"+vFb+"/sample"+(str)(z)+".txt "+Windows[1-t]+" "+Windows[t]+" algo2 "+(str)(t+1)+" ./files/traces/"+folT+"/n"+nJb+"DATA.txt ./files/results/"+folT+"/n"+nJb+"Av"+vAb+"Ra"+vRb+"Fr"+vFb+"Co"+nbCores[k]+"a2"+(str)(t)+".txt\n")
                    

                for k in nbJobs:
                    for l in range(len(AlgPar)):
                        al=AlgPar[l]
                        for t in range(version,version+1):
                            file.write("./files/traces/"+folT+"/n"+k+"_"+(str)(j)+".txt "+nbMach+" "+(str)((int)(vAb)-(int)(vRb))+" "+vCb+" "+"./files/variations/Av"+vAb+"Ra"+vRb+"Fr"+vFb+"/sample"+(str)(z)+".txt "+Windows[1-t]+" "+Windows[t]+" algo "+(str)(t+1)+" ./files/traces/"+folT+"/n"+k+"DATA.txt BSS "+al+" ./files/results/"+folT+"/n"+k+"Av"+vAb+"Ra"+vRb+"Fr"+vFb+"Co"+vCb+"a"+(str)(l+len(AlgPar)*t)+"BSS.txt\n")
                            file.write("./files/traces/"+folT+"/n"+k+"_"+(str)(j)+".txt "+nbMach+" "+(str)((int)(vAb)-(int)(vRb))+" "+vCb+" "+"./files/variations/Av"+vAb+"Ra"+vRb+"Fr"+vFb+"/sample"+(str)(z)+".txt "+Windows[1-t]+" "+Windows[t]+" algo "+(str)(t+1)+" ./files/traces/"+folT+"/n"+k+"DATA.txt BP1 "+al+" ./files/results/"+folT+"/n"+k+"Av"+vAb+"Ra"+vRb+"Fr"+vFb+"Co"+vCb+"a"+(str)(l+len(AlgPar)*t)+"BP1.txt\n")
                            file.write("./files/traces/"+folT+"/n"+k+"_"+(str)(j)+".txt "+nbMach+" "+(str)((int)(vAb)-(int)(vRb))+" "+vCb+" "+"./files/variations/Av"+vAb+"Ra"+vRb+"Fr"+vFb+"/sample"+(str)(z)+".txt "+Windows[1-t]+" "+Windows[t]+" algo "+(str)(t+1)+" ./files/traces/"+folT+"/n"+k+"DATA.txt BS1 "+al+" ./files/results/"+folT+"/n"+k+"Av"+vAb+"Ra"+vRb+"Fr"+vFb+"Co"+vCb+"a"+(str)(l+len(AlgPar)*t)+"BS1.txt\n")
                    for l in range(2):
                        for t in range(version,version+1):
                            file.write("./files/traces/"+folT+"/n"+k+"_"+(str)(j)+".txt "+nbMach+" "+(str)((int)(vAb)-(int)(vRb))+" "+vCb+" "+"./files/variations/Av"+vAb+"Ra"+vRb+"Fr"+vFb+"/sample"+(str)(z)+".txt "+Windows[1-t]+" "+Windows[t]+" FF "+(str)(t+1)+" "+(str)(l)+" ./files/results/"+folT+"/n"+k+"Av"+vAb+"Ra"+vRb+"Fr"+vFb+"Co"+vCb+"FF"+(str)(l+2*t)+".txt\n")
                    for t in range(0):
                        file.write("./files/traces/"+folT+"/n"+k+"_"+(str)(j)+".txt "+nbMach+" "+(str)((int)(vAb)-(int)(vRb))+" "+vCb+" "+"./files/variations/Av"+vAb+"Ra"+vRb+"Fr"+vFb+"/sample"+(str)(z)+".txt "+Windows[1-t]+" "+Windows[t]+" algo2 "+(str)(t+1)+" ./files/traces/"+folT+"/n"+k+"DATA.txt "+" ./files/results/"+folT+"/n"+k+"Av"+vAb+"Ra"+vRb+"Fr"+vFb+"Co"+vCb+"a2"+(str)(t)+".txt\n")
                    
    
                file.close()
        

if("launch" in TODO):
    print("Launch")
    os.chdir("./files/results/")
    os.system("find . -type f -delete")
    os.chdir("../..")
    file=open("launch",'w')
    for i in range (nbVar-1):
        file.write("./SIM \"./files/arguments/args"+(str)(i)+".txt\" &\n")
    file.write("./SIM \"./files/arguments/args"+(str)(nbVar-1)+".txt\"")
    file.close()
    os.system("bash launch")

if("plots" in TODO):
    print("Generate plots")
    os.chdir("./plots/")
    os.system("find . -type f -delete")
    os.chdir("..")
    nJb="20000"
    for i in plots:
        typ="vAb "
        Var=""
        for k in range(len(varAvT)):
            Var+=varAvT[k]+" "
            
        for z in objectives:
            os.system("python3 plotter.py "+i+" "+z+" "+typ+vAb+" "+vRb+" "+vFb+" "+nJb+" "+vCb+" "+(str)(naLg)+" "+(str)(len(varAvT))+" "+Var)
        
        typ="vRb "
        Var=""
        for k in range(len(varRangeT)):
            Var+=varRangeT[k]+" "
            
        for z in objectives:
            os.system("python3 plotter.py "+i+" "+z+" "+typ+vAb+" "+vRb+" "+vFb+" "+nJb+" "+vCb+" "+(str)(naLg)+" "+(str)(len(varRangeT))+" "+Var)
        
        typ="vFb "
        Var=""
        for k in range(len(varFreqT)):
            Var+=varFreqT[k]+" "
            
        for z in objectives:
            os.system("python3 plotter.py "+i+" "+z+" "+typ+vAb+" "+vRb+" "+vFb+" "+nJb+" "+vCb+" "+(str)(naLg)+" "+(str)(len(varFreqT))+" "+Var)
        
        
        typ="vCb "
        Var=""
        for k in range(len(nbCoresT)):
            Var+=nbCoresT[k]+" "
            
        for z in objectives:
            os.system("python3 plotter.py "+i+" "+z+" "+typ+vAb+" "+vRb+" "+vFb+" "+nJb+" "+vCb+" "+(str)(naLg)+" "+(str)(len(varFreqT))+" "+Var)
        
            
        typ="nJb "
        if (i in synTraces): 
            Var=""
            for k in range(len(nbJobsT)):
                Var+=nbJobsT[k]+" "
                
            for z in objectives:
                os.system("python3 plotter.py "+i+" "+z+" "+typ+vAb+" "+vRb+" "+vFb+" "+nJb+" "+vCb+" "+(str)(naLg)+" "+(str)(len(nbJobsT))+" "+Var)






