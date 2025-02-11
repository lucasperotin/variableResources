#include <iostream>
#include <vector>
#include <queue>
#include <string>
#include <fstream>
#include <utility>
#include <algorithm>   
#include <math.h>      
#include <random>

using namespace std;

class Task
{
public:
    Task(string n, double t, long p, double r, double i) : name(n), time(t), np(p), release(r), inifacTime(i) {}
    void setMachine(long m)
    {
        machine=m;
    }
    long getMachine()
    {
        return machine;
    }
    void setStretch(double s)
    {
        stretch=s;
    }
    double getStretch()
    {
        return stretch;
    }
    void setFacTime(double s)
    {
        facTime=s;
    }
    double getFacTime()
    {
        return facTime;
    }
    void setStart(double s)
    {
        start=s;
    }
    double getStart()
    {
        return start;
    }
    void setRStart(double s)
    {
        Rstart=s;
    }
    double getRStart()
    {
        return Rstart;
    }
    void setEnd(double e)
    {
        end=e;
    }
    double getEnd()
    {
        return end;
    }
    void setPerc(double e)
    {
        perc=e;
    }
    double getPerc()
    {
        return perc;
    }
    void setStatus(string s)
    {
        status=s;
    }
    string getStatus()
    {
        return status;
    }
    void setIndex(long i)
    {
        index=i;
    }
    long getIndex()
    {
        return index;
    }
    string name;
    double time;
    long np;
    double release;
    double inifacTime;

private:
    long machine;
    double stretch;
    string status;
    double start;
    double Rstart;
    double end;
    long index;
    double facTime;
    double perc;
};

class Machine
{
public:
    Machine(long n, long i) : nodes(n), index(i) {}
    void setAlloc(vector<pair<long,double>> a)
    {
        alloc=a;
    }
    vector<pair<long,double>> getAlloc()
    {
        return alloc;
    }
    void setUtil(long u)
    {
        util=u;
    }
    long getUtil()
    {
        return util;
    }
    void setWait(long s){
        waitSize=s;
    }
    long getWait(){
        return waitSize;
    }
    long nodes;
    long index;

private:
    vector<pair<long,double>> alloc;
    long util;
    long waitSize;
};

class Event
{
public:
    Event(double t, long rt, long m, string tp) : time(t), relatedTask(rt), machine(m), type(tp) {}
    double time;
    long relatedTask;
    long machine;
    string type;
};

auto cmpEvent = [](Event left, Event right)
{
    return left.time > right.time or (left.time==right.time and left.type>right.type) or 
                        (left.time==right.time and left.type==right.type and left.machine>right.machine);
};

auto cmpTask=[](Task left, Task right)
{
    return left.release > right.release;
};

auto cmpInd=[](long left, long right)
{
    return left > right;
};

vector<Task> jobs;
vector<Machine> machines;
double waste=0;
double countW=0;

long MSpace=0;

vector<long>quantiles;

priority_queue<Task,vector<Task>,decltype(cmpTask)> jobQueue(cmpTask);
priority_queue<Task,vector<Task>,decltype(cmpTask)> tmpjobQueue(cmpTask);
priority_queue<Event,vector<Event>,decltype(cmpEvent)> eventQueue(cmpEvent);
priority_queue<long,vector<long>,decltype(cmpInd)> indexes(cmpInd);

void printMachine(long ind,double cTime)
{
    long p;
    double t;
    int count=0;
    vector<pair<long,double>> alloc=machines[ind].getAlloc();
    cout << "Printing Machine " << ind << " of size " << alloc.size() << "\n";
    for (int j=0; j<alloc.size(); j++)
    {
        p=get<0>(alloc[j]);
        t=get<1>(alloc[j]);
        cout << p << ' ' << t << "\n";
    }
    cout << "\n";
    
    for (int i =0;i<jobs.size();i++){
        if(jobs[i].getStatus()=="started" and jobs[i].getEnd()>cTime){
            cout << "aya "<<jobs[i].name << " " <<jobs[i].np<< " " <<jobs[i].getRStart() << " "<<jobs[i].getEnd() << "\n";
        }
    }
}

void addQuantiles(string quantfile){
    
    ifstream quanStr(quantfile,ios::in);
    long lenght;
    
    while(quanStr >> lenght){
        //cout << lenght << "\n";
        quantiles.push_back(lenght);
    }
}

double findQuantile(long length){
    int i;
    int maxi=0;
   

    for (i=0;i<quantiles.size();i++){
        if(length<quantiles[i]){
            maxi=i;
            break;
        }
    }
    

    if(quantiles.size()>0 and length>quantiles[quantiles.size()-1]){
        maxi=quantiles.size();
    }
    //cout << "Affect " << length <<" " << maxi << "\n";
    
    return(1-(double)(maxi)/1000);
}

