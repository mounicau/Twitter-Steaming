# We used this script to interact with our Azure DB
# interacting == connecting and inserting

import pyodbc

# each group member had to install the SQL Server ODBC driver and run this
# script (through TwitterStreaming_Final.py) to connect to and insert to the DB

# function to connect to DB using generic group credentials
def get_conn():
    server = 'scrapersmsda2017.database.windows.net'
    database = 'msdatwitter'
    username = 'scrapersmsda'
    password = 'msdascrapers@2017'
    driver= '{ODBC Driver 17 for SQL Server}'
    cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    return cnxn, cursor

# function to insert data into the Azure DB and return an error, if one occurs
def insert_data(query,conn, cursor, args ):
    try:
        cursor.execute(query, args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8],
                       args[9], args[10], args[11], args[12], args[13], args[14], args[15], args[16], args[17],
                       args[18], args[19], args[20], args[21], args[22], args[23], args[24], args[25])
        print("------------inserted---------------")
        conn.commit()
    except Exception as exception:
        print("Error Occured", exception)



