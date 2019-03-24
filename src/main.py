import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import os
import os.path
import folium
import sys
import time


# clear screen
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
 
 
def task1(conn):
    # notify
    print('Running task 1\n')

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
        print('[1] Q1')
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