/*
int addJob(ifstream& jobstr)
{
    string nam;
    double t;
    long p;
    double r;
    long ind;

//cout<<"ijijij\n";
    jobstr >> nam;
    if(nam!="end")
    {
        jobstr >> t >> p >> r;
        t=rand();
        cout<<t<<"\n";
        Task cJob=Task(nam,t,p,r);
        cJob.setStatus("exists");
        if(not indexes.empty())
        {
            ind=indexes.top();
            indexes.pop();
            jobs[ind]=cJob;
            jobs[ind].setIndex(ind);
        }
        else
        {
            jobs.push_back(cJob);
            ind=jobs.size()-1;
            jobs[ind].setIndex(ind);
        }
        jobs[ind].setFacTime(0);
        Event cEv=Event(r,ind,-1,"Farrival");
        eventQueue.push(cEv);
        return 1;
    }
    return 0;
}*/

int addVar(ifstream& varStr, long start)
{
    long m;
    long t;
    if (varStr >> t)
    {
        varStr >> m;
        Event cEv=Event(t,-1,m,"Change");
        eventQueue.push(cEv);
        return 1;
    }
    return 0;
}

void getAllJobs(ifstream& jobstr, double start, double end)
{
    string nam;
    double t;
    long p;
    double r;
    double temptime;
    long ind;
    string type;
    double totArea=0;
    double curArea=0;

    while(jobstr >> nam){
        jobstr >> r >> t >> p >> type;
        if(r>=start){
            Task cJob=Task(nam,t,p,r,0);
            cJob.setStatus("exists");
            temptime=t;
            jobs.push_back(cJob);
            ind=jobs.size()-1;
            jobs[ind].setIndex(ind);
            jobs[ind].setFacTime(0);
            if(r+t>end){
                temptime=end-r;
            }
            if (t>end-start){
                t=end-start;
            }
            jobs[ind].setPerc(findQuantile(t));
            Event cEv=Event(r,ind,r,"Farrival");
            eventQueue.push(cEv);
            if(r+t>end){
                temptime-=r+t-end;
            }
        }
        else if(r+t>=start){
            
            Task cJob=Task(nam,t,p,r,start-r);
            cJob.setStatus("exists");
            temptime=t;
            jobs.push_back(cJob);
            ind=jobs.size()-1;
            jobs[ind].setIndex(ind);
            jobs[ind].setFacTime(start-r);
            Event cEv=Event(start,ind,r,"Farrival");
            eventQueue.push(cEv);
            temptime+=r-start;
            //cout << jobs[ind].name << "\n";
            if(r+t>end){
                temptime-=r+t-end;
            }
            if (t>end-start){
                t=end-start;
            }
            jobs[ind].setPerc(findQuantile(t));
        }
    }
    //cout<<"TA "<<totArea<<"\n";
}

void initializeMachines(long nbMachines, long nbNodes)
{
    long i;
    vector<pair<long,double>> a;
    a.push_back(make_pair(0,0));

    for(i=0; i<nbMachines; i++)
    {
        machines.push_back(Machine(nbNodes,i));
        machines[i].setAlloc(a);
        machines[i].setUtil(0);
        machines[i].setWait(0);
    }

}

