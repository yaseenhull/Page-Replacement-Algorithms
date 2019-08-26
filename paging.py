# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 08:07:59 2019

@author:    hllyas001
@name:      Yaseen Hull
@Ass 3 OS:  Page replacement algorithms 
"""
import random
import sys

Q = list();     # used as Fifo queue
lruQ = list();  # used as lru queue
optQ = list();  # used as opt queue


pages = list(); # storage for page reference string
poplist = list(); # used in conjuction with Opt algorithm

pglist = [8, 5, 6, 2, 5, 3, 5, 4, 2, 3, 5, 3, 2, 6, 2, 5, 6, 8, 5, 6, 2, 3, 4, 2, 1, 3, 7, 5, 4, 3, 1, 5] # test page reference string

def pageGenerate():
    for i in range(10): # user specifies number of pages as range
        pages.append(random.randint(0,9)) # randomly generates page reference string

def printQ(x): # to print page reference string or que (e.g pages, Q, lruQ, optQ)
    return x

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
FIFO IMPLEMENTATION (First In First Out)
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def insertQ(data):
    if data not in Q:
        Q.insert(0,data) # insert data at index 0
        return True      # if data is inserted return true for page fault
        
def popQ(Q):
    if len(Q) > 0: # pop data from queue at last index
        Q.pop()
      
    else:
        return "Queue is empty"
        
def sizeQ(Q):
    return len(Q)

def FIFO(size,pages):
 
    pgf = 0
    
    for i in range(len(pages)): 
        state = insertQ(pages[i])
        if state == True:
           pgf += 1     #increment pgf (pagefaults) upon successful insertion
       
        if sizeQ(Q) > size: # retain queue size to frame size
            popQ(Q)
   
    return pgf

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
LRU IMPLEMENTATION (Least Recently Used)
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def insertlruQ(data,size):

    if data not in lruQ:

        lruQ.insert(0,data)

        if sizeQ(lruQ) > size:
            leastRU = lruQ[size] # find LRU page (least recently used)
            mostRU = lruQ[0]     # find MRU page (most recently used)

            lruQ.remove(leastRU) # remove LRU page
        return True
    
    else:
        lruQ.remove(data) # update page to MRU on page hit
        lruQ.insert(0,data)
        mostRU = lruQ[0]

def LRU(size,pages):

    pgf = 0
    
    for i in range(len(pages)):
        state = insertlruQ(pages[i], size)
        if state == True:
            pgf +=1     #increment pgf (pagefaults) upon successful insertion
            
    return pgf


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
OPTIMAL IMPLEMENTATION
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def removeQ():
    if len(poplist) > 0:
        poplist.remove(poplist[0]) # remove page from poplist
    else:
        return "Queue is empty"

def insertoptQ(data,size):
   
    if data not in optQ:
        optQ.insert(0,data)

        removeQ() #pops from poplist
  
        if sizeQ(optQ) > size: # if que size is bigger than frame
            
            replace = check(size) # checks which value to replace in current queue
            optQ.remove(replace)

        return True
      
    else:
        removeQ()
        return False

def check(size):
    
    maxlife = 0 # assigned to page which is to be used not in recent future
    ind = 0
    
    for i in range(size,0,-1): # start at bottom of stack
        
        occurence = poplist.count(optQ[i]) # determines the number of occurences of a value currently in queue
        
        
        if occurence == 0: # if the occurences is 0 the associated value is set to maxlife
            maxlife = optQ[i] 
            break;
        
        elif occurence != 0 :
            prev = ind 
            prevmx = maxlife 
            ind = poplist.index(optQ[i]) # gets index of current page in poplist while looping through optimal queue
            
            maxlife = optQ[i] 
            
            if ind < prev: # checks if previous index is more than current index
                maxlife = prevmx 
                ind = prev
   
    return maxlife



def OPT(size, pages):
  
    pgf = 0
  
    for i in range(len(pages)):
        poplist.append(pages[i])
    
    for i in range(len(pages)):

        state = insertoptQ(pages[i], size)
        if state == True:

           pgf += 1     #increment pgf (pagefaults) upon successful insertion
    
    return pgf

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
MAIN
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def main():
    #...TODO...
    pageGenerate() # generates random reference string 
    size = int(sys.argv[1])
    
    # to use pglist from above just replace 'pages' with 'pglist'
    print( 'FIFO', FIFO(size,pages), 'page faults.') 
    print('LRU', LRU(size,pages), 'page faults.') 
    print( 'OPT', OPT(size,pages), 'page faults.')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: python paging.py [number of pages]')
    else:
        main()
