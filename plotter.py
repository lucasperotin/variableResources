import sys
import matplotlib
import matplotlib.pyplot as plt
import glob, os
import numpy as np


def plotplot(folt,obj,typ,vAb,vRb,vFb,nJb,vCb,naLg,Var):
    loc="./files/results/"
    figname="./plots/"+typ+"/"+obj+"/"+folt+".pdf"
    print(figname)
    print(naLg)
    temp=0
    xlab=""
    nbFF=2
    iObj=0
    iObjNorm=3
    if (obj=="util"):
        iObj=4
        obj="Goodput"
    elif(obj=="utiltot"):
        iObj=5
        obj="Goodput"
    elif(obj=="Waste"):
        iObj=6
        obj="AbortedVolume"
    elif(obj=="maxSt"):
        iObj=7
        obj="MaximumStretch"
    elif(obj=="avgSt"):
        iObj=8
        obj="AverageStretch"
    elif(obj=="perc"):
        iObj=9
        obj="PercentageCompleted"
    elif(obj=="avgLength"):
        iObj=10
        obj="AbortedVolume"
        
    #print(folt+" "+obj+" "+typ+" "+vAb+" "+vRb+" "+vFb+" "+nJb+" "+(str)(naLg)+" "+str(Var).strip('[]')) 
    y=[[[] for j in range(len(Var))] for i in range(3*naLg+nbFF)]
    
    if(typ=="vAb"):
        for i in range(len(Var)):
            for j in range(naLg):    
                xi=[]
                cnti=0
                file=open(loc+folt+"/n"+nJb+"Av"+Var[i]+"Ra"+vRb+"Fr"+vFb+"Co"+vCb+"a"+(str)(j)+"BP1.txt",'r')
                Lines=file.readlines()
                for l in range(len(Lines)):
                    line=Lines[l].split(" ")
                    if(line[2][0]!='F'):
                        temp=(float) (line[iObj])
                        if(iObj<7):
                            temp/=(float)(line[iObjNorm])
                        xi.append(temp)
                        cnti+=1
                    else:
                        print("ERR")
                if(cnti>0):
                      cnti+=0
                y[j][i]=xi
            
            for j in range(naLg):    
                xi=[]
                cnti=0
                file=open(loc+folt+"/n"+nJb+"Av"+Var[i]+"Ra"+vRb+"Fr"+vFb+"Co"+vCb+"a"+(str)(j)+"BSS.txt",'r')
                Lines=file.readlines()
                for l in range(len(Lines)):
                    line=Lines[l].split(" ")
                    if(line[2][0]!='F'):
                        temp=(float) (line[iObj])
                        if(iObj<7):
                            temp/=(float)(line[iObjNorm])
                        xi.append(temp)
                        cnti+=1
                    else:
                        print("ERR")
                if(cnti>0):
                      cnti+=0
                y[j+naLg][i]=xi
                
            for j in range(naLg):    
                xi=[]
                cnti=0
                file=open(loc+folt+"/n"+nJb+"Av"+Var[i]+"Ra"+vRb+"Fr"+vFb+"Co"+vCb+"a"+(str)(j)+"BS1.txt",'r')
                Lines=file.readlines()
                for l in range(len(Lines)):
                    line=Lines[l].split(" ")
                    if(line[2][0]!='F'):
                        temp=(float) (line[iObj])
                        if(iObj<7):
                            temp/=(float)(line[iObjNorm])
                        xi.append(temp)
                        cnti+=1
                    else:
                        print("ERR")
                if(cnti>0):
                      cnti+=0
                y[j+2*naLg][i]=xi
                
            for j in range(nbFF):
                xi=[]
                cnti=0
                file=open(loc+folt+"/n"+nJb+"Av"+Var[i]+"Ra"+vRb+"Fr"+vFb+"Co"+vCb+"FF"+(str)(j)+".txt",'r')
                Lines=file.readlines()
                for l in range(len(Lines)):
                    line=Lines[l].split(" ")
                    if(line[2][1]!='A'):
                        temp=(float) (line[iObj])
                        if(iObj<7):
                            temp/=(float)(line[iObjNorm])
                        xi.append(temp)
                        cnti+=1
                    else:
                        print("ERR")
                if(cnti>0):
                      cnti+=0
                y[j+3*naLg][i]=xi
            
            # xi=[]
            # cnti=0
            # file=open(loc+folt+"/n"+nJb+"Av"+Var[i]+"Ra"+vRb+"Fr"+vFb+"Co"+vCb+"a20.txt",'r')
            # Lines=file.readlines()
            # for l in range(len(Lines)):
            #     line=Lines[l].split(" ")
            #     if(line[2][1]!='A'):
            #         temp=(float) (line[iObj])
            #         if(iObj<7):
            #             temp/=(float)(line[iObjNorm])
            #         xi.append(temp)
            #         cnti+=1
            #     else:
            #         print("ERR")
            # if(cnti>0):
            #       cnti+=0
            # y[nbFF+3*naLg][i]=xi
        
          
        # naming the x axis
        xlab='Average Number of Machine'
    
    if(typ=="vCb"):
        for i in range(len(Var)):
            for j in range(naLg):    
                xi=[]
                cnti=0
                file=open(loc+folt+"/n"+nJb+"Av"+vAb+"Ra"+vRb+"Fr"+vFb+"Co"+Var[i]+"a"+(str)(j)+"BP1.txt",'r')
                Lines=file.readlines()
                for l in range(len(Lines)):
                    line=Lines[l].split(" ")
                    if(line[2][0]!='F'):
                        temp=(float) (line[iObj])
                        if(iObj<7):
                            temp/=(float)(line[iObjNorm])
                        xi.append(temp)
                        cnti+=1
                    else:
                        print("ERR")
                if(cnti>0):
                      cnti+=0
                y[j][i]=xi
            
            for j in range(naLg):    
                xi=[]
                cnti=0
                file=open(loc+folt+"/n"+nJb+"Av"+vAb+"Ra"+vRb+"Fr"+vFb+"Co"+Var[i]+"a"+(str)(j)+"BSS.txt",'r')
                Lines=file.readlines()
                for l in range(len(Lines)):
                    line=Lines[l].split(" ")
                    if(line[2][0]!='F'):
                        temp=(float) (line[iObj])
                        if(iObj<7):
                            temp/=(float)(line[iObjNorm])
                        xi.append(temp)
                        cnti+=1
                    else:
                        print("ERR")
                if(cnti>0):
                      cnti+=0
                y[j+naLg][i]=xi
            
            for j in range(naLg):    
                xi=[]
                cnti=0
                file=open(loc+folt+"/n"+nJb+"Av"+vAb+"Ra"+vRb+"Fr"+vFb+"Co"+Var[i]+"a"+(str)(j)+"BS1.txt",'r')
                Lines=file.readlines()
                for l in range(len(Lines)):
                    line=Lines[l].split(" ")
                    if(line[2][0]!='F'):
                        temp=(float) (line[iObj])
                        if(iObj<7):
                            temp/=(float)(line[iObjNorm])
                        xi.append(temp)
                        cnti+=1
                    else:
                        print("ERR")
                if(cnti>0):
                      cnti+=0
                y[j+2*naLg][i]=xi
                
            for j in range(nbFF):
                xi=[]
                cnti=0
                file=open(loc+folt+"/n"+nJb+"Av"+vAb+"Ra"+vRb+"Fr"+vFb+"Co"+Var[i]+"FF"+(str)(j)+".txt",'r')
                Lines=file.readlines()
                for l in range(len(Lines)):
                    line=Lines[l].split(" ")
                    if(line[2][1]!='A'):
                        temp=(float) (line[iObj])
                        if(iObj<7):
                            temp/=(float)(line[iObjNorm])
                        xi.append(temp)
                        cnti+=1
                    else:
                        print("ERR")
                if(cnti>0):
                      cnti+=0
                y[j+3*naLg][i]=xi
                
            
            # xi=[]
            # cnti=0
            # file=open(loc+folt+"/n"+nJb+"Av"+vAb+"Ra"+vRb+"Fr"+vFb+"Co"+Var[i]+"a20.txt",'r')
            # Lines=file.readlines()
            # for l in range(len(Lines)):
            #     line=Lines[l].split(" ")
            #     if(line[2][1]!='A'):
            #         temp=(float) (line[iObj])
            #         if(iObj<7):
            #             temp/=(float)(line[iObjNorm])
            #         xi.append(temp)
            #         cnti+=1
            #     else:
            #         print("ERR")
            # if(cnti>0):
            #       cnti+=0
            # y[nbFF+3*naLg][i]=xi
        
          
        # naming the x axis
        xlab='Number of Cores'
        
    if(typ=="vRb"):
        for i in range(len(Var)):
            for j in range(naLg):   
                xi=[]
                cnti=0
                file=open(loc+folt+"/n"+nJb+"Av"+vAb+"Ra"+Var[i]+"Fr"+vFb+"Co"+vCb+"a"+(str)(j)+"BP1.txt",'r')
                Lines=file.readlines()
                for l in range(len(Lines)):
                    line=Lines[l].split(" ")
                    if(line[2][0]!='F'):
                        temp=(float) (line[iObj])
                        if(iObj<7):
                            temp/=(float)(line[iObjNorm])
                        xi.append(temp)
                        cnti+=1
                    else:
                        print("ERR")
                if(cnti>0):
                      cnti+=0
                y[j][i]=xi
            
            for j in range(naLg):   
                xi=[]
                cnti=0
                file=open(loc+folt+"/n"+nJb+"Av"+vAb+"Ra"+Var[i]+"Fr"+vFb+"Co"+vCb+"a"+(str)(j)+"BSS.txt",'r')
                Lines=file.readlines()
                for l in range(len(Lines)):
                    line=Lines[l].split(" ")
                    if(line[2][0]!='F'):
                        temp=(float) (line[iObj])
                        if(iObj<7):
                            temp/=(float)(line[iObjNorm])
                        xi.append(temp)
                        cnti+=1
                    else:
                        print("ERR")
                if(cnti>0):
                      cnti+=0
                y[j+naLg][i]=xi
                
            
            for j in range(naLg):   
                xi=[]
                cnti=0
                file=open(loc+folt+"/n"+nJb+"Av"+vAb+"Ra"+Var[i]+"Fr"+vFb+"Co"+vCb+"a"+(str)(j)+"BS1.txt",'r')
                Lines=file.readlines()
                for l in range(len(Lines)):
                    line=Lines[l].split(" ")
                    if(line[2][0]!='F'):
                        temp=(float) (line[iObj])
                        if(iObj<7):
                            temp/=(float)(line[iObjNorm])
                        xi.append(temp)
                        cnti+=1
                    else:
                        print("ERR")
                if(cnti>0):
                      cnti+=0
                y[j+2*naLg][i]=xi
                
            for j in range(nbFF):
                xi=[]
                cnti=0
                file=open(loc+folt+"/n"+nJb+"Av"+vAb+"Ra"+Var[i]+"Fr"+vFb+"Co"+vCb+"FF"+(str)(j)+".txt",'r')
                Lines=file.readlines()
                for l in range(len(Lines)):
                    line=Lines[l].split(" ")
                    if(line[2][1]!='A'):
                        temp=(float) (line[iObj])
                        if(iObj<7):
                            temp/=(float)(line[iObjNorm])
                        xi.append(temp)
                        cnti+=1
                    else:
                        print("ERR")
                if(cnti>0):
                      cnti+=0
                y[j+3*naLg][i]=xi
                
            
            # xi=[]
            # cnti=0
            # file=open(loc+folt+"/n"+nJb+"Av"+vAb+"Ra"+Var[i]+"Fr"+vFb+"Co"+vCb+"a20.txt",'r')
            # Lines=file.readlines()
            # for l in range(len(Lines)):
            #     line=Lines[l].split(" ")
            #     if(line[2][1]!='A'):
            #         temp=(float) (line[iObj])
            #         if(iObj<7):
            #             temp/=(float)(line[iObjNorm])
            #         xi.append(temp)
            #         cnti+=1
            #     else:
            #         print("ERR")
            # if(cnti>0):
            #       cnti+=0
            # y[nbFF+3*naLg][i]=xi
        
        # x axis values
        # corresponding y axis values
          
        # naming the x axis
        xlab='Range of the machines'
        
    if(typ=="vFb"):
        for i in range(len(Var)):
            for j in range(naLg):     
                xi=[]
                cnti=0
                file=open(loc+folt+"/n"+nJb+"Av"+vAb+"Ra"+vRb+"Fr"+Var[i]+"Co"+vCb+"a"+(str)(j)+"BP1.txt",'r')
                Lines=file.readlines()
                for l in range(len(Lines)):
                    line=Lines[l].split(" ")
                    if(line[2][0]!='F'):
                        temp=(float) (line[iObj])
                        if(iObj<7):
                            temp/=(float)(line[iObjNorm])
                        xi.append(temp)
                        cnti+=1
                    else:
                        print("ERR")
                if(cnti>0):
                      cnti+=0
                y[j][i]=xi
            
            for j in range(naLg):     
                xi=[]
                cnti=0
                file=open(loc+folt+"/n"+nJb+"Av"+vAb+"Ra"+vRb+"Fr"+Var[i]+"Co"+vCb+"a"+(str)(j)+"BSS.txt",'r')
                Lines=file.readlines()
                for l in range(len(Lines)):
                    line=Lines[l].split(" ")
                    if(line[2][0]!='F'):
                        temp=(float) (line[iObj])
                        if(iObj<7):
                            temp/=(float)(line[iObjNorm])
                        xi.append(temp)
                        cnti+=1
                    else:
                        print("ERR")
                if(cnti>0):
                      cnti+=0
                y[j+naLg][i]=xi
            
            
            for j in range(naLg):     
                xi=[]
                cnti=0
                file=open(loc+folt+"/n"+nJb+"Av"+vAb+"Ra"+vRb+"Fr"+Var[i]+"Co"+vCb+"a"+(str)(j)+"BS1.txt",'r')
                Lines=file.readlines()
                for l in range(len(Lines)):
                    line=Lines[l].split(" ")
                    if(line[2][0]!='F'):
                        temp=(float) (line[iObj])
                        if(iObj<7):
                            temp/=(float)(line[iObjNorm])
                        xi.append(temp)
                        cnti+=1
                    else:
                        print("ERR")
                if(cnti>0):
                      cnti+=0
                y[j+2*naLg][i]=xi
                
            for j in range(nbFF):
                xi=[]
                cnti=0
                file=open(loc+folt+"/n"+nJb+"Av"+vAb+"Ra"+vRb+"Fr"+Var[i]+"Co"+vCb+"FF"+(str)(j)+".txt",'r')
                Lines=file.readlines()
                for l in range(len(Lines)):
                    line=Lines[l].split(" ")
                    if(line[2][1]!='A'):
                        temp=(float) (line[iObj])
                        if(iObj<7):
                            temp/=(float)(line[iObjNorm])
                        xi.append(temp)
                        cnti+=1
                    else:
                        print("ERR") 
                y[j+3*naLg][i]=xi
            
            # xi=[]
            # cnti=0
            # file=open(loc+folt+"/n"+nJb+"Av"+vAb+"Ra"+vRb+"Fr"+Var[i]+"Co"+vCb+"a20.txt",'r')
            # Lines=file.readlines()
            # for l in range(len(Lines)):
            #     line=Lines[l].split(" ")
            #     if(line[2][1]!='A'):
            #         temp=(float) (line[iObj])
            #         if(iObj<7):
            #             temp/=(float)(line[iObjNorm])
            #         xi.append(temp)
            #         cnti+=1
            #     else:
            #         print("ERR")
            # if(cnti>0):
            #       cnti+=0
            # y[nbFF+3*naLg][i]=xi
        
        # x axis values
        # corresponding y axis values
          
        # naming the x axis
        xlab='Period of Machine Change (in seconds)'
        
    if(typ=="nJb"):
        
        for i in range(len(Var)):
            for j in range(naLg):   
                xi=[]
                cnti=0
                file=open(loc+folt+"/n"+Var[i]+"Av"+vAb+"Ra"+vRb+"Fr"+vFb+"Co"+vCb+"a"+(str)(j)+"BP1.txt",'r')
                Lines=file.readlines()
                for l in range(len(Lines)):
                    line=Lines[l].split(" ")
                    if(line[2][0]!='F'):
                        temp=(float) (line[iObj])
                        if(iObj<7):
                            temp/=(float)(line[iObjNorm])
                        xi.append(temp)
                        cnti+=1
                    else:
                        print("ERR")
                if(cnti>0):
                      cnti+=0
                y[j][i]=xi
            
            for j in range(naLg):   
                xi=[]
                cnti=0
                file=open(loc+folt+"/n"+Var[i]+"Av"+vAb+"Ra"+vRb+"Fr"+vFb+"Co"+vCb+"a"+(str)(j)+"BSS.txt",'r')
                Lines=file.readlines()
                for l in range(len(Lines)):
                    line=Lines[l].split(" ")
                    if(line[2][0]!='F'):
                        temp=(float) (line[iObj])
                        if(iObj<7):
                            temp/=(float)(line[iObjNorm])
                        xi.append(temp)
                        cnti+=1
                    else:
                        print("ERR")  
                y[j+naLg][i]=xi
                
            
            for j in range(naLg):   
                xi=[]
                cnti=0
                file=open(loc+folt+"/n"+Var[i]+"Av"+vAb+"Ra"+vRb+"Fr"+vFb+"Co"+vCb+"a"+(str)(j)+"BS1.txt",'r')
                Lines=file.readlines()
                for l in range(len(Lines)):
                    line=Lines[l].split(" ")
                    if(line[2][0]!='F'):
                        temp=(float) (line[iObj])
                        if(iObj<7):
                            temp/=(float)(line[iObjNorm])
                        xi.append(temp)
                        cnti+=1
                    else:
                        print("ERR")
                if(cnti>0):
                      cnti+=0
                y[j+2*naLg][i]=xi
            
            for j in range(nbFF):
                xi=[]
                cnti=0
                file=open(loc+folt+"/n"+Var[i]+"Av"+vAb+"Ra"+vRb+"Fr"+vFb+"Co"+vCb+"FF"+(str)(j)+".txt",'r')
                Lines=file.readlines()
                for l in range(len(Lines)):
                    line=Lines[l].split(" ")
                    if(line[2][1]!='A'):
                        temp=(float) (line[iObj])
                        if(iObj<7):
                            temp/=(float)(line[iObjNorm])
                        xi.append(temp)
                        cnti+=1
                    else:
                        print("ERR")
                if(cnti>0):
                      cnti+=0
                y[j+3*naLg][i]=xi
            
            # xi=[]
            # cnti=0
            # file=open(loc+folt+"/n"+Var[i]+"Av"+vAb+"Ra"+vRb+"Fr"+vFb+"Co"+vCb+"a20.txt",'r')
            # Lines=file.readlines()
            # for l in range(len(Lines)):
            #     line=Lines[l].split(" ")
            #     if(line[2][1]!='A'):
            #         temp=(float) (line[iObj])
            #         if(iObj<7):
            #             temp/=(float)(line[iObjNorm])
            #         xi.append(temp)
            #         cnti+=1
            #     else:
            #         print("ERR")
            # if(cnti>0):
            #       cnti+=0
            # y[nbFF+3*naLg][i]=xi
        
        # x axis values
        # corresponding y axis values
        xlab='Number of Jobs'
    
    #LegAlg=["sDist-LMUsev1","LDist-LMUsev1","sDist-LMUsev2","LDist-LMUsev2"]
    #LegAlg=["RiskAware","LDist-LMUsev2"]
    labels = ["PackedTargetASAP", "TargetForStretch", "TargetASAP", "FirstFitOrdered", "FirstFitUnordered"]
    labels = ["FirstFitAware", "FirstFitUnaware", "TargetStretch", "TargetASAP", "PackedTargetASAP"]
    colors = ["red", "blue", "green", "orange", "purple"]
    y[0], y[1], y[2], y[3], y[4] = y[3], y[4], y[1], y[2], y[0]
    fig, ax = plt.subplots()
    artists = []
    avg_values = {name: [] for name in labels}
    
    for j, name in enumerate(labels):
        positions = np.arange(len(y[j])) + j / (len(labels) + 1)
        box = ax.boxplot(y[j], positions=positions, widths=1 / (len(labels) + 1),
                         labels=["" for _ in range(len(y[j]))], showfliers=False,
                         patch_artist=True, boxprops=dict(facecolor=colors[j], edgecolor=colors[j]),
                         whiskerprops=dict(color=colors[j]), capprops=dict(color=colors[j]),
                         medianprops=dict(color="None"), whis=(10,90))
    
        artists.append(plt.Rectangle((0, 0), 1, 1, fc=colors[j], edgecolor=colors[j], linewidth=2, label=name))
    
        for i in range(len(y[j])):
            avg_values[name].append(np.nanmean(y[j][i]))
            ax.plot(positions[i], np.nanmean(y[j][i]), 'x', color='black', markersize=3)
    
    ax.set_xticks(np.arange(len(y[0])) + 0.5, minor=False)
    ax.set_xticklabels(Var, ha='center', rotation=0)
    ax.set_xlabel(xlab)
    ax.set_ylabel(obj)
    #ax.legend(handles=artists, loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=5)
    
    plt.savefig(figname)
    legend_fig, legend_ax = plt.subplots(figsize=(10, 1))
    legend_ax.axis('off')
    legend_ax.legend(handles=artists, loc='center', ncol=5, frameon=False)
    
    legend_fig.savefig("legend.pdf", bbox_inches='tight')
    
              
folt=sys.argv[1]
obj=sys.argv[2]
typ=sys.argv[3]
vAb=sys.argv[4]
vRb=sys.argv[5]
vFb=sys.argv[6]
nJb=sys.argv[7]
vCb=sys.argv[8]
naLg=(int)(sys.argv[9])
Var=[]
l=(int) (sys.argv[10])
for i in range(l):
    Var.append(sys.argv[11+i])

plotplot(folt,obj,typ,vAb,vRb,vFb,nJb,vCb,naLg,Var)
	
# function to show the plot 
