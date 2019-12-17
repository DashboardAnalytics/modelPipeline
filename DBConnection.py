import psycopg2
import requests
import csv 
from datetime import datetime

def GetIDS(shoppingName, storeName):
    url = "http://35.193.208.246:3000/shopping/store/name"
    body = {'shopping_name':'Florida Center', 'store_name':'Paris'} 
    r = requests.get(url = url, data = body) 
    data = r.json()
    data = data.get("data")
    storeID = data[0].get("id_store")
    shoppingID = data[0].get("id_shopping")
    return shoppingID, storeID
def SendToDB(csvName):

    print(csvName)
    user = "doadmin"
    password = "qx2a5a5k2rbry8or"
    host = "pingesoresults-do-user-6864511-0.db.ondigitalocean.com"
    port = "25060"
    database = "analyticsDatabase"
    try:
        connection = psycopg2.connect(
            user = user,
            password = password,
            host = host,
            port = port,
            database = database
        )
        cursor = connection.cursor()
        """
        # Print PostgreSQL Connection properties
        with open(csvName, 'r') as f:
            reader = csv.reader(f, delimiter = ";")
            next(reader) # Se salta el header
            for row in reader:
                print(row)
                cursor.execute("INSERT INTO result(frame, n_people, id_shopping, id_store, frame_date, frame_time) VALUES %s %s %s %s %s %s", row)
        """

        sql = "SET datestyle TO European;"
        cursor.execute(sql)
        with open(csvName, 'r') as f:
            reader = csv.reader(f,  delimiter=';')
            next(reader) # Skip the header row.
            for row in reader:
                if(row[1] != ''):
                    cursor.execute("INSERT INTO result(frame, n_people, id_shopping, id_store, frame_date, frame_time) VALUES (%s, %s, %s, %s, %s, %s)",(row[0],str(int(float(row[1]))),row[2],row[3],row[4],row[5],))
                else:
                    cursor.execute("INSERT INTO result(frame, n_people, id_shopping, id_store, frame_date, frame_time) VALUES (%s,%s, %s, %s, %s, %s)",(row[0],"0",row[2],row[3],row[4],row[5],))
        connection.commit()
        cursor.close()
        connection.close()
        print("DB Updated!")
        print("PostgreSQL connection is closed")
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)


