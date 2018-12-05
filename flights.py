import sqlite3
from datetime import timedelta

class Flights():
    def __init__(self,database):
        self.connection = sqlite3.connect(database)
        self.commands = {
            0 : "select ID, FlightDate, Origin, CRSDepTime, Dest, CRSArrTime from flights",
            1 : "Select ID, TIME from weather where AIRPORT = ? and DATE = ?",
            2 : "UPDATE flights SET DeptWeatherID = ? WHERE ID = ?",
            3 : "UPDATE flights SET ArrWeatherID = ? WHERE ID = ?",
            4 : "select * from flights",
            5 : "select * from weather WHERE ID = ?"
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
        for row in cur:
            ret = {}
            ret["flight"] = row
            if(row["DeptWeatherID"] != None and row["ArrWeatherID"] != None):
                cur1 = self.connection.cursor()
                cur1.execute(self.commands[5], (row["DeptWeatherID"],))
                ret["origin_weather"] = cur1.fetchone()
                cur1.execute(self.commands[5], (row["ArrWeatherID"],))
                ret["destination_weather"] = cur1.fetchone()
                yield ret

    """transforms row and col into 2d martix just focusing on dep delay"""
    def transformData(self):
        flight_features = ["Month", "DayofMonth", "DayOfWeek",
         "OriginAirportID", "DestAirportID","DOT_ID_Reporting_Airline"]
        weather_features = ["HOURLYWindSpeed", "HOURLYWindDirection",
        "HOURLYDRYBULBTEMPC","HOURLYWETBULBTEMPC", "HOURLYStationPressure",
        "HOURLYRelativeHumidity"]

        X = []
        Y = []
        for row in self.getDictionaryRows():
            Y.append(int(row["flight"]["DepDel15"] == "1.00"))
            f = []
            X.append([int(row["flight"][f]) for f in flight_features] +
            [row["origin_weather"][f] for f in weather_features] +
            [int(y) for y in row["flight"]["CRSDepTime"].split(":")] +
            [int(y) for y in row["flight"]["CRSArrTime"].split(":")])
            print(X,Y)

        return X, Y


    def dict_factory(self,cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d


def main():
    f = Flights("weatherflights.db")
    f.transformData()

if __name__ == '__main__':
    main()