double allocToMach(long ind, long cTime, double t, long np, long indj, double stretchM)
{
    long pU;
    double tU;
    long pU2;
    double tU2;
    bool doable=true;
    bool flag=false;
    double tTry=cTime;
    double tChan;
    double stretch;
    long inTry;
    long pTry;
    long pUold;
    inTry=0;
    long size;

    vector<pair<long,double>> alloc=machines[ind].getAlloc();
    long nod=machines[ind].nodes;
    long i=0;
    long j;

    if(alloc.size()==1)
    {
        alloc[0]=make_pair(np,cTime);
        alloc.push_back(make_pair(0,cTime+t));
        machines[ind].setAlloc(alloc);
        eventQueue.push(Event(cTime, indj, ind, "Astart"));
        eventQueue.push(Event(cTime+t, indj, ind, "Cend"));
        stretch=(cTime+t-jobs[indj].release)/jobs[indj].time;
        jobs[indj].setStatus("assigned");
        jobs[indj].setMachine(ind);
        jobs[indj].setStretch(stretch);
        jobs[indj].setStart(cTime);
        jobs[indj].setRStart(cTime);
        jobs[indj].setEnd(cTime+t);
        
        return 0;
    }
    else
    {
        pU=get<0>(alloc[i]);
        tU=get<1>(alloc[i]);
        i+=1;
        pTry=pU+np;
        tChan=tU;
        doable=(pTry<=nod);
        inTry=1;
        size=alloc.size();
        pUold=pU;
        while(i<size)
        {
            
            pU=get<0>(alloc[i]);
            tU=get<1>(alloc[i]);
            if (doable and tU>=tTry+t)
            {
                
                for(j=inTry; j<i; j++)
                {
                    pU2=get<0>(alloc[j]);
                    tU2=get<1>(alloc[j]);
                    pU2+=np;
                    alloc[j]=make_pair(pU2,tU2);
                }
                //if(tChan>tU){
                stretch=(tTry+t-jobs[indj].release)/jobs[indj].time;
                if (stretch<=stretchM)
                {
                    jobs[indj].setStatus("assigned");
                    jobs[indj].setMachine(ind);
                    jobs[indj].setStretch(stretch);
                    jobs[indj].setStart(tTry);
                    jobs[indj].setRStart(tTry);
                    jobs[indj].setEnd(tTry+t);
                    eventQueue.push(Event(tTry, indj, ind, "Astart"));
                    eventQueue.push(Event(tTry+t, indj, ind, "Cend"));
                    
                    
                }
                else
                {
                    
                    return stretch;
                }
                auto it = alloc.begin();
                if (tChan<tTry and cTime==tTry)
                {
                    //cout<<cTime << " AIAIA " << tTry << "\n";
                    it = alloc.insert(it+inTry, make_pair(pTry,tTry));
                }
                else
                {
                    alloc[inTry-1]=make_pair(pTry,tTry);
                }
                if (tU>tTry+t)
                {
                    it = alloc.insert(it+j, make_pair(pUold,tTry+t));
                }
                flag=true;
                break;
                //}
            }
            if (doable)
            {
                doable=(pU+np<=nod);
            }
            else if (i!= size-1)
            {
                doable=(pU+np<=nod);
                if (doable)
                {
                    inTry=i+1;
                    pTry=pU+np;
                    tTry=tU;
                }
            }
            i+=1;
            pUold=pU;
        }
        if(not flag)
        {
            if (doable)
            {
                for(j=inTry; j<i; j++)
                {
                    pU2=get<0>(alloc[j]);
                    tU2=get<1>(alloc[j]);
                    pU2+=np;
                    alloc[j]=make_pair(pU2,tU2);
                }
                //if(tChan>tU){
                stretch=(tTry+t-jobs[indj].release)/jobs[indj].time;
                if (stretch<=stretchM)
                {
                    jobs[indj].setStatus("assigned");
                    jobs[indj].setMachine(ind);
                    jobs[indj].setStretch(stretch);
                    jobs[indj].setStart(tTry);
                    jobs[indj].setRStart(tTry);
                    jobs[indj].setEnd(tTry+t);
                    eventQueue.push(Event(tTry, indj, ind, "Astart"));
                    eventQueue.push(Event(tTry+t, indj, ind, "Cend"));
                    
                    
                }
                else
                {
                    return stretch;
                }
                auto it = alloc.begin();
                if (tChan<tTry and cTime==tTry)
                {
                    it = alloc.insert(it+inTry, make_pair(pTry,tTry));
                }
                else
                {
                    alloc[inTry-1]=make_pair(pTry,tTry);
                }
                
                alloc.push_back(make_pair(0,tTry+t));
            }
            else
            {
                size=alloc.size();
                tU=get<1>(alloc[size-1]);
                alloc[size-1]=make_pair(np,tU);
                alloc.push_back(make_pair(0,t+tU));
                stretch=(tU+t-jobs[indj].release)/jobs[indj].time;
                if (stretch<=stretchM)
                {
                    jobs[indj].setStatus("assigned");
                    jobs[indj].setMachine(ind);
                    jobs[indj].setStretch(stretch);
                    jobs[indj].setStart(tU);
                    jobs[indj].setRStart(tU);
                    jobs[indj].setEnd(tU+t);
                    eventQueue.push(Event(tU, indj, ind, "Astart"));
                    eventQueue.push(Event(tU+t, indj, ind, "Cend"));
                    
                    
                }
                else
                {
                    
                    return stretch;
                }
            }
        }
        for (int i=0;i<alloc.size()-1;i++){
            if (get<0>(alloc[i])==get<0>(alloc[i+1])){
                /*if(indj==18240){
                    for (int j=0;j<10;j++){
                        cout<<"ATAYAYAYAYAYAYA\n\n";
                    }
                    cout<<i<<'\n';
                    cout<<get<1>(alloc[0])<<"AA\n";  
                } */         
                alloc.erase(alloc.begin()+i+1);
            }
        }
        machines[ind].setAlloc(alloc);
        return 0;
    }
}

double computeUtil(long mUse)
{    
   // cout<<"Ideiqed\n";
    double util=0;
    for (int i=0;i<mUse;i++){
        /*if(i==68){
            cout<<machines[i].getAlloc().size()<<'\n';
        }*/
        if(machines[i].getWait()>0){
            util+=1;
        }
        else{
            //cout<<i<<' ';
            if (machines[i].getAlloc().size()==0){
                vector<pair<long,double>> alloc=machines[i].getAlloc();
                alloc.push_back(make_pair(0,0));
                machines[i].setAlloc(alloc);
            }
            util+=(float) (get<0>(machines[i].getAlloc()[0]))/(float) (machines[i].nodes);
        }
    }
    return util/(float) (mUse);
}

