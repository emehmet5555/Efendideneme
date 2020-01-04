"""
EFENDİ

ALNS

Electrical HHC with fast charge techs


"""
# classes imported here

import ClassEV
import ClassJob
import ClassStation
import Class
import Classheuristic
import copy

# necessary libraries imported here
import time
import math
import random

print("Program started :")
#change these with respect to the number of entities-------
N = 15 # this is number of entity and indicates the number of jobs and EVs (nurses)
S=3 # this is number of stations
#--------------------------------------------------------
# run time calculation starts here
def procedure():
   time.sleep(2.5)

# measure wall time
t0 = time.time()


#####File read here respectively
def assign3zeros(N, vector):  # Nx10 zero matrix 10: column
    Feature = 10
    for j in range(N):
        column = []
        for i in range(Feature):
            column.append(0)
        vector.append(column)
    return vector

Wdata = []
# the parameter set of ev initializing from the data file here
def parameterev(Wdata):
    assign3zeros(N, Wdata)
    file = open("F:/AA makale/datanurse.txt", "r")
    data = file.readlines()
  #  print("---------->data", data)
    l=0
    for k in data:
        liste = k.split(",")
        k=0
        for i in liste:
            Wdata[l][k]=i
            k=k+1
        l=l+1

    file.close()
    return Wdata

Wdata=parameterev(Wdata)

###########EVs##############
# the number of EVs created here!!!!!

EVs = [] # the ev objects holds within this
i = 0
while (i < N):
    EV = ClassEV.Ev((i), Wdata[i][0], Wdata[i][1], Wdata[i][2], Wdata[i][3], Wdata[i][4], Wdata[i][5],Wdata[i][6], Wdata[i][7], Wdata[i][8],-1)
    EVs.append(EV)
 #   EV.printinfo()
    i = i + 1


#####File read here respectively
def parameterjob(Wdata):
    Wdata = []
    assign3zeros(N, Wdata)

    file1 = open("F:/AA makale/data.txt", "r")
    data1 = file1.readlines()
    #print("---------->data", data)
    l=0
    for k in data1:
        liste = k.split(",")
        k=0
        for i in liste:
            Wdata[l][k]=i
            k=k+1
        l=l+1
    file1.close()
    return Wdata

###########Jobs##############
Wdata=parameterjob(Wdata)
# the number of jobs created here!!!!!
Jobs = [] # the job objects holds within this
i = 0
while (i < N):
    Job = ClassJob.Job((i), Wdata[i][0], Wdata[i][1], Wdata[i][2], Wdata[i][3], Wdata[i][4], Wdata[i][5],Wdata[i][6], Wdata[i][7], Wdata[i][8])
    Jobs.append(Job)
    i = i + 1


# this function calculates the scores for each job
Order = Job.Scorejob(Jobs)

# this function calculates the scores for each ev/nurse
Ordere=EV.Scoreev (EVs)

###########Charging Stations##############
Stations = [] # the station objects holds within this
i = 0
while (i < S):#number of charging stations
    Stat = ClassStation.Station([str(i+N)],360,1380)
    Stations.append(Stat)
    i = i + 1

###############################



Solutions = [] # the solution objects holds within this
Bestsolutions= []
Currentsolutions= []


i = 0
while (i < N):
    Soln = Class.Solution([str(i)],[str(EVs[i].etwa),str(0),str(EVs[i].etwa),str(EVs[i].etwb)],[str(100),str(100)],[str(1)],[str(0)],[str(-1)],0,str(EVs[i].cost),0.0924,0.66,0,0)
    Solutions.append(Soln)
  #  Soln.printinfo()
    i = i + 1
Bestsolutions = copy.deepcopy(Solutions)
Currentsolutions= copy.deepcopy(Solutions)
Cplexsol= copy.deepcopy(Solutions)

############distance matrix read from the distance.txt file ############
Dmatris=[]
Dmatris=Solutions[0].distancematrix(Dmatris)
#########################
Incompat=Solutions[0].calculateincompat(N,EVs,Jobs)

# initial assignment is achieved here
Solutions[0].initialassignment(N,Solutions,Incompat,Ordere,Order)


Job.OrderJTwa(Solutions,Jobs,N)


# this method calculate overall routing, scheduling, and charging decisions and their cost charges
# this function just considers the initial solution
Solutions[0].Calculateoverall(N,S, Solutions, Jobs, EVs,Dmatris,Incompat)
print("Initial solution is generated")

#-----------------------------------------

Remove = [] # the remove objects holds within this
Repair = [] # the repair objects holds within this

Improvement=Classheuristic.Heuristic(99999,99999,99999)
Improvement.neighbourhood(Remove,Repair)
#---------the iteratation number ---------------------------
#change this if it is necessary
Maximumiteration=50000
#--------------------------------------------------------
print("Improvement procedure is started")
# ALNS is started here
(Solutions,Bestsolutions,Currentsolutions)=Improvement.alns(N, S,Solutions,Bestsolutions,Currentsolutions,Jobs,EVs, Repair, Remove,Maximumiteration,Dmatris,Incompat) # ALNS procedure is achieved here!!

# the best solution is given here
print("\n---Bestsolutions")
for i in Bestsolutions:
    i.printinfo()
Totalobj =0
Totalobj=Improvement.totalobjectivefuntion(Bestsolutions)
print("\n---Bestsolutions",Totalobj,Improvement.totalobj(Bestsolutions))

"""
#cplexs optimum solution is summarized here
print("\n---Cplexsol")
for i in Cplexsol:

    if int(i.routing[0])==2:
        i.routing=['2','18','17','16','24','25','29','26']
        print("v",i.routing)
    elif int(i.routing[0])==5:
        i.routing=['5','15','21','23','19','22','20','28','27']
        print("v", i.routing)

Cplexsol[0].Calculateoverall(N,S, Cplexsol, Jobs, EVs,Dmatris,Incompat)
Improvement.totalobjectivefuntion(Cplexsol)
print("\n---Cplexsol")
for i in Cplexsol:
    i.printinfo()
"""
print ("Wall time", time.time() - t0  )
print("\nProgram finished !")
