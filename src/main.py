import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import os
import os.path
import folium
import sys
import time

# check if a variable is an integer
def isInt(x):
    try:
        int(x)
        return True
    except:
        return False

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

    # get the interval of years [a, b]
    print('Enter years for the interval [a, b]')
    a = input('a: ')
    b = input('b: ')

    # validate
    if not ( isInt(a) and isInt(b) ):
        print('Error: a,b must be integers')
        return

    b = int(b)
    a = int(a)
    
    if b < a:
        print('Error: b cannot be less than a')
        return

    # get N for top-n neighborhoods
    print('Enter n to display the top-n neighborhoods')
    n = input('n: ')

    # validate
    if not isInt(n):
        print('Error: n must be an integer')
        return
    n = int(n)

    if n < 0:
        print('Error: n must be positive and non-zero')

    # read SQL
    try:
        f = open('4a.sql','r')
        sql = f.read()
        f.close()
    except Exception as e:
        print(e)
        return

    # execute (fetch all)
    args = (a, b)
    cur = conn.cursor()
    try:
        cur.execute(sql, args)
    except sqlite3.Error as e:
        print(e)
        return

    # fetch top-n
    rows = []
    for row in cur:
        #if len(rows) == n and row[3] != rows[n-1][3]:
        #    break
        rows.append(row)

    # read SQL
    try:
        f = open('4b.sql','r')
        sql = f.read()
        f.close()
    except Exception as e:
        print(e)
        return

    # execute (fetch all)
    topCrimes = []
    for i in range(0, len(rows)):
        args = (a, b, rows[i][0])
        cur = conn.cursor()
        try:
            cur.execute(sql, args)
        except sqlite3.Error as e:
            print(e)
            return
        # don't know syntax for single, so abuse loop
        for row in cur:
            topCrimes.append(row[0])
            break

    assert(len(topCrimes) == len(rows))
    if len(rows) == 0:
        print("No data for that year range. Skipping map generations.")
        return

    # Now plot the DataFrames on a map...
    m = folium.Map(location=[rows[0][1], rows[0][2]], zoom_start=12)
    for i in range(0, len(rows)):
        folium.Circle(
            location=[ rows[i][1], rows[i][2] ],
            popup= "{} <br> {} <br> {}".format(rows[i][0], topCrimes[i], rows[i][3]),
            radius=rows[i][3]*500,
            color='crimson',
            fill=True,
            fill_color='crimson'
        ).add_to(m)

    # Search for an available filename and save the map to an HTML file
    prefix = "Q4-"
    i=1
    while(True):
        if os.path.isfile("%s%i.html" % (prefix, i)):
            i+=1
        else:
            break
    m.save("%s%i.html" % (prefix, i))
    print("Map generated! > '%s%i.html'" % (prefix, i))

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