void computeMSpace(long mAlive){
    MSpace=0;
    for (int i=0;i<mAlive;i++){
        if(machines[i].nodes-machines[i].getUtil()>MSpace){
            MSpace=machines[i].nodes-machines[i].getUtil();
        }
    }
}

bool FFit(vector<int> shuf, long indj, double cTime, double t, long mUse)
{
    bool found=false;
    double success;
    long indm;
    long np=jobs[indj].np;
    long i=0;
    bool comp=false;
    
    double stretch=(cTime+t-jobs[indj].release)/jobs[indj].time;
    
    while (not found and i<shuf.size()){
        indm=shuf[i];
        if (indm<mUse and machines[indm].getUtil()+np<=machines[indm].nodes){
            if(machines[indm].nodes-machines[indm].getUtil()==MSpace){
                comp=true;
            }
            machines[indm].setUtil(machines[indm].getUtil()+np);
            jobs[indj].setStatus("assigned");
            jobs[indj].setMachine(indm);
            jobs[indj].setStretch(stretch);
            jobs[indj].setStart(cTime);
            jobs[indj].setRStart(cTime);
            jobs[indj].setEnd(cTime+t);
            eventQueue.push(Event(cTime, indj, indm, "Astart"));
            eventQueue.push(Event(cTime+t, indj, indm, "Cend"));
            if(comp){
                computeMSpace(mUse);
            }
            found=true;
        }
        i+=1;
    }
    return found;
}

void findAndAlloc(long indm,double cTime,double t,long indj,double maxStret,long maxDist,long mUse,string details)
{
    double i;
    double j;
    long np=jobs[indj].np;

    double mini;
    double utilTot;
    double firstT;
    long imini;
    long machal;
    string dir;
    long maxDist2;
    
    bool cont=true;
    if(indm<0){
        indm=0;
        cont=false;
    }
    
    if(details[0]=='R'){
        dir="right";
        maxDist2=maxDist;
    }
    else if (details[0]=='L'){
        dir="left";
        maxDist2=maxDist;
    }
    else{
        dir="both";
        maxDist2=maxDist;
    }
    
   
    if(details[2]=='1'){
        firstT=1;
    }
    else{
        firstT=maxStret;
    }


    vector<double> successes(machines.size(),-1);
    double success;

    success=allocToMach(indm, cTime, t, np, indj,firstT);
    machal=indm;
    if (success>0)  //DO NOT FIT IN THE MACHINE
    {
        successes[indm]=success;
        for (i=1; i<maxDist2+1; i++)
        {
            if(indm+i<mUse and (dir=="right" or dir=="both"))
            {
                success=allocToMach(indm+i, cTime, t, np, indj,firstT);
                if(success==0)
                {
                    machal=indm+i;
                    break;
                }
                else
                {
                    successes[indm+i]=success;
                }
            }
            if(indm-i>=0 and (dir=="left" or dir=="both"))
            {
                success=allocToMach(indm-i, cTime, t, np, indj,firstT);
                if(success==0)
                {
                    machal=indm-i;
                    break;
                }
                else
                {
                    successes[indm-i]=success;
                }
            }
        }
    }
    
    if(success>0 and cont)  // DO NOT FIT IN ANY ACCEPTABLE MACHINE
    {
        utilTot=computeUtil(mUse);
        //cout << cTime << " " << mUse << " " << utilTot << "\n";
        mini=successes[indm];
        imini=indm;
        for(i=0; i<successes.size(); i++)
        {
            if(successes[i]>0 and successes[i]<mini)
            {
                mini=successes[i];
                imini=i;
            }
        }
        maxStret=mini;
        //cout<<' ' << maxStret<<"\n";
        success=allocToMach(imini, cTime, t, np, indj,maxStret);
        machal=imini;
    }
    machines[machal].setWait(machines[machal].getWait()+1);
}

int getTargetMachine(long indj, long mUse, string details)
{
    long choices;
    double temp;
    if(details[1]=='P'){
        choices=floor(mUse/5);
        if (choices==0){
            choices=1;
        }
        //cout << " Perc " << jobs[indj].getPerc() << "\n";
        temp=floor(jobs[indj].getPerc()*choices);
        if (temp==choices){
            temp-=1;
        }
        //cout<<jobs[indj].getPerc() << ' ' << temp*10<<' '<<mUse<<"\n";
        return (temp*5);
    }
    if (floor(jobs[indj].getPerc()*mUse==mUse)){
        return mUse-1;
    }
    return floor(jobs[indj].getPerc()*mUse);
}

void resetMachines(long nbNodes)
{
    long i;
    vector<pair<long,double>> a;
    a.push_back(make_pair(0,0));

    for(i=0; i<machines.size(); i++)
    {
        machines[i]=Machine(nbNodes,i);
        machines[i].setAlloc(a);
        machines[i].setWait(0);
        machines[i].setUtil(0);
    }
}

