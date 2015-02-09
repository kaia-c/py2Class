# -*- coding: UTF-8 -*-
######################################################################################
# Assignment 1
# CSC 217, Advanced Python
# assign1v3.py
# Programmers:  Kaia Chapman, Karna Johnson, Drew Lane
# Date Created: January 29, 2015
# Date of Final Update: February 9, 2015
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


def end(success=False):
    #################################################################################
    """Arg=optional True for success completion, default False for user-interrupt fail
    calls log with status and and exits immediately on fail, and on success ends on
    char input|enter input if not windows"""
    #################################################################################
    print("\nGoodbye.")
    log("\nRun Successful." if success else "\nUser Terminated Run Early.", "\nProgram Terminating at ", time.strftime("%c"))
    if success and os.name == 'nt':#if windows and success ==True
        os.system("pause")#use system pause
    elif success:#if not windows and success ==True
        input("Press [Enter] to Exit Program.")# have user push enter to end run
    exit()#else for success==False just exit

def validateFloat(rawInput):
    #################################################################################
    """Arg = input str,
    return = float for input of float[-100000,100000]; else returns false | calls end on [q]uit input """
    #################################################################################
    if len(rawInput) > 20:#return error if user entered too long of string without further checking
        return -1000001 #-1000001, out of range int, is error flag not False because False==0
    testInput=[x for x in rawInput if ord(x) > 44 and ord(x) < 123]#put values in range of numbers/letters and - sign in list, exclude commas + other unneeded chars
    rawInput=""
    for i in testInput:#c) i) for loop puts chars in list into a string
        rawInput+=i
    try: 
        floatInput=float(rawInput)  #attempt to convert to a float
    except ValueError: #if that doesn't work
        if rawInput.lower()=="q": #check if input was "q", quit signal, if so call end()
            end()
        else: #otherwise return error flag
            return -1000001 
    return floatInput if (floatInput >= -1000000 and floatInput <= 1000000 ) else  -1000001  #if float conversion worked return floats in range or error flag for out of range

def getSampleInput():
    #################################################################################
    """returns bool sample = true if input represents sample; 
    false if it's a population| calls end on [q]uit input """
    #################################################################################
    #Setting sample and population to false
    sample=population=False    
    while not sample and not population:#run until user gives sample/population choice or [Q]uit input
        #asking for the input of either samples of the population or the entire population
        rawAns=input("Before we get started, are these numbers:\n\t1)\tSamples from a population, or \n\t2)\tThe entire population\n[Enter 1 or 2] :")
        if str(rawAns).lower()!="q": #if the answer is not equal to 'q'
            if len(str(rawAns))<3 and str(rawAns).isdigit():#if they entered a short digit
                if int(rawAns)==1:#if they indicated sample
                    return True #return true
                elif int(rawAns)==2:#if they indicated population
                    return False #return false
        else:#if user entered "q", end()
            end()

def getInput():
    #################################################################################
    """Loops on obtaining and processing valid input, 
    returns list of 5 floats and bool sample (true for sample, false for population)"""
    #################################################################################
    sample = getSampleInput() #assigning sample to the function getSampleInput()
    #a print statement to ask for 5 numbers
    print("\nThanks! Now, I'll need 5 numbers (examples: 42, 12,525, 12525, -53.12345).\n")
    numList=[] #list
    #While the length of numList is less than 5
    while len(numList)<5:
        #assigning num to the function validateFloat()
        num=validateFloat(str(input("Enter a number: ")))
        if num != -1000001:#if not error flag
            #add num to numList
            numList.append(num)
        #otherwise    
        else:
            #printing a statement to make sure that only numerical values are inputed
            print("Sorry, I only accept numerical input in the range of += 1,000,000.\n\nPlease try again.\n")
    #return numList and sample
    return (numList, sample)

def calc(numList):
    #################################################################################
    """arg = list of floats
    return = tuple as (smallest float, largest float, average of floats)"""
    #################################################################################
    return (min(numList), max(numList), (sum(numList)/float(len(numList))))#f) tuple 

