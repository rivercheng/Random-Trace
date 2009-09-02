import string
import math
import datetime
import sys
import dircache
import random
import os
from scipy.stats import *
import numpy as np
import matplotlib.pyplot as plt
from scipy import *

def selectSessionLength():
    rand = 0
    mu = exp(18.23)
    while rand <= 0:
      rand = lognorm.rvs(0.75432,scale = mu)
    return rand 
    
    

def selectFirstInterval(lifeTime):
    rand = 0
    a = -0.25772
    b = 10281000
    c = 1054700
    print "current session length: ", lifeTime
    
    while rand<=0:
        rand = genextreme.rvs(a, b, c)
    if rand>=lifeTime:
        rand = lifeTime
 
    print 'current first Interval: ', rand
    return rand 
    
    
def selectFirstAction(dic):
    pass
    

    
def selectThinkTime():
    rand = 0
    a = -0.51
    b = 266370
    c= 199870
    while rand < 20000:
      rand = genextreme.rvs(a, b, c)
    
    print 'current think time: ', rand
    return rand 
    
    
    
def selectAction(dic, x, y ,z):
    actName = "ZOOM_IN"
    return actName 
    

def selectActionTimes(opsTimesRanges, actName, x, y ,z):
    range = [0, 0]
    times = 1
    
    timesRange = opsTimesRanges[actName]
    #print "current action : timerange", actName, timesRange
    
    rand = random.random()
    
    for k in timesRange.keys():
      
      range = timesRange[k]
      
      if ((rand > range[0])&(rand <= range[1])):
        times = int(k)
        
        if actName == 'MOVE_LEFT':
          if times>(highBoundX-x):
            times = highBoundX-x
          x += times
        elif actName == 'MOVE_RIGHT':
          if times>(x-lowBoundX):
            times = x-lowBoundX
          x -= times
        elif actName == 'MOVE_UP':
          if times>(highBoundY-y):
            times = highBoundY-y
          y += times
        elif actName == 'MOVE_DOWN':
          if times>(y-lowBoundY):
            times = y-lowBoundY
          y -= times
        elif actName == 'ZOOM_IN':
          if times>(highBoundZ-z):
            times = highBoundZ-z
          z += times
        elif actName == 'ZOOM_OUT':
          if times>(z-lowBoundZ):
            times = z-lowBoundZ
          z -= times
        elif actName == 'RESET':
          x = y = z = 0
          times = 1
        break
          
    return times, x, y, z
    
def selectActShortInterval():
    rand = 0
    a = 0.48351
    b = 372.66
    while ((rand <= 0)|(rand > 20000)):
      rand = weibull_min.rvs(a,loc=0,scale=b)
    
    #print 'current short action interval: ', rand
    return rand
    
def setProbabilityRange(file):
    rangeStart = 0.0
    dic = {}
    range = [0.0,0.0]
 
    for line in file: 
      ln = line.split()
      op = ln[0]
      prob = float(ln[2])
      
      range[0] = rangeStart
      range[1] = range[0]+prob
      if range[1]>1.0:
        #print "impossible probability: ", range[1]
        range[1] = 1.0
        
      dic[op] = [range[0], range[1]]
      rangeStart = range[1]
    
    return dic
    
# for each operation, calculate the distribution of times of occurence of consective operations including single operation   
def getOpsTimesRanges(dic):
  
  keyValues = dic.keys()
  keyValues.sort()
  
  for op in keyValues:
    f = open('huge_normal_consecOpsOccurence_'+op+'.txt', 'r')
    eventRangesDic = setProbabilityRange(f)  
    dic[op] = eventRangesDic
    f.close()
  return dic 


def generateTraces(count):
  prefix = 'randomTrace'
  eventFreFName = 'huge_normal_eventfrequency.txt'
  firstActFName = 'huge_normal_firstActFrequency.txt'
  
  opsTimesSelectRanges = {}
  dic = {}
  
  eventFreFile = open(eventFreFName, 'r')
  firstActFile = open(firstActFName, 'r')
  
  for line in eventFreFile:
    ops = line.split()
    op = ops[0]
    opsTimesSelectRanges[op]= {}

    
  #caculate the distribution of occurence of differenct operations
  opsTimesSelectRanges = getOpsTimesRanges(opsTimesSelectRanges)
  eventFreFile.close()
  
  firstActFrequencyRanges = setProbabilityRange(firstActFile)
  #print firstActFrequencyRanges
  
  eventFreFile = open(eventFreFName, 'r')
  #get distribution of operation event frequency to choose one action
  dic = setProbabilityRange(eventFreFile)
  
  
  eventFreFile.close()
  
  for k in range(count):
  
    fstr = str(k) 
    
    x = y = z =0
    currentTime = 0.0 
    lifeTime = 0.0
    firstTimeInterval = 0.0 
    actionTimes = 0
    actionNum = 0
    
    print "Start generating trace " + fstr
    
    #outpath = 'c:/new_traces/random_traces/'
    outpath = sys.argv[2]
    f = open(outpath+prefix+'_'+fstr+'.txt','w')
    
    
    # generate life time
    lifeTime = selectSessionLength()
    
    # get the interval to first operation from 'BEGIN'
    firstTimeInterval = selectFirstInterval(lifeTime)
    
    print >>f, 0, 0, 'BEGIN'
    
    currentTime = firstTimeInterval
    
   
    while currentTime < lifeTime:
    
      ##############################################
      if actionNum == 0 :
        action = selectFirstAction(firstActFrequencyRanges)
      else:
        action = selectAction(dic, x , y, z)
        
      actionNum += 1
      
      #action = selectAction(dic, x , y, z)
      #list is a list containing actionTimes, x, y, z
      
      res = selectActionTimes(opsTimesSelectRanges, action, x, y, z)
      
      actionTimes = int(res[0])
      print "current action: action times ", action, ":", actionTimes
      x = res[1]
      y = res[2]
      z = res[3]
    
      print >>f, int(currentTime/1000000), int(currentTime%1000000), action
      
      if actionTimes > 1:
        for k in range(actionTimes-1):
          shortInterval = selectActShortInterval()
          
          currentTime += shortInterval
          
          if currentTime >=lifeTime:
            break
            #print >>f, int(lifeTime/1000000), int(lifeTime%1000000), 'QUIT'
            
          else:
            print >>f, int(currentTime/1000000), int(currentTime%1000000), action
            
      thinkTime = selectThinkTime()
      currentTime += thinkTime
    
    print >>f, int(lifeTime/1000000), int(lifeTime%1000000), 'QUIT' 
    f.close()
    print "Complete generating trace " + fstr
    print ""
    
    
####main function
parameterNum = len(sys.argv)
if parameterNum < 3:
  print "error: usage:", sys.argv[0], "<trace count>","<output directory>"
  exit()
  
random.seed(0)
getBounds()

print lowBoundX, highBoundX
print lowBoundY, highBoundY
print lowBoundZ, highBoundZ

count = int(sys.argv[1])
generateTraces(count)
  