void resetJob(long indj)
{
    jobs[indj].setStatus("interupted");
    jobs[indj].setStart(-1);
    jobs[indj].setRStart(-1);
    jobs[indj].setEnd(-1);
    jobs[indj].setMachine(-1);
    jobs[indj].setFacTime(0);
}

double tryQueue(double cTime, double maxStret,long maxDist,long mUse, string heuristic, bool debuga, double mAlive, vector<int> shuf, string details)
{    
    //cout<<" "<<cTime << " A ";
    long indj;
    long indm;
    double t;
    bool isMax;
    double temp;
    bool found=false;
    
    while (!jobQueue.empty() and (heuristic=="algo" or MSpace>0))
    {
        
        found=false;
        Task job=jobQueue.top();
        indj=job.getIndex();
        
        t=jobs[indj].time;
        if(heuristic=="algo"){
            indm=getTargetMachine(indj,mUse,details);
            findAndAlloc(indm,cTime,t,indj,maxStret,maxDist,mUse, details);
        }
        else if (MSpace>=jobs[indj].np){
                found=FFit(shuf, indj, cTime, t, mAlive);
        }
        
        if (jobs[indj].getStretch()>maxStret)   // We rescheduled on an empty machine... We can't do better!
        {
            maxStret=jobs[indj].getStretch();
        }
        jobQueue.pop();
        
        if(heuristic=="FF" and found==false){
            tmpjobQueue.push(jobs[indj]);
        }
    }
    while (!tmpjobQueue.empty())
    {
        Task job=tmpjobQueue.top();
        jobQueue.push(job);
        tmpjobQueue.pop();
    }
    return maxStret;
}

double realloc(long mAlive, long mUse, long nbNodes, double cTime, double maxDist, double maxStret,double maxrStret, bool debuga, string heuristic, vector<int> shuf, string details, double startcount)
{
    long i;
    long indj;
    long indm;
    double t;
    bool isMax;
    double temp;
    resetMachines(nbNodes);
    for (i=0; i<jobs.size(); i++)
    {
        if (jobs[i].getMachine()>=mAlive and (jobs[i].getStatus()=="started" or jobs[i].getStatus()=="assigned"))
        {
            if(debuga){
                cout<<"Aborted Job " << jobs[i].name << " Target "<<jobs[i].getMachine()<<"\n";
            }
            if (jobs[i].getStatus()=="started"){
                if (debuga){
                    cout << "Waste: " << waste << "\n";
                }
                countW+=1;
                if(cTime-jobs[i].getRStart()<0){
                    cout<< "FATAL ERROR, negative work done\n";
                }
                if (jobs[i].getRStart()>startcount and jobs[i].getStatus()=="started"){
                    waste+=(cTime-jobs[i].getRStart())*jobs[i].np;
                }
                else if (cTime>startcount and jobs[i].getStatus()=="started"){
                    waste+=(cTime-startcount)*jobs[i].np;
                }
                if(debuga){
                    cout << "Waste: " << waste << " " << startcount << "\n";
                }
            }
            resetJob(i);
            jobQueue.push(jobs[i]);
        }
        else if(jobs[i].getStatus()=="assigned")
        {
            resetJob(i);
            jobQueue.push(jobs[i]);
        }
        else if(jobs[i].getStatus()=="started" and heuristic=="algo")
        {
            //cout<<"Alive\n";
            temp=jobs[i].getRStart();
            allocToMach(jobs[i].getMachine(), cTime, jobs[i].getEnd()-cTime, jobs[i].np, i, maxStret);
            jobs[i].setRStart(temp);
            machines[jobs[i].getMachine()].setWait(machines[jobs[i].getMachine()].getWait()+1);
            maxStret=max(maxStret,jobs[i].getStretch());
            //cout<<"Dead\n";
        }
        else if(jobs[i].getStatus()=="started" and heuristic=="FF"){
            indm=jobs[i].getMachine();
            if (indm<mAlive and machines[indm].getUtil()+jobs[i].np<=machines[indm].nodes){
                machines[indm].setUtil(machines[indm].getUtil()+jobs[i].np);
            }
            else{
                cout<<"Fatal Error, dig realloc\n";
            }
        }
    }
    
    return tryQueue(cTime,maxStret,maxDist,mUse,heuristic,debuga,mAlive,shuf, details);
}


