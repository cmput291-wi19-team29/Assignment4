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
 
# check if a variable is an integer
def isInt(x):
    try:
        int(x)
        return True
    except:
        return False

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
    print('Mapping neighbourhood populations...')
    
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

    print("Enter number of locations: ", end='')
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

    # Search for an available filename and save the map to an HTML file
    prefix = "Q2-"
    i=1
    while(True):
        if os.path.isfile("%s%i.html" % (prefix, i)):
            i+=1
        else:
            break
    m.save("%s%i.html" % (prefix, i))
    print("Map generated! > '%s%i.html'" % (prefix, i))
    
def task3(conn):
    # TODO adjusting circle radius size based on crime type would be ideal, but whatever
    print('Reading data...\n')

    try:
        query_a = open('3a.sql','r') # Main query
        query_b = open('3b.sql','r') # Available crime types
        query_c = open('3c.sql','r') # Available year range
        sql_a = query_a.read()
        sql_b = query_b.read()
        sql_c = query_c.read()
        query_a.close()
        query_b.close()
        query_c.close()
    except Exception as e:
        print(e)
        return

    # Extract the data from the extra queries
    cur = conn.cursor()
    try:
        cur.execute(sql_b);
        types_raw = cur.fetchall()
        crime_types = []
        for t in types_raw:
            crime_types.append(t[0])
        cur.execute(sql_c);
        ranges = cur.fetchall()
        min_year = ranges[0][0]
        max_year = ranges[0][1]
    except Exception as e:
        print(e)
        return

    print('There is data from %i to %i.\n' % (min_year, max_year))
    print('The types of crimes are:')
    for crime in crime_types:
        print(crime)
    print()

    # Could this be inside a loop instead?
    try:
        print('Enter start year (YYYY): \t', end='')
        start = int(input())
        if start < min_year or start > max_year:
            raise Exception("Error: No data for that year!")
        print('Enter end year (YYYY): \t\t', end='')
        end = int(input())
        if end > max_year or end < min_year:
            raise Exception("Error: No data for that year!")
        if start > end:
            raise Exception("Error: start year is greater than end year")
        print('Enter crime type: \t\t', end='')
        crime = input()
        if crime not in crime_types:
            raise Exception("\nError: Crime not recognized.\nEnter the crime exactly as it appears above. It's case sensitive!")
        print('Enter number of neighbourhoods: ', end='')
        N = int(input())
        if N <= 0:
            raise Exception("Error: Please enter a valid number of neighbourhoods.")
        #print(start, end, crime, N)
    except Exception as e:
        print(e)
        return

    # Now that we have all the parameters, execute the main query
    try:
        cur.execute(sql_a, (crime, start, end))
    except Exception as e:
        print(e)
        return
    df = pd.DataFrame(cur.fetchall())
    #print(df)

    # Filter the results
    if len(df) > N:
        # TOP N neighbourhoods. Check for ties.
        bound = N-1
        for i in range(N, len(df)):
            #print("Checking ", i-1, i)
            if df[1][i-1] != df[1][i]: # The crime counts are hardcoded to column 2...
                break
            else:
                bound = i
        top = df.iloc[0:bound+1,:]
    else:
        # There are fewer than N neighbourhoods, so just include all of them.
        print("NOTE: There are only %i neighbourhoods; they will all be mapped.\n" % len(df))
        top = df
    print('\n', top, '\n')
    
    # Get coordinates for mapping
    try:
        query_d = open('3d.sql','r') # Neighbourhood coordinates
        sql_d = query_d.read()
        query_d.close()
        cur.execute(sql_d);
        coords = cur.fetchall()
        #for c in coords:
        #    print(c[0], c[1], c[2])
    except Exception as e:
        print(e)
        print("Unable to map results!")
        return

    # Concatenate the crime statistics and the neighbourhood coordinates
    results = []
    for i in range(0, len(top)):
        found = False
        for c in coords:
            if top[0][i] == c[0]:
                # Match! We need these coordinates.
                results.append( (top[0][i], c[1], c[2], top[1][i]) )
                found = True
                break
        if not found:
            print("WARNING: no coordinates found for %s, it won't be mapped" % (top[0][i]))
        
    # Now map the results
    m = folium.Map(location=[results[0][1], results[0][2]], zoom_start=12)
    for neighbourhood in results:
        folium.Circle(
            location=[ neighbourhood[1], neighbourhood[2] ],
            popup= "%s <br> %s: %i" % (neighbourhood[0], crime, neighbourhood[3]),
            radius=int(neighbourhood[3])*2, # Multiplier can be adjusted
            color='crimson',
            fill=True,
            fill_color='crimson'
        ).add_to(m)
    # Search for an available filename and save the map to an HTML file
    prefix = "Q3-"
    i=1
    while(True):
        if os.path.isfile("%s%i.html" % (prefix, i)):
            i+=1
        else:
            break
    m.save("%s%i.html" % (prefix, i))
    print("Map generated! > '%s%i.html'" % (prefix, i))
    
def task4(conn):
    # notify
    print('Running task 4\n')

    # get the interval of years [a, b]
    print('Enter years for the interval [a, b]')
    a = get_valid_year("Enter Start Year (YYYY): ")
    b = get_valid_year("Enter End Year (YYYY): ", min = a)

    while True:
        # get N for top-n neighborhoods
        print('Enter n to display the top-n neighborhoods')
        n = input('n: ')

        # validate
        if not isInt(n):
            print('Error: n must be an integer')
            continue
            
        n = int(n)

        if n < 0:
            print('Error: n must be positive and non-zero')
            continue
        
        break

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
        if len(rows) == n and row[3] != rows[n-1][3]:
            break
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
            radius=rows[i][3]*700,
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
        print('[1] Bar Plot of Monthly Crimes in Year Range')
        print('[2] Map the most and least populous neighbourhoods')
        print('[3] Map the occurences of a particular type of crime')
        print('[4] Map the ratio of crimes and population, and top crime')
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
