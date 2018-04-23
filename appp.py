from flask import Flask,render_template,request,jsonify
import pymysql
import time
import hashlib
import json
import csv
import random
from datetime import datetime
import sys,os
from dateutil import parser
from sklearn.cluster import KMeans
from flask import Flask, render_template,request
import os
import pymysql
import csv
# Array processing
import numpy as np
# Data analysis, wrangling and common exploratory operations
import pandas as pd
from pandas import Series, DataFrame
import re
# For visualization. Matplotlib for basic viz and seaborn for more stylish figures
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


headers=[]
#hostname = ''
username = ''
password = ''
database = ''
myConn = pymysql.connect(host='', user=username, passwd=password,db=database,local_infile=True)

app = Flask(__name__)


@app.route('/')
def index():
     return render_template('index.html')

# creating table using the csv and importing the data
@app.route('/createtable',methods=['POST'])
def createtable():
    
    cursor = myConn.cursor()
    file_name = 'C:/Users/ShilpiVMStudent/Desktop/CSEFall2018.csv'
    droptbl = "DROP TABLE IF EXISTS cloud4.csefall2018;"
    cursor.execute(droptbl)
    with open(file_name, 'rt', encoding = 'Latin-1') as csvfile:
        reader = csv.reader(csvfile,quotechar='`')
        headers = next(reader)
    
    start_time = time.time()
    
    PKquery="create table if not exists csefall2018("
    for i in range(0, len(headers)):
         PKquery +=  headers[i] + " varchar(100),"
    PKquery += "columnID int AUTO_INCREMENT PRIMARY KEY)"
    cursor.execute(PKquery)
    
    csvquery="""LOAD DATA LOCAL INFILE 'C:/Users/ShilpiVMStudent/Desktop/CSEFall2018.csv'
          INTO TABLE csefall2018 FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;"""
    cursor.execute(csvquery)
    myConn.commit()
    
    end_time = time.time()
    time_diff = end_time - start_time   

    return render_template('index.html',time_taken=time_diff,success = "Data inserted into database")


 

@app.route('/mymavlogin',methods=['POST'])
def login():
    Student_username = request.form['usrname']
    S_password = request.form['pswd']
    cursor = myConn.cursor()
    login_query = "SELECT GivenName from Students where Username = %s and Password = %s"
    cursor.execute(login_query,(Student_username,S_password))
    S_data = cursor.fetchall()
    if len(S_data) != 1:
        return render_template('login.html', error = "User does not exist")
    return render_template('search.html')




@app.route('/searchpg', methods=['POST'])
def search():
    Department = request.form['dept']
    Courseno = request.form['courseno']
    cursor = myConn.cursor()
    search_query = "SELECT Subject, ClassNumber, MaxEnroll from CSEFall2018 where SectionNumber = %s and CourseNumber = "+str(Courseno)
    cursor.execute(search_query,(Department))
    Search_data = cursor.fetchall()
    if len(Search_data) == 0:
        return render_template('search.html', error_msg = "Course does not exist")
    return render_template('class_section.html')


@app.route('/kmeans', methods=['POST'])
def kmeans():
    df = pd.read_csv('CSEFall2018.csv', encoding='latin1')
    f1 = df['CourseNumber'].values
    f2 = df['MaxEnroll'].values
    X = np.array(list(zip(f1, f2)))
    plt.rcParams['figure.figsize'] = (16, 9)
    kmeans = KMeans(int(request.form['numberofclusters']))
    kmeans = kmeans.fit(X)    
    labels = kmeans.predict(X)    
    centroids = kmeans.cluster_centers_
    points = kmeans.labels_
    centrd = []
    x = np.arange(30)
    ys = [i+x+(i*x)**2 for i in range(30)]
    colors = cm.rainbow(np.linspace(0, 1, len(ys)))
    plt.figure()
    colour=['red','blue','green','pink','black','yellow','fluroscent','purple']
    for i, col in zip(range(int(request.form['nclusters'])), colors):
        groups = kmeans.labels_ == i
        centroid = kmeans.cluster_centers_[i]
        centrd.append(centroid)
        
        plt.plot(X[groups, 0], X[groups, 1], 'w', markerfacecolor=col, marker='.')
        plt.plot(centroid[0], centroid[1], '*', markerfacecolor=col, markeredgecolor='k', markersize=6)
    plt.title('kmeansScatter')
    print(groups)
    plt.grid(True)
    fileno = int(random.randrange(500,1000))
    plt.savefig('static/test'+str(fileno)+'.png')
    file = 'static/test'+str(fileno)+'.png'
    return render_template('Kplotscatter.html',fileno = file)



    
@app.route('/randomfunc',methods=['POST'])
def randomfunc():    
    Random1 = random.randrange(30,60)
    Random2 = random.randrange(50,100)
    mag1= int(Random1)  
    mag2= int(Random2)  
    cursor = myConn.cursor()
    query2 = "SELECT City, Latitude FROM starbucks WHERE Latitude between %s and %s  LIMIT 5"
    cursor.execute(query2,(mag1,mag2))
    randomlat = cursor.fetchall()
    fileno = int(random.randrange(100,1000))
    myFile = open('./static/file'+str(fileno)+'.csv', 'w',newline='')
    with myFile:
        cw = csv.writer(myFile)
        print("in file write")
        cw.writerow([i[0] for i in cursor.description])
        cw.writerows(randomlat)    
    return render_template('pie.html',fileno = str(fileno))




@app.route('/inputbar',methods=['POST'])
def inputfieldbar():
    voteinput1 = request.form['votpop1']
    voteinput2 = request.form['votpop2']
    cursor = myConn.cursor()
    inputquery = "SELECT StateName, PercentReg from statevote where votepop between %s and %s limit 5"
    cursor.execute(inputquery,(voteinput1,voteinput2))
    popdata = cursor.fetchall()
    fileno = int(random.randrange(500,1000))
    myFile = open('./static/file'+str(fileno)+'.csv', 'w',newline='')
    with myFile:
        cw = csv.writer(myFile)
        print("in file write")
        cw.writerow([i[0] for i in cursor.description])
        cw.writerows(popdata)
    return render_template('barchart.html', fileno = str(fileno))



@app.route('/scatter',methods=['POST'])
def scatter():    
    cursor = myConn.cursor()
    RS1 = random.randrange(0,50)
    magnst= int(RS1)   
    cursor = myConn.cursor()
    scaterquery = "SELECT depth, nst,id FROM eqcitydata WHERE magNst = %s limit 30"
    cursor.execute(scaterquery,magnst)
    scdata = cursor.fetchall()
    fileno = int(random.randrange(200,1000))
    myFile = open('./static/data'+str(fileno)+'.csv', 'w',newline='')
    with myFile:
        cw = csv.writer(myFile)
        print("in file write")
        cw.writerow([i[0] for i in cursor.description])
        cw.writerows(scdata)      
    return render_template('scatterplot.html',fileno = str(fileno))



     
  
port = os.getenv('PORT', '8080')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(port))