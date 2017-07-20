# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 13:02:46 2017

@author: Neha
"""
import copy
from operator import itemgetter
tails=['T1','T2','T3','T4','T5','T6']
flightDurations=[['AUS','DAL',50],['HOU','DAL',65],['AUS','HOU',45]]
groundTimes=[['AUS',25],['DAL',30],['HOU',35]]
gates=[['HOU',3],['DAL',2],['AUS',1]]
temp=[]
austinToDallasList=[]
initialSchedule=list()
cnt=0

def miltaryToMinutesAfterMidnight(militaryTime):
    militaryTimeInt=int(militaryTime)
    minAfterMidnightTime=(militaryTimeInt//100)*60+(militaryTimeInt%100)
    return minAfterMidnightTime

def minutesAfterMidnightToMilitary(minutesAfterMidnightTime,waitingDuration):
    minutesAfterMidnightTime=minutesAfterMidnightTime+waitingDuration
    hour,minutes=divmod(minutesAfterMidnightTime,60)
    if len(str(hour))==1:
        hour='{0:02d}'.format(hour)
    if len(str(minutes))==1:
        minutes=str(minutes).rjust(2,'0')
    newMilitaryTime=str(hour)+str(minutes)
    return newMilitaryTime    

def calculateDuration(flightToSearch):
    for duration in flightDurations:
        if flightToSearch[1] in duration and flightToSearch[2] in duration:
            return duration[2]

def groundTimeCalculation(destinationOfFlight):
        for grndTime in groundTimes:
            if destinationOfFlight in grndTime:
                return grndTime[1]  
   
def assignFlight(currentFlight,nextFlight):
    currentFlight[1]=nextFlight[1]
    currentFlight[2]=nextFlight[2]
    currentFlight[3]=nextFlight[5]
    currentFlight[4]=minutesAfterMidnightToMilitary(miltaryToMinutesAfterMidnight(currentFlight[3]),calculateDuration(currentFlight)) 
    currentFlight[5]=minutesAfterMidnightToMilitary(miltaryToMinutesAfterMidnight(currentFlight[4]),groundTimeCalculation(currentFlight[2]))
    return currentFlight

def assignFlightToAusDal(currentFlight,nextFlight):
    currentFlight[1]=currentFlight[2]
    currentFlight[2]=nextFlight[2]
    currentFlight[3]=currentFlight[5]
    currentFlight[4]=minutesAfterMidnightToMilitary(miltaryToMinutesAfterMidnight(currentFlight[3]),calculateDuration(currentFlight)) 
    currentFlight[5]=minutesAfterMidnightToMilitary(miltaryToMinutesAfterMidnight(currentFlight[4]),groundTimeCalculation(currentFlight[2]))
    return currentFlight

def ausDalFlight(ausFlight,dalFlight):
    flightAToD=[]
    copyFlight=[]
    while miltaryToMinutesAfterMidnight(minutesAfterMidnightToMilitary(miltaryToMinutesAfterMidnight(dalFlight[5]),calculateDuration(dalFlight)))<int(miltaryToMinutesAfterMidnight('2200')) and miltaryToMinutesAfterMidnight(minutesAfterMidnightToMilitary(miltaryToMinutesAfterMidnight(ausFlight[5]),calculateDuration(ausFlight)))<int(miltaryToMinutesAfterMidnight('2200')):
        copyFlight=copy.deepcopy(ausFlight)
        ausFlight=assignFlightToAusDal(ausFlight,dalFlight)
        dalFlight=assignFlightToAusDal(dalFlight,copyFlight)
        deepCopyAus=copy.deepcopy(ausFlight)
        deepCopyDal=copy.deepcopy(dalFlight)
        flightAToD.append(deepCopyDal)
        flightAToD.append(deepCopyAus)
    return flightAToD

def swappingFlight(flightsToSwap):
    flightsToSwapTemp=[]
    for x in range(0,len(flightsToSwap),2):
        if flightsToSwap[x][2]==flightsToSwap[x+1][1] and miltaryToMinutesAfterMidnight(minutesAfterMidnightToMilitary(miltaryToMinutesAfterMidnight(flightsToSwap[x][5]),calculateDuration(flightsToSwap[x])))<int(miltaryToMinutesAfterMidnight('1700')) and miltaryToMinutesAfterMidnight(minutesAfterMidnightToMilitary(miltaryToMinutesAfterMidnight(flightsToSwap[x+1][5]),calculateDuration(flightsToSwap[x+1])))<int(miltaryToMinutesAfterMidnight('1700')):
            temporary=[]
            temporary=copy.deepcopy(flightsToSwap[x])
            flightsToSwap[x]=assignFlight(flightsToSwap[x],flightsToSwap[x+1])
            flightsToSwap[x+1]=assignFlight(flightsToSwap[x+1],temporary)
            flightsToSwapTemp.append(flightsToSwap[x])
            flightsToSwapTemp.append(flightsToSwap[x+1])
    return flightsToSwapTemp  
         
for k in range(0,3):
    for j in range(k+1,3):
        while gates[k][1] !=0:
            if gates[j][1] != 0:
                temp.append(tails[cnt])
                temp.append(gates[k][0])
                temp.append(gates[j][0])
                temp.append('0600')
                destinationArrivalTime=minutesAfterMidnightToMilitary(miltaryToMinutesAfterMidnight('0600'),calculateDuration(temp))
                temp.append(destinationArrivalTime)       
                newDepartureTime=minutesAfterMidnightToMilitary(miltaryToMinutesAfterMidnight(destinationArrivalTime),groundTimeCalculation(gates[j][0]))
                temp.append(newDepartureTime) 
                temp1=copy.deepcopy(temp)
                initialSchedule.append(temp1)
                cnt+=1
                del temp[:]
                temp.append(tails[cnt])
                temp.append(gates[j][0])
                temp.append(gates[k][0])
                temp.append('0600')
                destinationArrivalTime=minutesAfterMidnightToMilitary(miltaryToMinutesAfterMidnight('0600'),calculateDuration(temp))
                temp.append(destinationArrivalTime)       
                newDepartureTime=minutesAfterMidnightToMilitary(miltaryToMinutesAfterMidnight(destinationArrivalTime),groundTimeCalculation(gates[k][0]))
                temp.append(newDepartureTime) 
                temp1=copy.deepcopy(temp)
                initialSchedule.append(temp1)
                cnt+=1
                del temp[:]     
                gates[k][1]-=1
                gates[j][1]-=1               
            else:
                break

finalSchedule=copy.deepcopy(initialSchedule)
while True:
    initialSchedule=swappingFlight(initialSchedule)
    finalSchedule+=copy.deepcopy(initialSchedule)
    if len(initialSchedule) == 0:
        break

for y in range(len(finalSchedule))[::-1]:
    if finalSchedule[y][2] == 'DAL':
        dallas=copy.deepcopy(finalSchedule[y])
        break
    
for z in range(len(finalSchedule))[::-1]:
    if finalSchedule[z][2] == 'AUS':
        austin=copy.deepcopy(finalSchedule[z])
        break
		
austinToDallasList=ausDalFlight(austin,dallas)
finalSchedule+=copy.deepcopy(austinToDallasList)

sortedList=sorted(finalSchedule,key=itemgetter(0,3))
listToPrint=[[w[0],w[1],w[2],w[3],w[4]] for w in sortedList]
    
csv_header = 'tail_number,origin,destination,departure_time,arrival_time'
file_name = 'flight_schedule.csv'
def print_flight_schedule(fn, csv_hdr, flt_sched):
    with open(fn,'wt') as f:
        print(csv_hdr, file=f)
        for s in flt_sched:
            print(','.join(s), file=f)
print_flight_schedule(file_name, csv_header, listToPrint)