import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import os
import os.path
import folium
import sys
import time
from datetime import date

def count(fn):
        # helps count the number of times a function has been called
        # https://stackoverflow.com/questions/33312853/simple-way-to-count-the-number-of-times-def-fx-is-evaluated

        def wrapper(*args, **kwargs):
            wrapper.called+= 1
            return fn(*args, **kwargs)
        wrapper.called= 0
        wrapper.__name__= fn.__name__
        return wrapper

def get_valid_year(prompt,min=0, max = date.today().year):
    # gets and validates inputs in the form of years
    # - prompt is the string to use when asking the user for input

    valid = False
    while not valid:
        year = input(prompt)
        if not year.isnumeric():
            print("Invalid year. Please enter the year as a number in YYYY format.")
            continue
        else:
            year = int(year)
            if year < min:
                # note that negatives are caught earlier in this function
                # because they have non-numeric characters
                # therefore this will only apply when the user enters a backward range
               
                print("The end year cannot be smaller than the start year.")
                continue
            if year > max:
                print("This year has not yet occured.")
                continue
            valid = True
            return year

# clear screen
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
 
@count 
def task1(conn):
    # notify
    print('Running task 1\n')
    
    # get input 
    start_year = get_valid_year("Enter Start Year (YYYY): ")
    end_year = get_valid_year("Enter End Year (YYYY): ", min = start_year)
    crime = input("Enter Crime Type: ")
    
    # read query -- generate results of monthly crimes of the given type
    # between the given years, inclusive

    try:
        query = open('1.sql','r')
        sql = query.read()
        query.close()

    except Exception as e:
        print(e)
        return

    try:
        df = pd.read_sql_query(sql,conn,params=[start_year,end_year,crime])
    except Exception as e:
        print(e)
        return
    
    # replace None with 0 
    # (fixes No Numerical Data problem in the case of no results)
    df.fillna(value=0,inplace=True)
    
    # generate bar chart 
    plot = df.plot.bar(x="Month")
    plt.plot()
    plt.title("Total monthly incidents of "+crime+" from " + str(start_year)+" to "+str(end_year)
)
    # save plot
    plt.savefig("Q1-"+str(task1.called))
    print("\nSaved the bar plot " + "Q1-"+str(task1.called)+ " to your working directory.")

    return

  
def task2(conn):
    # notify
    print('Running task 2\n')
    
def task3(conn):
    # notify
    print('Running task 3\n')   
    
def task4(conn):
    # notify
    print('Running task 4\n')
    
def main():
    # check for DB param
    if len(sys.argv) != 2:
        print('Error: expected exactly one arg (the relative path of the database to connect to)')
        return

    # check that DB exists
    if not os.path.isfile(sys.argv[1]):
        print('The DB at ./{} does not exist'.format(sys.argv[1]))
        return

    # connect to DB
    try:
        print("Connecting to DB at ./{}".format(sys.argv[1]))
        conn = sqlite3.connect(sys.argv[1])
    except sqlite3.Error as e:
        print(e)
        return

    # use dict since python has no switch
    tasks = {}
    tasks['1'] = task1
    tasks['2'] = task2
    tasks['3'] = task3
    tasks['4'] = task4


    # message pump
    while(True):
        # display API
        print('\n--- ASSIGNMENT 4 PROGRAM ---')
        print('What do you want to know?')
        print('[1] Bar Plot of Monthly Crimes in Year Range')
        print('[2] Q2')
        print('[3] Q3')
        print('[4] Q4')
        print('[E] Exit')
        action = input("Enter your choice: ")

        # exit condition
        if action.upper() == 'E':
            break

        # execute action
        
        try:
            print('') # newline
            tasks[action](conn)
        except:
            print('Error: invalid action')
            time.sleep(1.5)
            clear()
    
if __name__== "__main__":
    main()
