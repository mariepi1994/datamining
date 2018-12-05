import mysql.connector

cnx = mysql.connector.connect(user='sql9266811', password='G6r7YH52ZL',
                              host='sql9.freemysqlhosting.net',
                              database='sql9266811')

print(cnx)

mycursor = cnx.cursor()
#mycursor.execute("CREATE TABLE CITIES (name VARCHAR(255), id INTEGER)")
mycursor.execute("SHOW TABLES")

for table in mycursor:
    print(table)
# for db in mycursor:
#     print(db)
cnx.close()
