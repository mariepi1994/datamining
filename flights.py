import sqlite3
from datetime import timedelta
import csv
class Flights():
    def __init__(self,database):
        self.connection = sqlite3.connect(database)
        self.flight_features = ["Month", "DayofMonth", "DayOfWeek",
         "OriginAirportID", "DestAirportID","DOT_ID_Reporting_Airline"]
        self.weather_features = ["HOURLYWindSpeed", "HOURLYWindDirection",
        "HOURLYDRYBULBTEMPC","HOURLYWETBULBTEMPC", "HOURLYStationPressure",
        "HOURLYRelativeHumidity"]
        self.commands = {
            0 : "select ID, FlightDate, Origin, CRSDepTime, Dest, CRSArrTime from flights",
            1 : "Select ID, TIME from weather where AIRPORT = ? and DATE = ?",
            2 : "UPDATE flights SET DeptWeatherID = ? WHERE ID = ?",
            3 : "UPDATE flights SET ArrWeatherID = ? WHERE ID = ?",
            4 : "select * from flights ORDER BY FlightDate, CRSDepTime",
            5 : "select * from weather WHERE ID = ?",
            6 : "select * from weather ORDER BY DATE, TIME",
            7 : "UPDATE weather SET ? = ? WHERE ID = ?",
        }

    """commits weather for flight into DB -- shouldn't call """
    def findFlightWeather(self):
        cur = self.connection.cursor()
        cur.execute(self.commands[0])
        for row in cur:
            flight_id, date, origin, dept_time, destination, arr_time  = row

            cur2 = self.connection.cursor()
            cur2.execute(self.commands[1], (origin, date,) )
            origin_id = self.findClosestTime(dept_time,cur2.fetchall() )

            cur2.execute(self.commands[1], (destination, date,) )
            destination_id = self.findClosestTime(dept_time,cur2.fetchall() )

            cur3 = self.connection.cursor()
            cur3.execute(self.commands[2], (origin_id, flight_id,))
            cur3.execute(self.commands[3], (destination_id, flight_id,))

        self.connection.commit()


    def timeDifference(self,t1,t2):
        h, m = t1.split(":")
        x = timedelta(int(h), int(m))
        h, m = t2.split(":")
        y = timedelta(int(h), int(m))
        return abs(y - x)

    def findClosestTime(self, t1, weather_times): #t1 --> 04:19
        min_diff = timedelta(hours=24, minutes=00)
        index = None
        for t2 in weather_times:
            diff = self.timeDifference(t1,t2[1])
            if(diff < min_diff):
                min_diff = diff
                index = t2[0]

        return index

    def getDictionaryRows(self):
        self.connection.row_factory = self.dict_factory
        cur = self.connection.cursor()
        cur.execute(self.commands[4])
        last_row = {"flight":{}, "origin_weather": {}, "destination_weather": {}}
        for row in cur:
            ret = {}
            if(row["DeptWeatherID"] != None and row["ArrWeatherID"] != None):
                ret["flight"] = row
                cur1 = self.connection.cursor()
                cur1.execute(self.commands[5], (row["DeptWeatherID"],))
                ret["origin_weather"] = self.formatRow(cur1.fetchone(), last_row["origin_weather"])
                cur1.execute(self.commands[5], (row["ArrWeatherID"],))
                ret["destination_weather"] = self.formatRow(cur1.fetchone(), last_row["destination_weather"])
                last_row = ret
                yield ret


    def formatRow(self, row, last_row):
        if(last_row):
            for feature in row:
                if(row[feature] == '' or row[feature] == "VRB" or
                (feature == "HOURLYStationPressure" and "s" in row[feature])):
                    row[feature] = last_row[feature]
        return row


    """transforms row and col into 2d martix just focusing on dep delay"""
    def transformData(self):
        for row in self.getDictionaryRows():
            Y = int(row["flight"]["DepDel15"] == "1.00")
            X = ([int(row["flight"][f]) for f in self.flight_features] +
            [row["origin_weather"][f] for f in self.weather_features] +
            [int(y) for y in row["flight"]["CRSDepTime"].split(":")] +
            [int(y) for y in row["flight"]["CRSArrTime"].split(":")])
            yield X,Y

    def dict_factory(self,cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

def main():
    fl = Flights("flights_weather.db")
    with open ('unbalanced_all_x.csv', 'w') as f, open ('unbalanced_all_y.csv', 'w') as g:
        writer1 = csv.writer(f)
        writer2 = csv.writer(g)
        for row in fl.transformData():
            writer1.writerow(row[0])
            if '' in row[0]:
                print("found nothing")
                print(row[0])
            writer2.writerow([row[1]])
            #print row[0], row[1]





if __name__ == '__main__':
    main()
