import sqlite3
import zipfile
import csv
import pandas as pd
import os
import time

#conn = sqlite3.connect('employee.db')
cities = ("JFK","ALT","DFW")
weather_id = 0
flight_id = 0

def extractFile(name,connection,tableName):
    archive = zipfile.ZipFile(name, 'r')
    zippedfiles = archive.namelist()
    archive.extractall()

    f = ""
    for zfile in zippedfiles:
        if(zfile.endswith(".csv")):
            f = zfile
    print(f)

    c = connection.cursor()
    columns = getColumns("fields.txt")
    #cities = ("JFK","ALT","MIA")
    with open(f, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if(row["Origin"] in cities and row["Dest"] in cities):
                formatAirlineRow(row)
                command = "insert into " + tableName + " values " + columns
                c.execute(command,row)

    connection.commit()

    for f in zippedfiles:
        os.remove(f)

def extractAllFiles(folder,connection):
    tableName = "flights"

    c = connection.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS " + tableName + " "+ getColumns("fields.txt", True))

    for fname in os.listdir(folder):
        if(fname.endswith('.zip')):
            name = folder + fname
            extractFile(name, connection, tableName)

def extractWeatherFiles(folder, connection, tableName):
    c = connection.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS " + tableName + " "+ getColumns("weatherfields.txt", True))
    connection.commit()

    columns = getColumns("weatherfields.txt")
    for airport in cities:
        f = folder + airport + ".csv"
        print(airport)
        with open(f, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row["AIRPORT"] = airport
                formatWeatherRow(row)
                command = "insert into " + tableName + " values " + columns
                c.execute(command,row)
    connection.commit()

def formatAirlineRow(row):
    row["DeptWeatherID"] = None
    row["ArrWeatherID"] = None
    row["CRSDepTime"] = row["CRSDepTime"][0:2] + ":" + row["CRSDepTime"][2:4]
    row["CRSArrTime"] = row["CRSArrTime"][0:2] + ":" + row["CRSArrTime"][2:4]
    row["ID"] = flight_id
    incrementFlights()

def formatWeatherRow(row):
    d = row["DATE"]
    row["DATE"], row["TIME"] = d.split(" ")
    row["ID"] = weather_id
    m, d, y = row["DATE"].split("/")
    row["DATE"] = "20" + y + "-" + m.zfill(2)  + "-" + d.zfill(2)
    incrementWeather()
    # row["HOUR"], row["MINUTE"] = [val.zfill(2) for val in row["TIME"].split(":")]

def incrementWeather():
    global weather_id
    weather_id += 1

def incrementFlights():
    global flight_id
    flight_id += 1

def getColumns(f_file, table=False):
    file = open(f_file, "r")
    fields = []
    for line in file:
        if(table):
            fields.append(line.strip())
        else:
            line.strip().split(" ")
            fields.append(line.strip().split(" ")[0])

    if(table):
        return "( " + ", ".join(fields) + ")"


    return "(" + ", ".join(":"+field for field in fields) + ")"



def main():
    connection = sqlite3.connect("weatherflights.db")
    folder = "/Users/marianelapimienta/Documents/AirlineData/"
    extractAllFiles(folder, connection)

    folder = "/Users/marianelapimienta/Documents/WeatherData/"
    extractWeatherFiles(folder,connection,"weather")


    #print(getColumns("weatherfields.txt"))
    connection.close()
    #addtoDB()

if __name__ == '__main__':
    main()
