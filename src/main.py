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
    print('Mapping neighbourhood populations...\n')
    
    try:
        query = open('2.sql', 'r')
        sql = query.read()
        query.close()
    except Exception as e:
        print(e)
        return
    
    cur = conn.cursor()
    try:
        cur.execute(sql)
    except Exception as e:
        print(e)
        return
    
    df = pd.DataFrame(cur.fetchall())

    print("Enter number of locations: ")
    try:
        N = int(input())
        if N<=0:
            raise Exception("Please enter a valid number.")
    except Exception as e:
        print(e)
        return
    
    # Get the top N and bottom N populations...
    # Account for ties: keep extending the end limit until the tie is broken.
    if len(df) > N:
        # TOP N most populous neighbourhoods:
        bound = N-1
        for i in range(N, len(df)):
            #print("Checking ", i-1, i)
            if df[3][i-1] != df[3][i]: # Population counts are hardcoded to column 3...
                break
            else:
                bound = i
        top = df.iloc[0:bound+1,:]

        # BOTTOM N most populous neighbourhoods (LEAST populous)
        bound = len(df)-N
        for i in range(bound, -1, -1):
            #print("Checking ", i, i-1)
            if df[3][i] != df[3][i-1]:
                break
            else:
                bound = i-1
        bot = df.iloc[bound:len(df),:].sort_values(3, ascending=True)

    else:
        # There are fewer than N neighbourhoods, so just map all of them.
        print("NOTE: There are only %i neighbourhoods; they will all be mapped.\n" % len(df))
        top = df
        bot = df
    
    # Now plot the DataFrames on a map...
    m = folium.Map(location=[top[1][0], top[2][0]], zoom_start=12)
    for i in range(0, len(top)):
        folium.Circle(
            location=[ top[1][i], top[2][i] ],
            popup= "%s <br> Population: %i" % (top[0][i], top[3][i]),
            radius=top[3][i]*0.0625, # Multiplier can be adjusted
            color='crimson',
            fill=True,
            fill_color='crimson'
        ).add_to(m)
    for i in range(len(df)-1, len(df)-len(bot)-1, -1):
        folium.Circle(
            location=[ bot[1][i], bot[2][i] ],
            popup= "%s <br> Population: %i" % (bot[0][i], bot[3][i]),
            radius=int(bot[3][i]), # Multiplier can be adjusted
            color='crimson',
            fill=True,
            fill_color='crimson'
        ).add_to(m)

    filename = "2" # could also be changed or taken as input
    m.save("%s.html" % filename)
    print("Map generated! > '%s.html'" % filename)
    
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
        print('[2] Map the most and least populous neighbourhoods')
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