def calcStr(calcTup, stDev, calcMedian):
    #################################################################################
    """Returns formatted string of answers to calculations"""
    #################################################################################
    return ("\tThe smallest value is : %.8g\n\tThe largest value is: %.8g\n\tThe average value is: %.8g\n\tThe standard deviation is: %.8g.\n\tThe median is: %.8g\nThanks for using this program!\n"%(calcTup[0], calcTup[1], calcTup[2], stDev, calcMedian ))#tuple


def sort(numList):
    #################################################################################
    """Sort function with nested if's"""
    #################################################################################
    tmpList=list(numList) # Copy the list into a temporary list
    sortedList=[] # Create a new list to store the sorted list
    lowest=tmpList[0] # This is the first entry for comparison
    i=0 # Set loop variable to zero
    while len(tmpList) > 0: # Start looping through list
        if tmpList[i] < lowest: # Compare values
            lowest = tmpList[i] # Assign value if index is smaller
        i+=1 # Increment loop
        if i == len(tmpList): # Check if we have tested all numbers
            sortedList.append(lowest) # Add value to sorted list
            tmpList.remove(lowest) # Remove value from temporary list
            if tmpList: # Check if temporary list is zero
                lowest = tmpList[0] # Assign variable to first entry
            i=0 # Reset variable
    return sortedList # Return the sorted List

def calcMedian(numList):
    #################################################################################
    """Calls sort on list. Calculates the median"""
    #################################################################################
    #sorting numList with the sort function that we created
    numList = sort(numList)
    #if the length of numList is less than 1
    if len(numList) < 1:
        #return none
        return None
    #if the length of numList modulus 2 equals 1    
    if len(numList) % 2 == 1:
        #return numList with the length of numList plus 1 divided by 2 minus 1 in a list
        return numList[((len(numList)+1)//2)-1]
    #if the length of numList modulus 2 equals 0   
    if len(numList) % 2 ==0:
        #return the float of the sum of numList in a list of the length of numList divided by 2 minus 1
        #slicing the length of numList divided by 2 plus 1 all divided by 2
        return float(sum(numList[(len(numList)//2)-1:(len(numList)//2)+1]))//2.0
    

def stDev(numList, isSample):
    #################################################################################
    """Args = list of floats, bool isSample
    return = standard deviation of the population or sample provided
    Formula= square root of (for for i->1 summation to n ((x - x-bar) squared)) / n if population else n-1 for sample)
    Why is this here? = I needed some arithmetic still :)
    """
    #################################################################################
    return ((sum([(x-(sum(numList)/float(len(numList))))**2 for x in numList])/ ((len(numList)-1) if isSample else len(numList)))**(1/2))

def log(str1, str2="", str3=""):
    #################################################################################
    """outputs logs of 1-3 provided string parameters to append to file at log_file.txt"""
    #################################################################################
    with open("log_file.txt", 'a') as log:
        log.write("%s%s%s"%(str1, str2, str3))

def main():
    #################################################################################
    """main driver"""
    #################################################################################
    log("\n=====================================\nNew Session beginning ", time.strftime("%c"), "\n")#print initial log
    #print welcome message
    print("Welcome to Assignment 1. I will print the minimum, maximum, average value, \nmedian, and standard deviation of exactly 5 numbers.\n\nYou will be prompted to enter 5 numbers - \n\tplease keep your inputs between -1,000,000 and 1,000,000.\n\nYou can enter \"Q\" to Quit at any time.\n")
    numList, sample=getInput()#get numList and if it's a sample/population from user input
    log("Sample:" if sample else "Population:", str(numList))#log if sample/population and the numList
    calcTup = calc(numList)#get a tuple == (min of numList, max of numList, mean of numList)
    calcMed = calcMedian(numList)#get the median of the numList
    calcString = calcStr(calcTup, stDev(numList, sample), calcMed)#get a formatted string of calculations in the tuple, by calling stDev, and in the calcMed variable
    log("\nResults in output:\n", calcString)#log the formatted string
    print(calcString)#print the formatted string for user
    end(True) #end, indicating success   
main()



