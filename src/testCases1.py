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

 
def Test1(conn,sql):
    print("small numbers test") 
    print("Getting Homicides from 2009 to 2017")
    try:
        df = pd.read_sql_query(sql,conn,params=[2009,2017,"Homicide"])
    except Exception as e:
        print(e)
        return -100
    
    # replace None with 0 
    # (fixes No Numerical Data problem in the case of no results)
    df.fillna(value=0,inplace=True)

    expected_data = [[1,6],[2,5],[3,4],[4,8],[5,9],[6,19],[7,8],[8,7],[9,7],[10,2],[11,7],[12,6]]
    expected_data = pd.DataFrame(expected_data,columns=['Month','TotalNum'])

    if df.equals(expected_data):
        print("Test Passed!\n")
        return 1
    else:
        print("Test Failed!!!\n")
        return 0
    
    


def Test2(conn,sql):
    print("large numbers test")
    print("Getting Theft From Vehicle from 2013 to 2015")
    try:
        df = pd.read_sql_query(sql,conn,params=[2013,2015,"Theft From Vehicle"])
    except Exception as e:
        print(e)
        return -100
    
    # replace None with 0 
    # (fixes No Numerical Data problem in the case of no results)
    df.fillna(value=0,inplace=True)

    expected_data = [[1,495],[2,462],[3,499],[4,557],[5,576],[6,682],[7,701],[8,744],[9,699],[10,687],[11,576],[12,613]]
    expected_data = pd.DataFrame(expected_data,columns=['Month','TotalNum'])

    if df.equals(expected_data):
        print("Test Passed!\n")
        return 1
    else:
        print("Test Failed!!!\n")
        return 0
    
    

def Test3(conn,sql):
    print("nonexistant crime type test")
    print("Getting Arson from 2009 to 2019")
    try:
        df = pd.read_sql_query(sql,conn,params=[2013,2015,"Arson"])
    except Exception as e:
        print(e)
        return -100
    
    # replace None with 0 
    # (fixes No Numerical Data problem in the case of no results)
    df.fillna(value=0,inplace=True)

    expected_data = [[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0],[8,0],[9,0],[10,0],[11,0],[12,0]]
    expected_data = pd.DataFrame(expected_data,columns=['Month','TotalNum'])

    if df.equals(expected_data):
        print("Test Passed!\n")
        return 1
    else:
        print("Test Failed!!!\n")
        return 0
    
    

def Test4(conn,sql):
    print("crime within one year test")
    print("Getting Robbery in 2011")
    try:
        df = pd.read_sql_query(sql,conn,params=[2011,2011,"Robbery"])
    except Exception as e:
        print(e)
        return -100
    
    # replace None with 0 
    # (fixes No Numerical Data problem in the case of no results)
    df.fillna(value=0,inplace=True)

    expected_data = [[1,26],[2,30],[3,30],[4,26],[5,42],[6,13],[7,29],[8,13],[9,14],[10,20],[11,18],[12,15]]
    expected_data = pd.DataFrame(expected_data,columns=['Month','TotalNum'])

    if df.equals(expected_data):
        print("Test Passed!\n")
        return 1
    else:
        print("Test Failed!!!\n")
        return 0
    

def Test5(conn,sql):
    print("no crimes in selected range test")
    print("Getting Sexual Assault from 2006 to 2008")
    try:
        df = pd.read_sql_query(sql,conn,params=[2006,2008,"Sexual Assault"])
    except Exception as e:
        print(e)
        return -100
    
    # replace None with 0 
    # (fixes No Numerical Data problem in the case of no results)
    df.fillna(value=0,inplace=True)

    expected_data = [[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0],[8,0],[9,0],[10,0],[11,0],[12,0]]
    expected_data = pd.DataFrame(expected_data,columns=['Month','TotalNum'])

    if df.equals(expected_data):
        print("Test Passed!\n")
        return 1
    else:
        print("Test Failed!!!\n")
        return 0
    


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

    # read query -- generate results of monthly crimes of the given type
    # between the given years, inclusive

    try:
        query = open('1.sql','r')
        sql = query.read()
        query.close()

    except Exception as e:
        print(e)
        return

    num_tests = 5
    tests_passed=0

    print("Running Tests...")
    tests_passed = Test1(conn,sql) + Test2(conn,sql) + Test3(conn,sql)+ Test4(conn,sql)+Test5(conn,sql)
    print("\n"+str(num_tests)+"/"+str(tests_passed)+" tests passed")
if __name__== "__main__":
    main()
