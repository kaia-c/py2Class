# -*- coding: UTF-8 -*-
######################################################################################
# Assignment 1
# CSC 217, Advanced Python
# assign1v3.py
# Programmers:  Kaia Chapman, Karna Johnson, Drew Lane
# Date Created: January 29, 2015
# Date of Final Update: February 4, 2015
######################################################################################
# Take 5 integers and calculate the min, max, mean, median and stDev, while validating all
# user input and offering exit on each input, in order to show the following:
#
# a) Arithmetic’s and variables
# b) if/else
# b) Nested “if” statements (3 levels)
# c) Loops
#   i)For
#   ii)While
# e) Strings
# f) Tuples
# g) Lists or Dictionaries
# h) Exceptions
######################################################################################
import time #for the log_file
import os #for the press any key to exit
import math # for calculating median

#Function for the end of the program
def end(success=False):
    """Arg=optional True for success completion, default False for user-interrupt fail
    calls log with status and and exits immediately on fail, and on success ends on
    char input|enter input if not windows"""
    #Printing "Goodbye
    print("\nGoodbye.")
    #if success is true and the os name equals 'nt'
    if success and os.name == 'nt':
        #use a system pause
        os.system("pause")
    #If just success is true
    elif success:
        #asking for user input to press enter to exit the program
        input("Press [Enter] to Exit Program.")#b)if examples
    #Using the function log() to write to the file 
    #if success --finish the rest
    log("\nRun Sucessful." if success else "\nUser Terminated Run Early.", "\nProgram Terminating at ", time.strftime("%c"))
    exit()

def validateInt(rawInput):
    """Arg = input str,
    return = float for input of float[-100000,100000]; else returns false | calls end on [q]uit input """
    if len(rawInput) > 32:
        return False
    testInput=[x for x in rawInput if ord(x) > 44 and ord(x) < 123]
    rawInput=""
    for i in testInput:#c) i) for loop
        rawInput+=i
    try:
        floatInput=float(rawInput) 
    except ValueError: #h) Exceptions
        if rawInput.lower()=="q":
            end()
        else:
            return -1000001
    return floatInput if (floatInput >= -1000000 and floatInput <= 1000000 ) else  -1000001 #not False because False==0

def getSampleInput():
    """returns bool sample = true if input represents sample; false if it's a population| calls end on [q]uit input """
    sample=population=False    
    while not sample and not population:
        rawAns=input("Before we get started, are these numbers:\n\t1)\tSamples from a population, or \n\t2)\tThe entire population\n[Enter 1 or 2] :")
        if str(rawAns).lower()!="q":
            if len(str(rawAns))<3 and str(rawAns).isdigit():
                if int(rawAns)==1:#c) 3 nested if's! Yes, there are excuses to get there, but there you go.
                    return True
                elif int(rawAns)==2:
                    return False
        else:
            end()

def getInput():
    """Loops on optaining and processing valid input, returns list of 5 floats and bool sample (true for sample, false for population)"""
    sample = getSampleInput()
    print("\nThanks! Now, I'll need 5 numbers (examples: 42, 12,525, 12525, -53.12345).\n")
    numList=[]#g) list
    while len(numList)<5:#d) ii] while loop
        num=validateInt(str(input("Enter a number: ")))#e) strings (input example)
        if num != -1000001:
            numList.append(num)
        else:
            print("Sorry, I only accept numerical input in the range of += 1,000,000.\n\nPlease try again.\n")
    return (numList, sample)

def calc(numList):
    """arg = list of floats
    return = tuple as (smallest float, largest float, average of floats)"""
    return (min(numList), max(numList), (sum(numList)/float(len(numList))))#f) tuple 

def calcStr(calcTup, stDev, calcMedian):
    """Returns formatted string of answers to calculations"""#e) strings (format example)
    return ("\tThe smallest value is : %.8g\n\tThe largest value is: %.8g\n\tThe average value is: %.8g\n\tThe standard deviation is: %.8g.\n\tThe median is: %.8g\nThanks for using this program!\n"%(calcTup[0], calcTup[1], calcTup[2], stDev, calcMedian ))#tuple
    

def sort(numList):
    """Sort function with nested if's"""
    tmpList=list(numList)
    sortedList=[]
    lowest=tmpList[0]
    i=0
    while len(tmpList) > 0:
        if tmpList[i] < lowest:
            lowest = tmpList[i]
        i+=1
        if i == len(tmpList):
            sortedList.append(lowest)
            tmpList.remove(lowest)
            if tmpList:
                lowest = tmpList[0]
            i=0
    return sortedList

def calcMedian(numList):
    """Calls sort on list. Calculates the median"""
    numList = sort(numList)
    if len(numList) < 1:
        return None
    if len(numList) % 2 == 1:
         return numList[((len(numList)+1)//2)-1]
    if len(numList) % 2 ==0:
        return float(sum(numList[(len(numList)//2)-1:(len(numLst)//2)+1]))//2.0
    

def stDev(numList, isSample):#a) arithmatic 
    """Args = list of floats, bool isSample
    return = standard deviation of the population or sample provided
    Why is this here? = I needed some arithmatic still :)"""
    return ((sum([(x-(sum(numList)/float(len(numList))))**2 for x in numList])/ ((len(numList)-1) if isSample else len(numList)))**(1/2))

def log(str1, str2="", str3=""):#h) file output
    """outputs logs of 1-3 provided string parameters to file at log_file.txt"""
    with open("log_file.txt", 'a') as log:
        log.write("%s%s%s"%(str1, str2, str3))

def main():
    """Main driver. Using functions created from above"""
    log("\n=====================================\nNew Session beginning ", time.strftime("%c"), "\n")
    print("Welcome to Assignment 1. I will print the minumum, maximum, average value, \nmedian, and standard deviation of exactly 5 numbers.\n\nYou will be prompted to enter 5 numbers - \n\tplease keep your inputs between -1,000,000 and 1,000,000.\n\nYou can enter \"Q\" to Quit at any time.\n")
    numList, sample=getInput()
    log("Sample:" if sample else "Population:", str(numList))
    calcTup = calc(numList)
    calcMed = calcMedian(numList)
    calcString = calcStr(calcTup, stDev(numList, sample), calcMed)
    log("\nResults in output:\n", calcString)
    print(calcString)
    end(True)    
main()



