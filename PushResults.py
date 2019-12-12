import psycopg2

def ConnectToDB():
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
        # Print PostgreSQL Connection properties
        print ( connection.get_dsn_parameters(),"\n")

        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record,"\n")


        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
ConnectToDB()