long updateMuse(long mUse,long mAlive, long alwUse,double infMuse,double supMuse,bool debuga,string heuristic)
{    
    double utilTot;
    bool changed=false;
    //cout<<mUse<<" QQ " << mAlive<<"\n";
    while(true){
        utilTot=computeUtil(mUse);
        //cout <<"ut "<< utilTot<< " "<<mUse << " ";
        if (utilTot<infMuse and mUse>alwUse){
            changed=true;
            mUse-=1;
            if(mUse==alwUse){
                break;
            }
        }
        else if(utilTot>supMuse and mUse<mAlive){
            changed=true;
            mUse+=1;
            if(mUse==mAlive){
                break;
            }
        }
        else{
            break;
        }
    }
    
    //cout<<"deasd\n";
    if(changed and debuga and heuristic=="algo"){
        cout<<"\nNew mUse"<<' '<<mUse<<"\n";
    }
    //
    return mUse;
}

double simulate(long alwUse, string varfile, string jobfile, long maxDist, long nbNodes, long nbMachines, 
                double start,double end,double infMuse,double supMuse,bool debuga,string heuristic, string details, string outfile, long wins)
{
    double maxrStret=1;
    long maxindm=0;
    double cTime = start;
    double cOldTime=start;
    long mAlive;
    double lastchange=start;
    double areaAvail=0;
    double temptime;
    
    srand(time(NULL));
    double maxStret=1;
    double Stret=0;
    double utilDone=0;
    double utilTot=0;
    double startcount;
    double i;
    double j;
    long jn=0;
    long vn=0;
    double t;
    double tfirst;
    long np;
    long indj;
    long indm;
    startcount=end-(end-start)/wins;

    double stretstret=0;
    double mini;
    double maxFFStret=0;
    long imini;
    bool fake=false;
    bool found;
    double avgStret=0;
    long njdone=0;
    long njdone2=0;
    long njstart=0;
    vector<int> shuf;
    bool err=false;
    double dataStart;
    
    for(i=0;i<nbMachines;i++){
        shuf.push_back(i);
    }
    if(maxDist>0){
        random_shuffle(shuf.begin(), shuf.end());
    }
    
    
    /*for(i=0;i<nbMachines;i++){
        cout<<shuf[i]<< ' ';
    }
    cout<<"\n";
*/
    bool flTest=false;
    string typ;
    vector<pair<long,double>> alloc;

    ifstream jobStr(jobfile,ios::in);
    getAllJobs(jobStr,start,end);
    
    Event cEv=Event(end,-1,-1,"xCut");
    eventQueue.push(cEv);
//Get first job eventmUse=1
    //jn+=addJob(jobStr);

    ifstream varStr(varfile,ios::in);
    varStr >> mAlive;
    
    computeMSpace(mAlive);
    long mUse=(mAlive+alwUse)/2;
    vn+=addVar(varStr,start);
//Get the first variation event


    //MAIN LOOP
    ofstream myfile;
    myfile.open(outfile, ios_base::app);

    while (!eventQueue.empty())
    {
        fake=false;
        Event cEv=eventQueue.top();
        cTime=cEv.time;
        indj=cEv.relatedTask;
        indm=cEv.machine;
        typ=cEv.type;
        eventQueue.pop();
        if (typ=="Farrival")  //NEW JOB
        {
            njstart+=1;
            //cout << cTime <<' ' << mUse<< "\n";
            if(cTime>start and not flTest){
                flTest=true;
            }
            found=false;
            if(debuga){
                cout << "\n" << typ << " Time "<<cTime << " Job " << jobs[indj].name << " FAC " << jobs[indj].getFacTime() << " Proc " << jobs[indj].np << " Release " << indm << " length " << jobs[indj].time << '\n';
            }
            temptime=indm;
            t=jobs[indj].time-jobs[indj].getFacTime();
            indm=getTargetMachine(indj,mUse,details);
            if(debuga and heuristic=="algo"){
                cout<<"Target "<<indm<<"\n";
            }
            if(heuristic=="algo"){
                if(temptime<start){
                    findAndAlloc(-1,cTime,t,indj,maxStret,mAlive,mUse,details);
                }
                else{
                    findAndAlloc(indm,cTime,t,indj,maxStret,maxDist,mUse, details);
                }
            }
            else if(heuristic=="FF"){
                if(temptime<start){
                    if(MSpace>=jobs[indj].np){
                        found=FFit(shuf, indj, cTime, t, mAlive);
                    }
                }
                else{
                    if(MSpace>jobs[indj].np){
                        found=FFit(shuf, indj, cTime, t, mAlive);
                    }
                    if(not found){
                        jobQueue.push(jobs[indj]);
                    }
                }
            }
            else{
                myfile << jobfile << " " << varfile << " " <<"FATAL ERROR : HEURISTIC NOT RECOGNIZED\n";
                err=true;
                break;
            }
            if(jobs[indj].getStretch()>maxStret){
                maxStret=jobs[indj].getStretch();
            }
            
            if(debuga and (heuristic=="algo" or found==true)){
                cout << "Job" << jobs[indj].name << " Decision " << jobs[indj].getMachine()<< " Start "<<jobs[indj].getRStart()<< 
                        " End "<<jobs[indj].getEnd()<<" Stretch "<< jobs[indj].getStretch() <<'\n';
            }
        }
        else if (typ=="Change") // CHANGE IN NUMBER OF MACHINES
        {
            //cout<<cTime<<"\n";
            if(indm!=mAlive){
                if(lastchange>startcount){
                    areaAvail+=(cTime-lastchange)*mAlive;
                }
                else if (cTime>startcount){
                    areaAvail+=(cTime-startcount)*mAlive;
                }
                lastchange=cTime;
                if(debuga){
                    cout << "\n" << typ << " Time "<< cTime << " New#Machines " << indm <<  '\n';
                }
                
                vn+=addVar(varStr,start);
                if(mAlive<indm){
                    mAlive=indm;
                    mUse=updateMuse(mUse,mAlive, alwUse,infMuse,supMuse,debuga,heuristic);
                }
                else if(mUse>indm){
                    mUse=indm;
                }
                mAlive=indm;
                computeMSpace(mAlive);
                maxStret=realloc(mAlive,mUse,nbNodes,cTime,maxDist,maxStret,maxrStret,debuga,heuristic,shuf,details, startcount);
                mUse=updateMuse(mUse,mAlive, alwUse,infMuse,supMuse,debuga,heuristic);
            }
            else{
                vn+=addVar(varStr,start);
            }
        }
        else if (typ=="Astart")  // START OF JOBS
        {
            if (!(jobs[indj].getStart()!=cTime or jobs[indj].getStatus()=="started"))
            {
                if(jobs[indj].getRStart()==cTime and debuga){
                    cout <<  typ << " Time "<< cTime << " Job " << jobs[indj].name << " Proc " << jobs[indj].np << " Machine " << indm << " " << jobs[indj].getEnd()<<"\n";
                }
                if(heuristic=="algo"){
                    alloc=machines[indm].getAlloc();
                    if (alloc.size()==0){
                        alloc.push_back(make_pair(0,0));
                    }
                    tfirst=get<1>(alloc[1]);
                    if(tfirst<=cTime)
                    {
                        alloc.erase(alloc.begin());
                    }
                    
                    if (alloc.size()==0){
                        alloc.push_back(make_pair(0,0));
                    }
                    machines[indm].setAlloc(alloc);
                    machines[indm].setWait(machines[indm].getWait()-1);
                    mUse=updateMuse(mUse,mAlive, alwUse,infMuse,supMuse,debuga,heuristic);
                }
                if(heuristic=="FF" and indm>maxindm){
                    maxindm=indm;
                }
                jobs[indj].setStatus("started");
            }
            else{
                fake=true;
            }
        }
        else if (typ=="Cend")  // END OF JOBS
        {
            
            if(!(jobs[indj].getEnd()!=cTime or jobs[indj].getStatus()=="completed"))
            {
                
                if(debuga){
                    cout << "\n" << typ << " Time " << cTime << " Job " << jobs[indj].name << " Proc " << jobs[indj].np << " Machine " << indm << '\n';
                }
                if(heuristic=="algo"){
                    alloc=machines[indm].getAlloc();
                    if (alloc.size()==0){
                        alloc.push_back(make_pair(0,0));
                    }
                    tfirst=get<1>(alloc[1]);
                    if(tfirst<=cTime)
                    {
                        alloc.erase(alloc.begin());
                    }
                    
                    if (alloc.size()==0){
                        alloc.push_back(make_pair(0,0));
                    }
                    machines[indm].setAlloc(alloc);
                }
                if(heuristic=="FF"){
                    machines[indm].setUtil(machines[indm].getUtil()-jobs[indj].np);
                    if(machines[indm].nodes-machines[indm].getUtil()>MSpace){
                        MSpace=machines[indm].nodes-machines[indm].getUtil();
                    }
                    if (machines[indm].getUtil()<0){
                        cout<<"FATAL ERROR\n less than 0 processors used " << indm << "\n";
                        err=true;
                        break;
                    }
                }
                jobs[indj].setStatus("completed");
                indexes.push(indj);
                stretstret=(cTime-jobs[indj].release)/jobs[indj].time;
                if(cTime>startcount){
                    avgStret+=stretstret;
                    if (stretstret>maxFFStret){
                        maxFFStret=stretstret;
                    }
                    njdone2+=1;
                }
                else{
                    njdone+=1;
                }
                maxrStret=max(maxrStret,jobs[indj].getStretch());
                if(debuga){
                    cout<<"Real stretch "<< jobs[indj].getStretch() <<"\n";//<< " maxStretch " << maxrStret<<'\n';
                }
                //cout << "OY"<<machines[indm].getWait()<<'\n';
                //cout<<"alive\n";
                mUse=updateMuse(mUse,mAlive, alwUse,infMuse,supMuse,debuga,heuristic);
                //cout<<"dead\n";
                if (jobs[indj].getRStart()>startcount){
                    if(!(cTime-jobs[indj].getRStart()>jobs[indj].time)){
                        utilDone+=(jobs[indj].time-jobs[indj].inifacTime)*jobs[indj].np;
                    }
                }
                else if(cTime>startcount){
                    utilDone+=(cTime-startcount)*jobs[indj].np;
                }
                
                if(heuristic=="FF"){
                    maxStret=tryQueue(cTime, maxStret, maxDist, mUse, heuristic, debuga, mAlive, shuf,details);
                }
                
            }
            else{
                fake=true;
            }
        }
        else if(typ=="xCut"){
            if(debuga){
                cout<<"\nCUT At Time "<<cTime<<"\n";
            }
            areaAvail+=(cTime-lastchange)*mAlive;
            utilTot=utilDone;
            for (i=0;i<jobs.size();i++){
                if(jobs[i].getStatus()=="started"){
                    if(jobs[i].getRStart()>startcount){
                        utilTot+=(cTime-jobs[i].getRStart())*jobs[i].np;
                    }
                    else{
                        utilTot+=(cTime-startcount)*jobs[i].np;
                    }
                    if(cTime-jobs[i].getRStart()>jobs[i].time){
                        myfile << jobfile << " " << varfile << " " <<"FATAL ERROR : You worked too much2\n";
                        err=true;
                        break;
                    }
                    
                }
            }
            break;
        }
        else{
            fake=true;
        }
        if(fake){
            cTime=cOldTime;
        }
        else{
            cOldTime=cTime;
        }
    }
    avgStret/=njdone2;
    //cout << njdone << " " << njstart<<"\n";
    if(not err){
        myfile << jobfile << " " << varfile << " " << heuristic << " "  << areaAvail*machines[0].nodes << " " << utilDone << " " << utilTot << " " << waste << " " << maxFFStret << " " << avgStret << " " << (double) (njdone2)/(double) (njstart-njdone) << " " << waste/countW  <<"\n";
    }
    myfile.close();
    //cout<<"Area Avail "<<areaAvail*machines[0].nodes<<" Area of completed jobs " <<utilDone<< " +Jobs in Progress " << utilTot << '\n';
    //cout<<"Max stretch "<<maxrStret << ' ' << maxStret<<'\n';
    return cTime;
}


int main(int argc, char** argv)
{
    bool debuga=false; // Print stuff for debug
    ifstream input(argv[1],ios::in);
    string jobfile;
    string quantfile;
    long nbMachines;
    long alwUse;
    long nbNodes;
    long nb_iter;
    string varfile;
    double start;
    double end;
    string outfile;
    string heuristic;
    string details="empty";
    long maxDist=0;
    double mDf=0;
    double infMuse=0;
    double supMuse=0;
    long wins;
    long i=0;
    bool contemp=true;
    double AVG=0;
    while(input>>jobfile)
    {
        contemp=false;
        input >> nbMachines;
        input >> alwUse;
        input >> nbNodes;
        input >> varfile;
        initializeMachines(nbMachines,nbNodes);
        
        input >> start;
        input >> end;
        end=start+end;
        input >> heuristic;        
        //cout<<heuristic<<"\n";
        cout<<jobfile<<"\n";
        if(heuristic=="algo"){
            input >> wins;
            input >> quantfile;
            addQuantiles(quantfile);
            input >> details;
            input >> mDf;
            maxDist=ceil(mDf/100*nbMachines);
            //maxDist=nbMachines;
            input >> infMuse;
            infMuse = infMuse/100;
            input >> supMuse;
            supMuse=supMuse/100;
        }
        else if(heuristic=="FF"){
            input >> wins;
            input >> maxDist;
        }
        else{
            input >> wins;
            input >> quantfile;
        }
        input >> outfile;
        double r;
        
        r=simulate(alwUse,varfile,jobfile,maxDist,nbNodes,nbMachines,start,end,infMuse,supMuse,debuga,heuristic,details,outfile, wins);
        
        
        
        //ofstream myfile;
        //myfile.open(outfile, ios_base::app);
        //myfile << jobfile << " " << varfile << " " << heuristic << " "  << nbMachines << " " << alwUse << " " << nbNodes << " " << wins << " " << nbMachines+1 << " " << alwUse+1 << " " << nbNodes+1 <<"\n";
        //myfile.close();
        //cout<< r << '\n';
        AVG+=r;
            
        AVG/=nb_iter;
        jobs={};
        machines={};
        
        quantiles={};
        
        //CLEAN
        while (!jobQueue.empty())
        {
            jobQueue.pop();
        }
        while (!tmpjobQueue.empty())
        {
            tmpjobQueue.pop();
        }
        while (!eventQueue.empty())
        {
            eventQueue.pop();
        }
        while (!indexes.empty())
        {
            indexes.pop();
        }
        waste=0;
        countW=0;
        //cout<<"Average: " << AVG << "\n";
    }
    return 0;
}